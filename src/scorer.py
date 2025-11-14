from nlp_utils import extract_skills, calculate_similarity, preprocess_text, extract_keywords, analyze_sections, identify_weak_words
from ai_analyzer import get_ai_recommendations

def score_resume(resume_text, job_text):
    """Comprehensive resume scoring against job description with AI analysis"""
    # Get AI-powered analysis
    ai_analysis = get_ai_recommendations(resume_text, job_text)
    
    # Preprocess texts
    resume_clean = preprocess_text(resume_text)
    job_clean = preprocess_text(job_text)
    
    # Calculate similarity score
    similarity_score = calculate_similarity(resume_clean, job_clean)
    
    # Extract skills using both traditional and AI methods
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    
    # Enhance with AI-detected skills
    ai_matching_skills = ai_analysis.get('matching_skills', [])
    ai_missing_skills = ai_analysis.get('missing_critical_skills', [])
    
    # Combine traditional and AI skill detection
    all_matching_skills = list(set(resume_skills) & set(job_skills)) + ai_matching_skills
    all_missing_skills = list(set(job_skills) - set(resume_skills)) + ai_missing_skills
    
    # Remove duplicates
    matching_skills = list(set(all_matching_skills))
    missing_skills = list(set(all_missing_skills))
    
    # Calculate skill match percentage
    if job_skills or ai_missing_skills:
        total_required_skills = len(set(job_skills + ai_missing_skills + ai_matching_skills))
        skill_match_score = len(matching_skills) / max(total_required_skills, 1)
    else:
        skill_match_score = 0
    
    # Extract keywords
    resume_keywords = [kw[0] for kw in extract_keywords(resume_text, 15)]
    job_keywords = [kw[0] for kw in extract_keywords(job_text, 15)]
    
    # Keyword analysis enhanced with AI
    matching_keywords = set(resume_keywords) & set(job_keywords)
    missing_keywords = list(set(job_keywords) - set(resume_keywords))
    ai_keyword_gaps = ai_analysis.get('keyword_gaps', [])
    missing_keywords.extend(ai_keyword_gaps)
    missing_keywords = list(set(missing_keywords))  # Remove duplicates
    
    # Section analysis
    found_sections, missing_sections = analyze_sections(resume_text)
    
    # Weak words analysis
    weak_words = identify_weak_words(resume_text)
    
    # ATS score calculation
    ats_score = calculate_ats_score(resume_text, job_text)
    
    # Experience match from AI
    experience_match = float(ai_analysis.get('experience_match', 70)) / 100
    
    # Overall score (weighted average with AI insights)
    overall_score = (
        similarity_score * 0.25 + 
        skill_match_score * 0.25 + 
        (len(matching_keywords) / max(len(job_keywords), 1)) * 0.2 +
        ats_score * 0.15 +
        experience_match * 0.15
    ) * 100
    
    return {
        'overall_score': round(overall_score, 2),
        'similarity_score': round(similarity_score * 100, 2),
        'skill_match_score': round(skill_match_score * 100, 2),
        'ats_score': round(ats_score * 100, 2),
        'experience_match': round(experience_match * 100, 2),
        'resume_skills': resume_skills,
        'job_skills': job_skills,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'resume_keywords': resume_keywords,
        'job_keywords': job_keywords,
        'matching_keywords': list(matching_keywords),
        'missing_keywords': missing_keywords,
        'found_sections': found_sections,
        'missing_sections': missing_sections,
        'weak_words': weak_words,
        'ai_analysis': ai_analysis
    }

def calculate_ats_score(resume_text, job_text):
    """Calculate ATS compatibility score"""
    score = 0.8  # Base score
    
    # Check for common ATS issues
    if len(resume_text.split()) < 200:
        score -= 0.2  # Too short
    
    if 'pdf' in resume_text.lower() or 'image' in resume_text.lower():
        score -= 0.1  # Potential formatting issues
    
    # Bonus for standard sections
    standard_sections = ['experience', 'education', 'skills']
    for section in standard_sections:
        if section in resume_text.lower():
            score += 0.05
    
    return min(score, 1.0)

def generate_suggestions(score_data):
    """Generate comprehensive improvement suggestions"""
    suggestions = {
        'critical': [],
        'important': [],
        'optional': []
    }
    
    # Critical suggestions
    if score_data['overall_score'] < 40:
        suggestions['critical'].append("Your resume needs significant improvement to match this job")
    
    if score_data['missing_sections']:
        suggestions['critical'].append(f"Add missing sections: {', '.join(score_data['missing_sections'])}")
    
    if len(score_data['missing_skills']) > 3:
        suggestions['critical'].append(f"Add key skills: {', '.join(score_data['missing_skills'][:3])}")
    
    # Important suggestions
    if score_data['missing_keywords']:
        suggestions['important'].append(f"Include keywords: {', '.join(score_data['missing_keywords'][:5])}")
    
    if score_data['weak_words']:
        suggestions['important'].append(f"Replace weak phrases: {score_data['weak_words'][0][0]} → {score_data['weak_words'][0][1]}")
    
    if score_data['ats_score'] < 70:
        suggestions['important'].append("Improve ATS compatibility by using standard formatting")
    
    # Optional suggestions
    if score_data['skill_match_score'] > 70:
        suggestions['optional'].append("Consider highlighting your matching skills more prominently")
    
    if score_data['overall_score'] > 80:
        suggestions['optional'].append("Excellent match! Consider minor tweaks to optimize further")
    
    return suggestions

def generate_detailed_feedback(score_data):
    """Generate detailed section-wise feedback"""
    feedback = {
        'strengths': [],
        'improvements': [],
        'additions': [],
        'removals': []
    }
    
    # Strengths
    if score_data['matching_skills']:
        feedback['strengths'].append(f"Strong skill alignment: {', '.join(score_data['matching_skills'][:3])}")
    
    if score_data['similarity_score'] > 60:
        feedback['strengths'].append("Good content relevance to job description")
    
    # Improvements needed
    if score_data['weak_words']:
        for weak, strong in score_data['weak_words'][:2]:
            feedback['improvements'].append(f"Replace '{weak}' with stronger terms like '{strong}'")
    
    # Additions needed
    if score_data['missing_skills']:
        feedback['additions'].append(f"Add missing skills: {', '.join(score_data['missing_skills'][:3])}")
    
    if score_data['missing_keywords']:
        feedback['additions'].append(f"Include job-relevant keywords: {', '.join(score_data['missing_keywords'][:3])}")
    
    # Potential removals (generic advice)
    feedback['removals'].append("Remove outdated or irrelevant skills")
    feedback['removals'].append("Eliminate weak action words and filler content")
    
    return feedback