from sqlalchemy import Integer, Column, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False) 

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    raw_text = Column(Text, nullable=True)
    skills = Column(JSON, nullable=True)
    embedding_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    skills = Column(JSON, nullable=True)
    embedding_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

class MatchResult(Base):
    __tablename__ = "match_results"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    semantic_score = Column(Float)
    match_percentage = Column(Float)
    missing_skills = Column(JSON)
    explanation = Column(Text, nullable=True)
    analyzed_at = Column(DateTime, default=lambda: datetime.now(UTC))

    jd = relationship("JobDescription")
    resume = relationship("Resume")
