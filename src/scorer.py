from nlp_utils import extract_skills, calculate_similarity, preprocess_text

def score_resume(resume_text, job_text):
    """Score resume against job description"""
    # Preprocess texts
    resume_clean = preprocess_text(resume_text)
    job_clean = preprocess_text(job_text)
    
    # Calculate similarity score
    similarity_score = calculate_similarity(resume_clean, job_clean)
    
    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    
    # Calculate skill match percentage
    if job_skills:
        matching_skills = set(resume_skills) & set(job_skills)
        skill_match_score = len(matching_skills) / len(job_skills)
    else:
        skill_match_score = 0
    
    # Overall score (weighted average)
    overall_score = (similarity_score * 0.6 + skill_match_score * 0.4) * 100
    
    return {
        'overall_score': round(overall_score, 2),
        'similarity_score': round(similarity_score * 100, 2),
        'skill_match_score': round(skill_match_score * 100, 2),
        'resume_skills': resume_skills,
        'job_skills': job_skills,
        'matching_skills': list(set(resume_skills) & set(job_skills)),
        'missing_skills': list(set(job_skills) - set(resume_skills))
    }

def generate_suggestions(score_data):
    """Generate improvement suggestions"""
    suggestions = []
    
    if score_data['overall_score'] < 50:
        suggestions.append("Consider tailoring your resume more closely to the job requirements")
    
    if score_data['missing_skills']:
        suggestions.append(f"Consider adding these skills: {', '.join(score_data['missing_skills'][:5])}")
    
    if score_data['skill_match_score'] < 30:
        suggestions.append("Highlight more relevant technical skills in your resume")
    
    if not suggestions:
        suggestions.append("Great match! Your resume aligns well with the job requirements")
    
    return suggestions