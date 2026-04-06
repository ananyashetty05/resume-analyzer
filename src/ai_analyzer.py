import json
import os
import re
from typing import Dict, List

import requests

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class AIResumeAnalyzer:
    def __init__(self):
        self.api_key = (
            os.getenv("HUGGINGFACE_API_TOKEN")
            or os.getenv("HF_TOKEN")
            or ""
        ).strip()
        self.model = os.getenv("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct-1M").strip()
        self.use_ai = bool(self.api_key)
        self.base_url = "https://router.huggingface.co/v1/chat/completions"

    def analyze_with_ai(self, resume_text: str, job_description: str) -> Dict:
        """Use Hugging Face AI to analyze a resume against a job description."""
        if not self.use_ai:
            return self._fallback_analysis(resume_text, job_description)

        try:
            prompt = f"""
You are an expert ATS resume reviewer and career coach.
Return valid JSON only with no markdown fences or extra commentary.

Analyze this resume against the job description.

JOB DESCRIPTION:
{job_description[:5000]}

RESUME:
{resume_text[:7000]}

Return JSON in this exact shape:
{{
    "overall_assessment": "Brief overall assessment",
    "matching_skills": ["skill1", "skill2"],
    "missing_critical_skills": ["skill1", "skill2"],
    "missing_nice_to_have_skills": ["skill1", "skill2"],
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "specific_improvements": ["improvement1", "improvement2"],
    "keyword_gaps": ["keyword1", "keyword2"],
    "experience_match": "0-100",
    "ats_recommendations": ["recommendation1", "recommendation2"],
    "content_to_add": ["content1", "content2"],
    "content_to_remove": ["content1", "content2"],
    "action_verbs_to_use": ["achieved", "implemented"],
    "quantifiable_achievements": "Suggestions for adding metrics",
    "role_fit_summary": "Short fit summary",
    "seniority_alignment": "entry-level | mid-level | senior-level | mixed",
    "industry_alignment": "Short industry alignment note",
    "top_resume_highlights": ["highlight1", "highlight2"],
    "interview_readiness": "0-100"
}}
"""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert ATS resume reviewer and career coach. Always return valid JSON only.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                "max_tokens": 900,
                "temperature": 0.2,
                "stream": False,
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=45,
            )
            response.raise_for_status()

            result_text = self._extract_response_text(response.json())
            parsed = self._parse_json_response(result_text)
            if parsed:
                return self._normalize_ai_response(parsed)
            return self._fallback_analysis(resume_text, job_description)
        except Exception as exc:
            print(f"AI analysis failed: {exc}")
            return self._fallback_analysis(resume_text, job_description)

    def _fallback_analysis(self, resume_text: str, job_description: str) -> Dict:
        """Fallback analysis when AI is unavailable."""
        return {
            "overall_assessment": "Hugging Face AI analysis unavailable, using built-in resume matching.",
            "matching_skills": self._extract_matching_skills(resume_text, job_description),
            "missing_critical_skills": self._extract_missing_skills(resume_text, job_description),
            "missing_nice_to_have_skills": [],
            "strengths": ["Resume content was processed successfully."],
            "weaknesses": ["Connect a Hugging Face token for deeper AI feedback."],
            "specific_improvements": ["Add HUGGINGFACE_API_TOKEN in .env to enable AI-powered guidance."],
            "keyword_gaps": self._find_keyword_gaps(resume_text, job_description),
            "experience_match": "70",
            "ats_recommendations": ["Use standard section headers", "Include relevant keywords"],
            "content_to_add": ["Quantified achievements", "Relevant keywords"],
            "content_to_remove": ["Outdated skills", "Irrelevant information"],
            "action_verbs_to_use": ["achieved", "implemented", "developed", "managed"],
            "quantifiable_achievements": "Add specific numbers and percentages to achievements.",
            "role_fit_summary": "The resume has partial alignment based on keyword and skills overlap.",
            "seniority_alignment": "mixed",
            "industry_alignment": "Industry fit could not be deeply evaluated without AI support.",
            "top_resume_highlights": ["Core resume parsing is active.", "Skills and ATS checks are available."],
            "interview_readiness": "65",
        }

    def _extract_matching_skills(self, resume_text: str, job_description: str) -> List[str]:
        """Extract skills that appear in both resume and job description."""
        common_skills = [
            "python", "java", "javascript", "react", "node.js", "sql", "aws",
            "docker", "kubernetes", "git", "machine learning", "data analysis",
            "project management", "agile", "scrum", "leadership", "communication",
        ]

        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        return [skill for skill in common_skills if skill in resume_lower and skill in job_lower]

    def _extract_missing_skills(self, resume_text: str, job_description: str) -> List[str]:
        """Extract skills mentioned in job description but not in resume."""
        common_skills = [
            "python", "java", "javascript", "react", "node.js", "sql", "aws",
            "docker", "kubernetes", "git", "machine learning", "data analysis",
            "project management", "agile", "scrum", "leadership", "communication",
            "tensorflow", "pytorch", "mongodb", "postgresql", "redis",
        ]

        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        return [skill for skill in common_skills if skill in job_lower and skill not in resume_lower]

    def _find_keyword_gaps(self, resume_text: str, job_description: str) -> List[str]:
        """Find important keywords missing from the resume."""
        job_words = re.findall(r"\b[a-zA-Z]{4,}\b", job_description.lower())
        resume_words = re.findall(r"\b[a-zA-Z]{4,}\b", resume_text.lower())
        important_keywords = [
            "experience", "development", "management", "analysis", "design",
            "implementation", "optimization", "collaboration", "innovation",
        ]

        return [
            keyword for keyword in important_keywords
            if keyword in job_words and keyword not in resume_words
        ][:5]

    def _extract_response_text(self, payload) -> str:
        if isinstance(payload, dict):
            choices = payload.get("choices", [])
            if choices and isinstance(choices[0], dict):
                message = choices[0].get("message", {})
                if isinstance(message, dict):
                    return message.get("content", "")
        return ""

    def _parse_json_response(self, text: str) -> Dict:
        if not text:
            return {}

        cleaned = text.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if not match:
                return {}
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return {}

    def _normalize_ai_response(self, payload: Dict) -> Dict:
        defaults = self._fallback_analysis("", "")
        merged = {**defaults, **payload}

        list_fields = [
            "matching_skills",
            "missing_critical_skills",
            "missing_nice_to_have_skills",
            "strengths",
            "weaknesses",
            "specific_improvements",
            "keyword_gaps",
            "ats_recommendations",
            "content_to_add",
            "content_to_remove",
            "action_verbs_to_use",
            "top_resume_highlights",
        ]
        for field in list_fields:
            value = merged.get(field, [])
            if isinstance(value, str):
                merged[field] = [item.strip() for item in value.split(",") if item.strip()]
            elif not isinstance(value, list):
                merged[field] = defaults.get(field, [])

        text_fields = [
            "overall_assessment",
            "experience_match",
            "quantifiable_achievements",
            "role_fit_summary",
            "seniority_alignment",
            "industry_alignment",
            "interview_readiness",
        ]
        for field in text_fields:
            value = merged.get(field)
            merged[field] = defaults.get(field, "") if value is None else str(value).strip()

        return merged


def get_ai_recommendations(resume_text: str, job_description: str) -> Dict:
    """Get AI-powered recommendations for resume improvement."""
    analyzer = AIResumeAnalyzer()
    return analyzer.analyze_with_ai(resume_text, job_description)
