import os, json, re
from typing import Dict
from groq import Groq
from .config import settings

# Initialize Groq clients
client = Groq(api_key=settings.LLM_API_KEY)

Prompt = """
You are an assistant that compares a candidate resume with the job description.
Strictly return a valid JSON with these keys:
- semantic_score: float (0-1) cosine/semantic similarity estimate
- match_percentage: float (0-100)
- missing_skills: list of strings
- explanation: short text (why matched or not)

Job Description:
{jd_text}

Resume:
{resume_text}

Instructions:
1) Focus on skill match, years of experience statements, and keywords.
2) Provide missing_skills that are explicitly required by JD but not present in resume.
3) Provide match_percentage (0-100).
4) Return ONLY a JSON. No extra text.
"""

def call_llm_score(jd_text: str, resume_text: str) -> Dict:
    prompt = Prompt.format(jd_text=jd_text, resume_text=resume_text)

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful AI for resume-job matching."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=400,
        )

        content = response.choices[0].message.content.strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                result = json.loads(match.group(0))
            else:
                result = {
                    "semantic_score": 0.0,
                    "match_percentage": 0.0,
                    "missing_skills": [],
                    "explanation": "LLM response not in JSON format.",
                }

        return result

    except Exception as e:
        return {
            "semantic_score": 0.0,
            "match_percentage": 0.0,
            "missing_skills": [],
            "explanation": f"Error calling Groq API: {str(e)}",
        }
