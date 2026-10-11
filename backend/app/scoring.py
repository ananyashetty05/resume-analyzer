from __future__ import annotations
import re
from collections import Counter

STOP = set("""
a an and are as at be by for from in is it of on or that the to with will you your we our
required preferred experience have has had need looking this into using use used work working
role job candidate ability responsibilities responsibility including
""".split())

def norm(text): return re.sub(r"\s+", " ", re.sub(r"[^\w+#./%₹$€£&' -]", " ", (text or "").lower())).strip()
def toks(text): return re.findall(r"[a-zA-Z][a-zA-Z0-9+#./&-]*", norm(text))
def meaningful(text): return [x for x in toks(text) if len(x)>2 and x not in STOP and not x.isdigit()]

def present(term, text):
    n, t = norm(term), norm(text)
    if not n: return False
    if re.search(rf"(?<!\w){re.escape(n)}(?!\w)", t): return True
    parts = meaningful(term)
    have = set(meaningful(text))
    return bool(parts) and sum(p in have for p in parts)/len(parts) >= .75

def job_terms(job):
    if not job.strip(): return []
    spans = re.findall(
        r"(?:required|preferred|must have|need(?:ed)?|looking for|experience with|"
        r"proficient in|expertise in|skills?|technologies|tools|platforms|knowledge of)"
        r"\s*[:\-]?\s*([^\n.;]{2,280})", job, re.I
    )
    candidates=[]
    for span in spans:
        for item in re.split(r",|/|\||\band\b|\bor\b", span, flags=re.I):
            item=" ".join(meaningful(item))
            if 2 < len(item) < 70: candidates.append(item)
    candidates += [t.lower() for t in toks(job) if any(c in t for c in "+#./-") or (t.isupper() and len(t)<=12)]
    return list(dict.fromkeys(candidates))[:35]

def keyword_terms(job):
    words=meaningful(job)
    counts=Counter(words)
    big=Counter(" ".join(words[i:i+2]) for i in range(len(words)-1))
    all_terms=list(counts.items())+[(k,v*1.35) for k,v in big.items()]
    all_terms.sort(key=lambda x:x[1], reverse=True)
    seen=[]; 
    for term,_ in all_terms:
        if term not in seen: seen.append(term)
    return seen[:30]

ALIASES={
"summary":["summary","professional summary","profile","objective"],
"experience":["experience","work experience","professional experience","employment"],
"education":["education","academic background","qualifications"],
"skills":["skills","technical skills","core skills","technologies"],
"projects":["projects","academic projects","personal projects"],
"certifications":["certifications","certificates","licenses"],
"leadership":["leadership","activities","positions of responsibility"],
}
def sections(text):
    found={}
    for line in text.splitlines():
        x=re.sub(r"[^a-z ]","",line.lower()).strip()
        x=re.sub(r"\s+"," ",x)
        if len(x)<=45:
            for k,aliases in ALIASES.items():
                if x in aliases: found[k]=line.strip(" -:|")
    return found

