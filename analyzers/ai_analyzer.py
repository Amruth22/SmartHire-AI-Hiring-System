"""
AI Analyzer - Pure Tool
Performs AI-powered analysis using Gemini
NO state management, NO orchestration logic
"""

import logging
import json
import re
from typing import Dict, Any, List
from utils.gemini_client import GeminiClient

logger = logging.getLogger("ai_analyzer")


class AIAnalyzer:
    """Pure AI analysis tool - reusable across workflows"""
    
    def __init__(self, api_key_name: str = "GEMINI_API_KEY_1"):
        """
        Initialize AI analyzer
        
        Args:
            api_key_name: Name of the API key to use
        """
        self.client = GeminiClient(api_key_name)
        logger.info(f"AI Analyzer initialized with {api_key_name}")
    
    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse resume text and extract structured features
        
        Args:
            resume_text: Raw resume text
        
        Returns:
            Dictionary with extracted resume features
        """
        if not self.client.is_available():
            logger.warning("Gemini client not available, using fallback parsing")
            return self._fallback_parse_resume(resume_text)
        
        try:
            prompt = f"""Extract structured data from this resume. Return valid JSON only:

{{
  "full_name": str,
  "email": str,
  "phone": str,
  "education": {{"degree": str, "major": str, "university": str}},
  "total_experience_years": float,
  "skills": [str],
  "projects": [str],
  "certifications": [str],
  "leadership_experience": int,
  "has_research_work": int
}}

