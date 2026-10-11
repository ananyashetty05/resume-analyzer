from __future__ import annotations

import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .parser import extract_resume_text
from .scoring import analyze_resume
from .ai import ai_analyze
from .research import research_company, detect_company

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "resume_intelligence.db"

app = FastAPI(title="Resume Intelligence API", version="2.0.0")

origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            filename TEXT,
            company TEXT,
            role TEXT,
            overall REAL,
            created_at TEXT,
            payload TEXT
        )
    """)
    conn.commit()
    return conn

class CompanyRequest(BaseModel):
    company: str

@app.get("/api/health")
def health():
    return {"status": "ok", "llm_configured": bool(os.getenv("HUGGINGFACE_API_TOKEN") or os.getenv("HF_TOKEN"))}

@app.post("/api/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(""),
    company: str = Form(""),
    role: str = Form(""),
):
    allowed = {".pdf", ".docx", ".txt"}
    suffix = Path(resume.filename or "").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, "Upload PDF, DOCX, or TXT.")

    raw = await resume.read()
    if len(raw) > 8 * 1024 * 1024:
        raise HTTPException(413, "Resume must be smaller than 8 MB.")

    try:
        text = extract_resume_text(raw, suffix)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

    company = company.strip() or detect_company(job_description)
    deterministic = analyze_resume(text, job_description)
    ai = ai_analyze(text, job_description, role, deterministic)

    analysis_id = str(uuid.uuid4())
    payload = {
        "id": analysis_id,
        "filename": resume.filename,
        "company": company,
        "role": role,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scores": deterministic["scores"],
        "profile": deterministic["profile"],
        "contact": deterministic["contact"],
        "sections": deterministic["sections"],
        "skills": deterministic["skills"],
        "keywords": deterministic["keywords"],
        "ats": deterministic["ats"],
        "achievements": deterministic["achievements"],
        "writing": deterministic["writing"],
        "ai": ai,
        "job_description_present": bool(job_description.strip()),
    }

    conn = db()
    conn.execute(
        "INSERT INTO analyses VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            analysis_id,
            resume.filename,
            company,
            role,
            deterministic["scores"]["overall"],
            payload["created_at"],
            __import__("json").dumps(payload),
        ),
    )
    conn.commit()
    conn.close()

    return payload

@app.post("/api/research-company")
def company_research(req: CompanyRequest):
    if not req.company.strip():
        raise HTTPException(400, "Company name is required.")
    return research_company(req.company.strip())

@app.get("/api/analyses")
def analyses(limit: int = 10):
    conn = db()
    rows = conn.execute(
        "SELECT id, filename, company, role, overall, created_at FROM analyses ORDER BY created_at DESC LIMIT ?",
        (max(1, min(limit, 50)),),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
