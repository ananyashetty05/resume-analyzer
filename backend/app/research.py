from __future__ import annotations
import os, re
from urllib.parse import quote_plus

def clean(x): return re.sub(r"\s+"," ",x or "").strip()

def detect_company(job):
    patterns=[
        r"(?:company|employer|organization)\s*[:\-]\s*([A-Z][A-Za-z0-9&.' -]{2,70})",
        r"(?:at|join|joining)\s+([A-Z][A-Za-z0-9&.'-]{2,50})(?:\s+as|\s+for|\s*$)",
    ]
    for p in patterns:
        m=re.search(p,job or "")
        if m:return clean(m.group(1)).strip(".,")
    return ""

def research_company(company):
    key=os.getenv("TAVILY_API_KEY")
    if key:
        try:
            import requests
            r=requests.post("https://api.tavily.com/search",
                json={"api_key":key,"query":f"{company} company products careers culture recent news interview","search_depth":"advanced","max_results":8,"include_answer":True},
                timeout=20)
            r.raise_for_status(); d=r.json()
            return {"company":company,"source":"Tavily","answer":d.get("answer",""),
                    "results":[{"title":x.get("title",""),"url":x.get("url",""),"snippet":x.get("content","")[:700]} for x in d.get("results",[])]}
        except Exception: pass
    try:
        import requests
        from bs4 import BeautifulSoup
        q=quote_plus(f"{company} company careers products interview")
        html=requests.get(f"https://html.duckduckgo.com/html/?q={q}",headers={"User-Agent":"Mozilla/5.0"},timeout=15).text
        soup=BeautifulSoup(html,"html.parser"); results=[]
        for a in soup.select(".result__a")[:8]:
            parent=a.find_parent(".result")
            results.append({"title":clean(a.get_text(" ",strip=True)),"url":a.get("href",""),
                            "snippet":clean(parent.select_one(".result__snippet").get_text(" ",strip=True)) if parent and parent.select_one(".result__snippet") else ""})
        return {"company":company,"source":"Web search","answer":"","results":results}
    except Exception:
        return {"company":company,"source":"offline","answer":"","results":[],"message":"Add TAVILY_API_KEY for reliable company research."}