Resume: {resume_text[:3000]}
"""
            
            response = self.client.generate_content(prompt)
            cleaned = self._clean_json_response(response)
            features = json.loads(cleaned)
            
            logger.info(f"Successfully parsed resume for {features.get('full_name', 'Unknown')}")
            return features
            
        except Exception as e:
            logger.error(f"AI resume parsing failed: {e}")
            return self._fallback_parse_resume(resume_text)
    
    
    def predict_experience_level(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict candidate experience level using AI
        
        Args:
            resume_features: Extracted resume features
        
        Returns:
            Dictionary with experience level and confidence
        """
        if not self.client.is_available():
            return self._fallback_experience_level(resume_features)
        
        try:
            years = resume_features.get('total_experience_years', 0)
            skills = resume_features.get('skills', [])
            projects = resume_features.get('projects', [])
            certs = resume_features.get('certifications', [])
            
            prompt = f"""Analyze candidate experience level based on their profile.

Candidate Profile:
- Total Experience: {years} years
- Skills: {len(skills)} skills - {', '.join(skills[:10])}
- Projects: {len(projects)} projects
- Certifications: {len(certs)} certifications

Classify as: Junior (0-2 years), Mid-Level (2-5 years), or Senior (5+ years)

Return JSON only:
{{"experience_level": "Junior/Mid-Level/Senior", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}
"""
            
            response = self.client.generate_content(prompt)
            result = json.loads(self._clean_json_response(response))
            
            experience_level = result.get('experience_level', 'Mid-Level')
            confidence = float(result.get('confidence', 0.8))
            
            logger.info(f"AI predicted experience: {experience_level} (confidence: {confidence:.2f})")
            
            return {
                "experience_level": experience_level,
                "confidence": confidence,
                "reasoning": result.get('reasoning', 'AI analysis complete')
            }
            
        except Exception as e:
            logger.error(f"AI experience prediction failed: {e}")
            return self._fallback_experience_level(resume_features)
    
    def score_resume(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score resume quality using AI
        
        Args:
            resume_features: Extracted resume features
        
        Returns:
            Dictionary with resume score and breakdown
        """
        if not self.client.is_available():
            return self._fallback_resume_score(resume_features)
        
        try:
            years = resume_features.get('total_experience_years', 0)
            skills = resume_features.get('skills', [])
            projects = resume_features.get('projects', [])
            certs = resume_features.get('certifications', [])
            education = resume_features.get('education', {})
            
            prompt = f"""Score this resume on a scale of 0-10 based on quality and completeness.

Resume Profile:
- Experience: {years} years
- Skills: {len(skills)} skills - {', '.join(skills[:10])}
- Projects: {len(projects)} projects
- Certifications: {len(certs)} certifications
- Education: {education.get('degree', 'Not specified')}

Evaluate:
1. Experience depth and relevance
2. Skills breadth and technical depth
3. Project portfolio quality
4. Professional certifications
5. Education background

Return JSON only:
{{"resume_score": 0-10, "breakdown": {{"experience": 0-10, "skills": 0-10, "projects": 0-10, "certifications": 0-10, "education": 0-10}}, "feedback": "brief feedback"}}
"""
            
            response = self.client.generate_content(prompt)
            result = json.loads(self._clean_json_response(response))
            
            score = float(result.get('resume_score', 5.0))
            score = min(10.0, max(0.0, score))
            
            logger.info(f"AI scored resume: {score:.2f}/10")
            
            return {
                "resume_score": score,
                "breakdown": result.get('breakdown', {}),
                "feedback": result.get('feedback', 'Resume evaluated')
            }
            
        except Exception as e:
            logger.error(f"AI resume scoring failed: {e}")
            return self._fallback_resume_score(resume_features)

    def analyze_job_fit(self, resume_features: Dict[str, Any], 
                       job_description: str, job_title: str) -> Dict[str, Any]:
        """
        Analyze job fit between candidate and position
        
        Args:
            resume_features: Extracted resume features
            job_description: Job description text
            job_title: Job title
        
        Returns:
            Dictionary with job fit analysis
        """
        if not self.client.is_available():
            return self._fallback_job_fit()
        
        try:
            candidate_skills = resume_features.get('skills', [])
            experience_years = resume_features.get('total_experience_years', 0)
            
            prompt = f"""Analyze job fit between candidate and position.

Candidate Profile:
- Skills: {', '.join(candidate_skills[:15])}
- Experience: {experience_years} years
- Projects: {len(resume_features.get('projects', []))}
- Certifications: {len(resume_features.get('certifications', []))}

Job Position:
- Title: {job_title}
- Description: {job_description[:500]}

Provide analysis in this format:
Fit: [Excellent Fit/Good Fit/Moderate Fit/Poor Fit]
Score: [0-10]
Reason: [Brief explanation]
Matching Skills: [List key matching skills]
Missing Skills: [List key missing skills]
"""
            
            response = self.client.generate_content(prompt)
            parsed = self._parse_job_fit_response(response)
            
            logger.info(f"Job fit analysis complete: {parsed.get('job_fit', 'Unknown')}")
            return parsed
            
        except Exception as e:
            logger.error(f"AI job fit analysis failed: {e}")
            return self._fallback_job_fit()
    
    def generate_questions(self, experience_level: str, job_title: str,
                          resume_features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate personalized interview questions
        
        Args:
            experience_level: Candidate experience level
            job_title: Job title
            resume_features: Resume features
        
        Returns:
            List of question dictionaries
        """
        if not self.client.is_available():
            return self._fallback_questions(job_title)
        
        try:
            skills = resume_features.get('skills', [])[:10]
            
            prompt = f"""Create 5 interview questions for {job_title} position.

Candidate Profile:
- Experience Level: {experience_level}
- Key Skills: {', '.join(skills)}

Return ONLY a JSON array:
[
  {{"id": "Q1", "type": "concept", "question": "...", "reference_answer": "..."}},
  {{"id": "Q2", "type": "concept", "question": "...", "reference_answer": "..."}},
  {{"id": "Q3", "type": "code", "question": "...", "reference_answer": "..."}},
  {{"id": "Q4", "type": "concept", "question": "...", "reference_answer": "..."}},
  {{"id": "Q5", "type": "code", "question": "...", "reference_answer": "..."}}
]

Mix concept and coding questions. Make them relevant to the candidate's skills.
"""
            
            response = self.client.generate_content(prompt)
            questions = self._extract_questions_json(response)
            
            logger.info(f"Generated {len(questions)} interview questions")
            return questions
            
        except Exception as e:
            logger.error(f"AI question generation failed: {e}")
            return self._fallback_questions(job_title)
    
    def evaluate_code_answer(self, question: str, reference_answer: str,
                            student_answer: str) -> Dict[str, Any]:
        """
        Evaluate a coding answer using AI
        
        Args:
            question: Question text
            reference_answer: Reference answer
            student_answer: Student's answer
        
        Returns:
            Dictionary with score and feedback
        """
        if not self.client.is_available():
            return {"score": 5.0, "feedback": "AI evaluation unavailable"}
        
        try:
            prompt = f"""Evaluate this coding answer. Return JSON only:
{{"score": int (0-10), "feedback": "brief feedback"}}

Question: {question}
Reference: {reference_answer}
Student Answer: {student_answer}

Assess correctness, efficiency, and code quality.
"""
            
            response = self.client.generate_content(prompt)
            result = json.loads(self._clean_json_response(response))
            
            return {
                "score": float(result.get("score", 5)),
                "feedback": result.get("feedback", "No feedback available")
            }
            
        except Exception as e:
            logger.error(f"AI code evaluation failed: {e}")
            return {"score": 5.0, "feedback": f"Evaluation error: {str(e)}"}
    
    # Helper methods
    
    def _clean_json_response(self, text: str) -> str:
        """Clean Gemini response to valid JSON"""
        text = text.strip()
        text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)
        text = text.replace("'", '"')
        text = re.sub(r"//.*", "", text)
        text = re.sub(r",(\s*[}\]])", r"\1", text)
        
        if not text.strip().endswith("}") and not text.strip().endswith("]"):
            text += "}"
        
        return text
    
    def _extract_questions_json(self, text: str) -> List[Dict[str, Any]]:
        """Extract JSON array from text"""
        text = text.strip()
        text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```\s*", "", text)
        
        start = text.find('[')
        if start == -1:
            raise ValueError("No JSON array found")
        
        bracket_count = 0
        end = start
        for i, char in enumerate(text[start:], start):
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    end = i
                    break
        
        json_str = text[start:end+1]
        questions = json.loads(json_str)
        
        # Validate structure
        for i, q in enumerate(questions):
            if "id" not in q:
                q["id"] = f"Q{i+1}"
            if "type" not in q:
                q["type"] = "concept"
            if "question" not in q:
                q["question"] = "Question not generated properly"
            if "reference_answer" not in q:
                q["reference_answer"] = "Answer not provided"
        
        return questions
    
    def _parse_job_fit_response(self, text: str) -> Dict[str, Any]:
        """Parse job fit analysis response"""
        result = {
            "job_fit": "Moderate Fit",
            "fit_score": 6.0,
            "reason": "Analysis completed",
            "matching_skills": [],
            "missing_skills": []
        }
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('Fit:'):
                result['job_fit'] = line.split(':', 1)[1].strip()
            elif line.startswith('Score:'):
                try:
                    score_text = line.split(':', 1)[1].strip()
                    score = float(re.search(r'\d+\.?\d*', score_text).group())
                    result['fit_score'] = min(10.0, max(0.0, score))
                except:
                    pass
            elif line.startswith('Reason:'):
                result['reason'] = line.split(':', 1)[1].strip()
        
        return result
    
    def _fallback_parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """Fallback resume parsing"""
        lines = resume_text.split('\n')
        name = lines[0] if lines else "Unknown Candidate"
        
        common_skills = ["python", "java", "javascript", "sql", "react", "node", "aws", "docker", "git"]
        found_skills = [skill for skill in common_skills if skill in resume_text.lower()]
        
        return {
            "full_name": name,
            "email": "not_extracted@example.com",
            "phone": "not_extracted",
            "education": {"degree": "Not extracted", "major": "Not extracted", "university": "Not extracted"},
            "total_experience_years": 2.0,
            "skills": found_skills,
            "projects": ["Project details not extracted"],
            "certifications": [],
            "leadership_experience": 0,
            "has_research_work": 0
        }
    
    def _fallback_job_fit(self) -> Dict[str, Any]:
        """Fallback job fit analysis"""
        return {
            "job_fit": "Moderate Fit",
            "fit_score": 6.0,
            "reason": "AI analysis unavailable, manual review recommended",
            "matching_skills": [],
            "missing_skills": []
        }
    
    def _fallback_questions(self, job_title: str) -> List[Dict[str, Any]]:
        """Fallback question generation"""
        return [
            {
                "id": "Q1",
                "type": "concept",
                "question": f"Tell me about your experience with {job_title} and what interests you about this position?",
                "reference_answer": "Should demonstrate understanding of the role and genuine interest"
            },
            {
                "id": "Q2",
                "type": "concept",
                "question": "What programming languages and technologies are you most comfortable with?",
                "reference_answer": "Should mention relevant technologies for the role"
            },
            {
                "id": "Q3",
                "type": "code",
    
    def _fallback_experience_level(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback experience level prediction"""
        years = resume_features.get('total_experience_years', 0)
        skills_count = len(resume_features.get('skills', []))
        projects_count = len(resume_features.get('projects', []))
        
        if years >= 5 or (skills_count >= 12 and projects_count >= 5):
            level = "Senior"
        elif years >= 2 or (skills_count >= 6 and projects_count >= 2):
            level = "Mid-Level"
        else:
            level = "Junior"
        
        return {
            "experience_level": level,
            "confidence": 0.7,
            "reasoning": "Rule-based fallback prediction"
        }
    
    def _fallback_resume_score(self, resume_features: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback resume scoring"""
        years = resume_features.get('total_experience_years', 0)
        skills_count = len(resume_features.get('skills', []))
        projects_count = len(resume_features.get('projects', []))
        certs_count = len(resume_features.get('certifications', []))
        
        score = (
            min(years * 0.5, 3.0) +
            min(skills_count * 0.2, 2.5) +
            min(projects_count * 0.3, 2.0) +
            min(certs_count * 0.4, 1.5) +
            1.0
        )
        score = min(10.0, max(0.0, score))
        
        return {
            "resume_score": score,
            "breakdown": {
                "experience": min(10.0, years * 1.5),
                "skills": min(10.0, skills_count * 0.8),
                "projects": min(10.0, projects_count * 1.5),
                "certifications": min(10.0, certs_count * 2.0),
                "education": 5.0
            },
            "feedback": "Rule-based scoring applied"
        }

                "question": "Write a function to reverse a string without using built-in reverse methods.",
                "reference_answer": "Should show basic programming skills and string manipulation"
            },
            {
                "id": "Q4",
                "type": "concept",
                "question": "Describe a challenging technical problem you solved recently.",
                "reference_answer": "Should demonstrate problem-solving skills and technical depth"
            },
            {
                "id": "Q5",
                "type": "code",
                "question": "Write a function to find the maximum element in an array.",
                "reference_answer": "Should show understanding of arrays and iteration"
            }
        ]