def contacts(text):
    urls=re.findall(r"(?:https?://)?(?:www\.)?[\w.-]+\.[a-z]{2,}(?:/[^\s]*)?",text,re.I)
    return {
        "email": bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+",text)),
        "phone": bool(re.search(r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]\d{3,4}",text)),
        "linkedin_or_portfolio": any(x for x in urls if any(k in x.lower() for k in ["linkedin","github","portfolio"])),
    }

def achievement_lines(text):
    lines=[x.strip("•-* \t") for x in text.splitlines() if x.strip()]
    return [x for x in lines if re.search(
        r"(?:\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*(?:users?|customers?|projects?|clients?|hours?|days?|months?|years?)|[$₹€£]\s*\d+)", x, re.I)]

def writing(text):
    bullets=[x for x in text.splitlines() if re.match(r"^\s*(?:[-•*]|\d+[.)])\s+",x)]
    avg=sum(len(x.split()) for x in bullets)/len(bullets) if bullets else 0
    return {"word_count":len(text.split()),"line_count":len([x for x in text.splitlines() if x.strip()]),
            "bullet_count":len(bullets),"avg_bullet_words":round(avg,1)}

def similarity(a,b):
    if not b.strip(): return 0
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        m=TfidfVectorizer(stop_words="english",ngram_range=(1,2),max_features=6000).fit_transform([a,b])
        return float(cosine_similarity(m[0:1],m[1:2])[0][0])
    except Exception:
        A,B=set(meaningful(a)),set(meaningful(b))
        return len(A&B)/len(A|B) if A|B else 0

def nlp_enrichment(text):
    entities=[]
    engines=[]

    try:
        import spacy
        try:
            pipeline=spacy.load("en_core_web_sm")
        except Exception:
            pipeline=spacy.blank("en")
        entities=[
            {"text": entity.text, "label": entity.label_}
            for entity in pipeline(text).ents
        ][:30]
        engines.append("spaCy")
    except Exception:
        pass

    try:
        from nltk.stem import SnowballStemmer
        from nltk.tokenize import wordpunct_tokenize
        stemmer=SnowballStemmer("english")
        tokens=[x for x in wordpunct_tokenize(text) if re.search(r"[A-Za-z]", x)]
        stems={stemmer.stem(x.lower()) for x in tokens}
        engines.append("NLTK")
    except Exception:
        stems=set()

    return {
        "engines": engines,
        "entities": entities,
        "stemmed_token_count": len(stems),
        "tfidf_similarity": True,
    }

def analyze_resume(text, job=""):
    terms=job_terms(job)
    matched=[x for x in terms if present(x,text)]
    missing=[x for x in terms if x not in matched]
    kws=keyword_terms(job)
    kwmatch=[x for x in kws if present(x,text)]
    sec=sections(text); con=contacts(text); ach=achievement_lines(text); wr=writing(text)
    sim=similarity(norm(text),norm(job))
    skill=len(matched)/len(terms) if terms else 1
    keyword=len(kwmatch)/len(kws) if kws else 1
    structure=min(len(sec)/5,1)
    contact=sum(con.values())/3
    evidence=min(len(ach)/5,1)
    scan=1 if 250<=wr["word_count"]<=900 else (.75 if wr["word_count"]>=150 else .45)
    ats=.25*structure+.20*contact+.25*evidence+.15*keyword+.15*scan
    overall=(.30*skill+.18*keyword+.18*sim+.24*ats+.10*evidence) if job else (.55*ats+.25*evidence+.20*structure)
    risks=[]
    if len(sec)<3: risks.append({"severity":"high","message":"Use standard headings such as Experience, Education, Skills and Projects."})
    if not con["email"]: risks.append({"severity":"high","message":"No email address detected."})
    if not con["phone"]: risks.append({"severity":"medium","message":"No phone number detected."})
    if not ach: risks.append({"severity":"medium","message":"No quantified achievement evidence detected."})
    if wr["avg_bullet_words"]>35: risks.append({"severity":"medium","message":"Some bullets are unusually long; shorten them for scanability."})
    if re.search(r"\b(date of birth|marital status|father|mother|references available)\b",text,re.I):
        risks.append({"severity":"medium","message":"Potentially unnecessary personal/reference information detected."})
    nlp=nlp_enrichment(text)
    profile={
        "word_count":wr["word_count"],
        "estimated_pages":max(1,round(wr["word_count"]/500)),
        "quantified_achievements":len(ach),
        "sections_found":len(sec),
        "nlp_entities":len(nlp["entities"]),
    }
    return {
        "scores":{"overall":round(overall*100,1),"ats":round(ats*100,1),"skill_match":round(skill*100,1),
                  "keywords":round(keyword*100,1),"semantic_match":round(sim*100,1),
                  "evidence":round(evidence*100,1),"interview_readiness":round((.55*overall+.25*evidence+.20*skill)*100,1)},
        "profile":profile,"nlp":nlp,"contact":con,"sections":sec,
        "skills":{"matched":matched,"missing":missing,"all_job_terms":terms},
        "keywords":{"matched":kwmatch,"missing":[x for x in kws if x not in kwmatch],"all":kws},
        "ats":{"risks":risks,"structure_score":round(structure*100,1),"contact_score":round(contact*100,1),
               "scanability_score":round(scan*100,1)},
        "achievements":ach[:20],"writing":wr
    }
