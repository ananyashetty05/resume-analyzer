import os
from typing import Dict, List
import json
import re
import requests

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class AIResumeAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('GROK_API_KEY', 'your-grok-api-key-here')
        self.use_ai = self.api_key != 'your-grok-api-key-here'
        self.base_url = "https://api.x.ai/v1/chat/completions"
    
    def analyze_with_ai(self, resume_text: str, job_description: str) -> Dict:
        """Use AI to analyze resume against job description"""
        if not self.use_ai:
            return self._fallback_analysis(resume_text, job_description)
        
        try:
            prompt = f"""
            Analyze this resume against the job description and provide detailed feedback:

            JOB DESCRIPTION:
            {job_description}

            RESUME:
            {resume_text}

            Please provide analysis in the following JSON format:
            {{
                "overall_assessment": "Brief overall assessment",
                "matching_skills": ["skill1", "skill2"],
                "missing_critical_skills": ["skill1", "skill2"],
                "missing_nice_to_have_skills": ["skill1", "skill2"],
                "strengths": ["strength1", "strength2"],
                "weaknesses": ["weakness1", "weakness2"],
                "specific_improvements": ["improvement1", "improvement2"],
                "keyword_gaps": ["keyword1", "keyword2"],
                "experience_match": "How well experience matches (0-100)",
                "ats_recommendations": ["recommendation1", "recommendation2"],
                "content_to_add": ["content1", "content2"],
                "content_to_remove": ["content1", "content2"],
                "action_verbs_to_use": ["achieved", "implemented"],
                "quantifiable_achievements": "Suggestions for adding metrics"
            }}
            """
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "grok-beta",
                "messages": [
                    {"role": "system", "content": "You are an expert resume reviewer and career coach. Provide detailed, actionable feedback."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1500,
                "temperature": 0.3
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()["choices"][0]["message"]["content"]
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return self._fallback_analysis(resume_text, job_description)
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._fallback_analysis(resume_text, job_description)
    
    def _fallback_analysis(self, resume_text: str, job_description: str) -> Dict:
        """Fallback analysis when AI is not available"""
        return {
            "overall_assessment": "Grok AI analysis unavailable - using basic matching",
            "matching_skills": self._extract_matching_skills(resume_text, job_description),
            "missing_critical_skills": self._extract_missing_skills(resume_text, job_description),
            "missing_nice_to_have_skills": [],
            "strengths": ["Resume uploaded successfully"],
            "weaknesses": ["Enable AI analysis for detailed feedback"],
            "specific_improvements": ["Add Grok API key for AI-powered analysis"],
            "keyword_gaps": self._find_keyword_gaps(resume_text, job_description),
            "experience_match": "70",
            "ats_recommendations": ["Use standard section headers", "Include relevant keywords"],
            "content_to_add": ["Quantified achievements", "Relevant keywords"],
            "content_to_remove": ["Outdated skills", "Irrelevant information"],
            "action_verbs_to_use": ["achieved", "implemented", "developed", "managed"],
            "quantifiable_achievements": "Add specific numbers and percentages to achievements"
        }
    
    def _extract_matching_skills(self, resume_text: str, job_description: str) -> List[str]:
        """Extract skills that appear in both resume and job description"""
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'machine learning', 'data analysis',
            'project management', 'agile', 'scrum', 'leadership', 'communication'
        ]
        
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        matching = []
        for skill in common_skills:
            if skill in resume_lower and skill in job_lower:
                matching.append(skill)
        
        return matching
    
    def _extract_missing_skills(self, resume_text: str, job_description: str) -> List[str]:
        """Extract skills mentioned in job description but not in resume"""
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'machine learning', 'data analysis',
            'project management', 'agile', 'scrum', 'leadership', 'communication',
            'tensorflow', 'pytorch', 'mongodb', 'postgresql', 'redis'
        ]
        
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        missing = []
        for skill in common_skills:
            if skill in job_lower and skill not in resume_lower:
                missing.append(skill)
        
        return missing
    
    def _find_keyword_gaps(self, resume_text: str, job_description: str) -> List[str]:
        """Find important keywords missing from resume"""
        # Extract important words from job description
        job_words = re.findall(r'\b[a-zA-Z]{4,}\b', job_description.lower())
        resume_words = re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower())
        
        # Common important keywords
        important_keywords = [
            'experience', 'development', 'management', 'analysis', 'design',
            'implementation', 'optimization', 'collaboration', 'innovation'
        ]
        
        gaps = []
        for keyword in important_keywords:
            if keyword in job_words and keyword not in resume_words:
                gaps.append(keyword)
        
        return gaps[:5]  # Return top 5 gaps

def get_ai_recommendations(resume_text: str, job_description: str) -> Dict:
    """Get AI-powered recommendations for resume improvement"""
    analyzer = AIResumeAnalyzer()
    return analyzer.analyze_with_ai(resume_text, job_description)