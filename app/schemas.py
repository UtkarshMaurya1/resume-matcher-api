# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class ResumeBase(BaseModel):
    candidate_name: str
    resume_text: str
    experience_years: Optional[int]
    skills: Optional[List[str]]

class ResumeResponse(ResumeBase):
    id: int
    class Config:
        from_attributes = True  # allows SQLAlchemy → Pydantic conversion



# ---------- Job Description Schemas ----------
class JobDescriptionBase(BaseModel):
    job_title: str
    jd_text: str
    required_skills: Optional[List[str]]

class JobDescriptionResponse(JobDescriptionBase):
    id: int
    class Config:
        from_attributes = True



# ---------- Matching Schemas ----------
class MatchRequest(BaseModel):
    job_id: int
    resume_ids: Optional[List[int]] = None

class MatchResult(BaseModel):
    resume_id: int
    candidate_name: str
    semantic_score: float
    match_percentage: float
    missing_skills: Optional[List[str]] = None

class JDMatchResponse(BaseModel):
    job_id: int
    job_title: str
    results: List[MatchResult]
