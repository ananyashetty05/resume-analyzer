from ai_analyzer import get_ai_recommendations
from nlp_utils import (
    analyze_sections,
    calculate_similarity,
    count_quantified_achievements,
    detect_contact_details,
    estimate_experience_years,
    extract_keywords,
    extract_role_signals,
    extract_skills,
    identify_weak_words,
    preprocess_text,
    score_keyword_coverage,
)


def score_resume(resume_text, job_text):
    """Comprehensive resume scoring against a job description with AI analysis."""
    ai_analysis = get_ai_recommendations(resume_text, job_text)

    resume_clean = preprocess_text(resume_text)
    job_clean = preprocess_text(job_text)
    similarity_score = calculate_similarity(resume_clean, job_clean)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    ai_matching_skills = ai_analysis.get("matching_skills", [])
    ai_missing_skills = ai_analysis.get("missing_critical_skills", [])

    matching_skills = list(set(set(resume_skills) & set(job_skills)).union(ai_matching_skills))
    missing_skills = list(set(set(job_skills) - set(resume_skills)).union(ai_missing_skills))

    if job_skills or ai_missing_skills:
        total_required_skills = len(set(job_skills + ai_missing_skills + ai_matching_skills))
        skill_match_score = len(matching_skills) / max(total_required_skills, 1)
    else:
        skill_match_score = 0

    resume_keywords = [kw[0] for kw in extract_keywords(resume_text, 15)]
    job_keywords = [kw[0] for kw in extract_keywords(job_text, 15)]
    matching_keywords = set(resume_keywords) & set(job_keywords)
    missing_keywords = list((set(job_keywords) - set(resume_keywords)).union(ai_analysis.get("keyword_gaps", [])))
    keyword_coverage = score_keyword_coverage(resume_keywords, job_keywords)

    found_sections, missing_sections = analyze_sections(resume_text)
    weak_words = identify_weak_words(resume_text)

    quantified_achievement_count = count_quantified_achievements(resume_text)
    contact_details = detect_contact_details(resume_text)
    contact_score = sum(contact_details.values()) / max(len(contact_details), 1)
    estimated_experience_years = estimate_experience_years(resume_text)
    role_signals = extract_role_signals(resume_text)

    ats_score = calculate_ats_score(resume_text, job_text)
    experience_match = float(ai_analysis.get("experience_match", 70)) / 100
    interview_readiness = float(ai_analysis.get("interview_readiness", 65)) / 100

    overall_score = (
        similarity_score * 0.20 +
        skill_match_score * 0.20 +
        keyword_coverage * 0.20 +
        ats_score * 0.15 +
        experience_match * 0.10 +
        contact_score * 0.05 +
        (quantified_achievement_count >= 3) * 0.05 +
        (role_signals["leadership_score"] / 100) * 0.05
    ) * 100

    return {
        "overall_score": round(overall_score, 2),
        "similarity_score": round(similarity_score * 100, 2),
        "skill_match_score": round(skill_match_score * 100, 2),
        "ats_score": round(ats_score * 100, 2),
        "experience_match": round(experience_match * 100, 2),
        "interview_readiness": round(interview_readiness * 100, 2),
        "keyword_coverage_score": round(keyword_coverage * 100, 2),
        "contact_score": round(contact_score * 100, 2),
        "quantified_achievement_count": quantified_achievement_count,
        "estimated_experience_years": estimated_experience_years,
        "contact_details": contact_details,
        "leadership_score": role_signals["leadership_score"],
        "collaboration_score": role_signals["collaboration_score"],
        "project_score": role_signals["project_score"],
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "resume_keywords": resume_keywords,
        "job_keywords": job_keywords,
        "matching_keywords": list(matching_keywords),
        "missing_keywords": missing_keywords,
        "found_sections": found_sections,
        "missing_sections": missing_sections,
        "weak_words": weak_words,
        "ai_analysis": ai_analysis,
    }


def calculate_ats_score(resume_text, job_text):
    """Calculate ATS compatibility score."""
    score = 0.8

    if len(resume_text.split()) < 200:
        score -= 0.2

    if "pdf" in resume_text.lower() or "image" in resume_text.lower():
        score -= 0.1

    for section in ["experience", "education", "skills"]:
        if section in resume_text.lower():
            score += 0.05

    if not detect_contact_details(resume_text)["email"]:
        score -= 0.1

    if count_quantified_achievements(resume_text) >= 3:
        score += 0.05

    return min(max(score, 0), 1.0)


def generate_suggestions(score_data):
    """Generate comprehensive improvement suggestions."""
    suggestions = {
        "critical": [],
        "important": [],
        "optional": [],
    }

    if score_data["overall_score"] < 40:
        suggestions["critical"].append("Your resume needs significant improvement to match this job.")

    if score_data["missing_sections"]:
        suggestions["critical"].append(f"Add missing sections: {', '.join(score_data['missing_sections'])}")

    if len(score_data["missing_skills"]) > 3:
        suggestions["critical"].append(f"Add key skills: {', '.join(score_data['missing_skills'][:3])}")

    if score_data["missing_keywords"]:
        suggestions["important"].append(f"Include keywords: {', '.join(score_data['missing_keywords'][:5])}")

    if score_data["weak_words"]:
        weak, strong = score_data["weak_words"][0]
        suggestions["important"].append(f"Replace weak phrases: {weak} -> {strong}")

    if score_data["ats_score"] < 70:
        suggestions["important"].append("Improve ATS compatibility by using standard formatting.")

    if score_data["quantified_achievement_count"] < 3:
        suggestions["important"].append("Add more quantified achievements with numbers, percentages, or impact metrics.")

    if score_data["contact_score"] < 80:
        suggestions["important"].append("Strengthen contact details by including email, phone, and professional profile links.")

    if score_data["skill_match_score"] > 70:
        suggestions["optional"].append("Highlight your matching skills more prominently near the top of the resume.")

    if score_data["overall_score"] > 80:
        suggestions["optional"].append("Excellent match. Minor tailoring may further improve results.")

    if score_data["leadership_score"] < 40:
        suggestions["optional"].append("Highlight ownership, leadership, or cross-functional work to show stronger impact.")

    return suggestions


def generate_detailed_feedback(score_data):
    """Generate detailed section-wise feedback."""
    feedback = {
        "strengths": [],
        "improvements": [],
        "additions": [],
        "removals": [],
    }

    if score_data["matching_skills"]:
        feedback["strengths"].append(f"Strong skill alignment: {', '.join(score_data['matching_skills'][:3])}")

    if score_data["similarity_score"] > 60:
        feedback["strengths"].append("Good content relevance to the job description.")

    if score_data["quantified_achievement_count"] >= 3:
        feedback["strengths"].append("Includes quantified achievements that improve recruiter trust.")

    if score_data["weak_words"]:
        for weak, strong in score_data["weak_words"][:2]:
            feedback["improvements"].append(f"Replace '{weak}' with stronger terms like '{strong}'.")

    if score_data["missing_skills"]:
        feedback["additions"].append(f"Add missing skills: {', '.join(score_data['missing_skills'][:3])}")

    if score_data["missing_keywords"]:
        feedback["additions"].append(f"Include job-relevant keywords: {', '.join(score_data['missing_keywords'][:3])}")

    if score_data["contact_score"] < 80:
        feedback["additions"].append("Add missing contact details or professional profile links.")

    feedback["removals"].append("Remove outdated or irrelevant skills.")
    feedback["removals"].append("Eliminate weak action words and filler content.")

    return feedback
