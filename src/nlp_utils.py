import re

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


def preprocess_text(text):
    """Clean and preprocess text."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_skills(text):
    """Extract skills from text using comprehensive skill categories."""
    skills_categories = {
        "programming": ["python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin"],
        "web_frameworks": ["react", "angular", "vue.js", "node.js", "express", "django", "flask", "spring", "laravel"],
        "databases": ["sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "oracle", "sqlite"],
        "cloud_devops": ["aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible"],
        "data_science": ["machine learning", "deep learning", "data analysis", "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn"],
        "tools": ["git", "jira", "confluence", "slack", "excel", "powerbi", "tableau", "figma", "photoshop"],
    }

    found_skills = []
    text_lower = text.lower()

    for skills in skills_categories.values():
        for skill in skills:
            if skill in text_lower:
                found_skills.append(skill)

    return found_skills


def extract_keywords(text, top_n=20):
    """Extract important keywords using TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    keywords = [(feature_names[i], scores[i]) for i in range(len(feature_names))]
    return sorted(keywords, key=lambda x: x[1], reverse=True)


def analyze_sections(resume_text):
    """Analyze resume sections and identify missing ones."""
    sections = {
        "contact": ["email", "phone", "linkedin", "github"],
        "summary": ["summary", "objective", "profile"],
        "experience": ["experience", "work", "employment", "career"],
        "education": ["education", "degree", "university", "college"],
        "skills": ["skills", "technical", "technologies"],
        "projects": ["projects", "portfolio"],
        "certifications": ["certification", "certified", "license"],
    }

    found_sections = []
    text_lower = resume_text.lower()

    for section, keywords in sections.items():
        if any(keyword in text_lower for keyword in keywords):
            found_sections.append(section)

    missing_sections = [section for section in sections if section not in found_sections]
    return found_sections, missing_sections


def calculate_similarity(resume_text, job_text):
    """Calculate similarity between resume and job description."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]


def identify_weak_words(text):
    """Identify weak words that should be replaced with stronger alternatives."""
    weak_words = {
        "responsible for": "managed, led, oversaw",
        "worked on": "developed, implemented, created",
        "helped": "assisted, supported, facilitated",
        "did": "executed, performed, accomplished",
        "made": "created, developed, built",
        "good": "excellent, proficient, skilled",
        "basic": "fundamental, foundational",
    }

    found_weak_words = []
    text_lower = text.lower()

    for weak, strong in weak_words.items():
        if weak in text_lower:
            found_weak_words.append((weak, strong))

    return found_weak_words


def count_quantified_achievements(text):
    """Estimate how many quantified achievements the resume contains."""
    patterns = [
        r"\b\d+%\b",
        r"\b\d+\+?\b",
        r"\$\s?\d[\d,]*",
        r"\b\d+\s?(years|yrs|months|people|users|clients|projects)\b",
    ]

    match_count = 0
    lowered = text.lower()
    for pattern in patterns:
        match_count += len(re.findall(pattern, lowered))
    return match_count


def detect_contact_details(text):
    """Check which contact methods are present."""
    lowered = text.lower()
    return {
        "email": bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)),
        "phone": bool(re.search(r"(\+\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}", text)),
        "linkedin": "linkedin.com" in lowered,
        "github": "github.com" in lowered,
        "portfolio": bool(re.search(r"https?://", lowered)) or "portfolio" in lowered,
    }


def estimate_experience_years(text):
    """Estimate years of experience referenced in the resume."""
    matches = re.findall(r"(\d+)\+?\s*(?:years|yrs)", text.lower())
    if not matches:
        return 0
    return max(int(match) for match in matches)


def score_keyword_coverage(resume_keywords, job_keywords):
    """Calculate keyword coverage ratio."""
    job_set = set(job_keywords)
    if not job_set:
        return 0
    return len(set(resume_keywords) & job_set) / len(job_set)


def extract_role_signals(text):
    """Capture simple leadership, collaboration, and project-delivery signals."""
    lowered = text.lower()
    leadership_terms = ["led", "managed", "mentored", "owned", "coordinated", "spearheaded"]
    collaboration_terms = ["collaborated", "partnered", "cross-functional", "stakeholders", "team"]
    project_terms = ["project", "projects", "built", "developed", "launched", "shipped"]

    leadership_hits = sum(1 for term in leadership_terms if term in lowered)
    collaboration_hits = sum(1 for term in collaboration_terms if term in lowered)
    project_hits = sum(1 for term in project_terms if term in lowered)

    return {
        "leadership_score": min(leadership_hits * 20, 100),
        "collaboration_score": min(collaboration_hits * 20, 100),
        "project_score": min(project_hits * 15, 100),
    }
