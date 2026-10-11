# AI Powered Resume Analyzer Intelligence 

A high-end resume analytics product with a React/Vite frontend and FastAPI backend.

## Stack

- Frontend: React + Vite + Recharts + Lucide
- Backend: FastAPI
- Storage: SQLite analysis history (easy to replace with PostgreSQL)
- NLP: spaCy entity extraction, NLTK token normalization, and TF-IDF similarity scoring
- AI: Hugging Face Inference Providers using your configured Qwen model
- Web research: Tavily when configured, with best-effort public web fallback
- Parsing: PDF / DOCX / TXT

## Features

1. Overview dashboard
2. Resume Health analytics
3. ATS audit
4. Target-job matching
5. Keyword analytics
6. Content coaching
7. Company intelligence
8. Interview preparation
9. Analysis history storage
10. Dark/light theme

The analysis endpoint accepts PDF, DOCX, and TXT resumes. It returns keyword gaps,
ATS readiness, semantic job matching, interview readiness, and optional Qwen-powered
role-fit and seniority alignment insights. The React/Vite dashboard provides the
interactive equivalent of a Streamlit analytics dashboard while keeping the API
available for other clients.

## Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Optional spaCy model for named-entity extraction
python -m spacy download en_core_web_sm
cp .env.example .env
# Put your NEW Hugging Face token in .env
uvicorn app.main:app --reload --port 8000
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Environment

```env
HUGGINGFACE_API_TOKEN=hf_YOUR_TOKEN
HF_MODEL=Qwen/Qwen2.5-7B-Instruct:featherless-ai
TAVILY_API_KEY=
CORS_ORIGINS=http://localhost:5173
```

Do not commit `.env` or API keys.

## Production next steps

- PostgreSQL instead of SQLite
- Redis/background jobs for long AI analyses
- Authentication and per-user workspaces
- Object storage with short-lived signed URLs if files must persist
- OCR for scanned resumes
- Malware scanning and upload quotas
- Server-side rate limiting
- Structured logging/observability
- Automated tests and CI/CD
- Role/company research caching
- Resume PDF visual rendering and page-layout inspection
- Streaming AI responses for a more dynamic UX
