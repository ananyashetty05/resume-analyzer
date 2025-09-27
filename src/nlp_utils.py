import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def preprocess_text(text):
    """Clean and preprocess text"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills(text):
    """Extract skills from text using predefined skill list"""
    skills_list = [
        'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
        'machine learning', 'data analysis', 'aws', 'docker', 'kubernetes',
        'git', 'html', 'css', 'angular', 'vue.js', 'tensorflow', 'pytorch',
        'excel', 'powerbi', 'tableau', 'r', 'scala', 'spark', 'hadoop'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in skills_list:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills

def calculate_similarity(resume_text, job_text):
    """Calculate similarity between resume and job description"""
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]