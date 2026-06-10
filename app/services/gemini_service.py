"""
Gemini AI Service — powers the AI interviewer conversation,
question generation, and answer evaluation.

Free tier: 1,500 requests/day, 1M tokens/minute.
Get your key at: aistudio.google.com
"""
import json
from typing import Optional
from google import genai
from google.genai import types
from app.core.config import settings


class GeminiService:
    """
    Wrapper around Google Gemini API for CareerBoost AI features.

    Used for:
    - Generating interview questions from job description + resume
    - Evaluating spoken answers with semantic understanding
    - Generating follow-up questions based on candidate responses
    - Producing overall interview feedback reports
    """

    def __init__(self):
        self._client = None
        self._initialized = False

    def _initialize(self):
        """Lazy initialization — only connects when first used."""
        if self._initialized:
            return

        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not set in .env file. "
                "Get a free key at aistudio.google.com"
            )

        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self._initialized = True

    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate text from a prompt using Gemini.
        Returns the response text or raises on failure.
        """
        self._initialize()
        try:
            response = self._client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")

    def generate_interview_questions(
        self,
        job_title: str,
        job_description: str,
        required_skills: list,
        candidate_experience: float = 0.0,
        candidate_skills: Optional[list] = None,
        num_questions: int = 5
    ) -> list:
        """
        Generate adaptive interview questions based on job + candidate.

        Returns a list of dicts with:
        - question_text
        - category (behavioral/technical/general)
        - difficulty (1-5)
        - expected_duration_seconds
        """
        candidate_skills_str = (
            ", ".join(candidate_skills)
            if candidate_skills else "Not specified"
        )
        required_skills_str = ", ".join(required_skills)

        prompt = f"""
You are an expert technical interviewer. Generate exactly {num_questions}
interview questions for the following role.

JOB TITLE: {job_title}

JOB DESCRIPTION:
{job_description[:1000]}

REQUIRED SKILLS: {required_skills_str}

CANDIDATE PROFILE:
- Years of experience: {candidate_experience}
- Known skills: {candidate_skills_str}

INSTRUCTIONS:
1. Start with easier questions (difficulty 1-2), progress to harder (3-5)
2. Mix behavioral and technical questions
3. Focus on required skills the candidate may lack
4. Questions must be answerable by speaking (no coding required)

Return ONLY a JSON array with exactly {num_questions} objects.
Each object must have these exact keys:
- "question_text": string (the full question)
- "category": string (one of: "behavioral", "technical", "general")
- "difficulty": integer (1 to 5)
- "expected_duration_seconds": integer (60 to 180)

Return ONLY the JSON array, no markdown, no explanation.
"""
        response_text = self.generate_text(
            prompt,
            temperature=0.8,
            max_tokens=2000
        )

        clean = response_text.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            clean = "\n".join(lines[1:-1])

        questions = json.loads(clean)

        validated = []
        for i, q in enumerate(questions[:num_questions]):
            validated.append({
                "question_text": str(q.get("question_text", "")),
                "category": str(q.get("category", "general")),
                "difficulty": min(5, max(1, int(q.get("difficulty", 2)))),
                "expected_duration_seconds": min(
                    180, max(60, int(q.get("expected_duration_seconds", 120)))
                ),
                "question_order": i + 1
            })

        return validated

    def evaluate_answer(
        self,
        question_text: str,
        answer_text: str,
        job_title: str,
        required_skills: list,
        web_search_context: Optional[str] = None
    ) -> dict:
        """
        Evaluate a candidate's spoken answer using Gemini.

        Uses web search context (from DuckDuckGo) to verify
        technical accuracy against current best practices.

        Returns:
        - score: int (0-100)
        - feedback: str
        - strengths: list
        - improvements: list
        """
        skills_str = ", ".join(required_skills)

        context_section = ""
        if web_search_context:
            context_section = f"""
CURRENT INDUSTRY CONTEXT (from web search):
{web_search_context[:500]}

Use this context to verify if the candidate's technical claims
are accurate and up-to-date.
"""

        prompt = f"""
You are an expert technical interviewer evaluating a candidate's spoken answer.

ROLE: {job_title}
REQUIRED SKILLS: {skills_str}

QUESTION ASKED:
{question_text}

CANDIDATE'S SPOKEN ANSWER:
{answer_text}
{context_section}

Evaluate this answer on these criteria:
1. Relevance to the question (0-25 points)
2. Technical accuracy (0-25 points)
3. Communication clarity (0-25 points)
4. Depth and examples (0-25 points)

Return ONLY a JSON object with these exact keys:
- "score": integer from 0 to 100
- "feedback": string (2-3 sentences of constructive feedback)
- "strengths": array of 1-2 short strings
- "improvements": array of 1-2 short strings

Return ONLY the JSON object, no markdown, no explanation.
"""
        response_text = self.generate_text(
            prompt,
            temperature=0.3,
            max_tokens=500
        )

        clean = response_text.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            clean = "\n".join(lines[1:-1])

        result = json.loads(clean)

        return {
            "score": min(100, max(0, int(result.get("score", 50)))),
            "feedback": str(result.get("feedback", "Answer evaluated.")),
            "strengths": result.get("strengths", []),
            "improvements": result.get("improvements", [])
        }

    def generate_follow_up_question(
        self,
        original_question: str,
        candidate_answer: str,
        job_title: str
    ) -> Optional[str]:
        """
        Generate a follow-up question based on candidate's answer.
        Used for the conversational interview flow.
        """
        prompt = f"""
You are an interviewer for a {job_title} role.

You asked: "{original_question}"

The candidate answered: "{candidate_answer[:500]}"

Generate ONE natural follow-up question that:
- Digs deeper into what they said
- Is conversational and encouraging
- Can be answered by speaking (no coding)
- Is 1-2 sentences maximum

Return ONLY the follow-up question, nothing else.
"""
        return self.generate_text(prompt, temperature=0.7, max_tokens=100)

    def generate_interview_report(
        self,
        job_title: str,
        questions_and_answers: list,
        overall_score: int
    ) -> str:
        """Generate a comprehensive interview feedback report."""
        qa_text = ""
        for i, qa in enumerate(questions_and_answers, 1):
            qa_text += (
                f"\nQ{i}: {qa.get('question', '')}\n"
                f"Answer: {qa.get('answer', '')[:300]}\n"
                f"Score: {qa.get('score', 0)}/100\n"
            )

        prompt = f"""
You are an expert recruiter writing an interview assessment report.

ROLE: {job_title}
OVERALL SCORE: {overall_score}/100

INTERVIEW TRANSCRIPT:
{qa_text}

Write a professional 3-4 sentence assessment that:
1. States the overall performance level
2. Highlights the strongest area
3. Identifies the main area for improvement
4. Gives a clear hiring recommendation

Return ONLY the assessment paragraph, no headings, no bullet points.
"""
        return self.generate_text(prompt, temperature=0.4, max_tokens=300)

    def is_available(self) -> bool:
        """Check if Gemini API is configured and available."""
        return bool(settings.GEMINI_API_KEY)


# Singleton instance
gemini_service = GeminiService()
