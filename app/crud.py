from sqlalchemy.orm import Session
import uuid
from . import models, schemas
from .embeddings import generate_embeddings
from .vector_client import upsert_vector
from .config import settings

def create_resume(db: Session, filename: str, raw_text: str, skills: dict | None = None):
    r = models.Resume(filename=filename, raw_text=raw_text, skills=skills or {})
    db.add(r)
    db.commit()
    db.refresh(r)

    emb = generate_embeddings(raw_text)
    vector_id = f"Resume_{r.id}"
    
    upsert_vector(vector_id, emb, payload={"resume_id": r.id})
    r.embedding_id = vector_id
    db.commit()
    db.refresh(r)
    return r

def create_job(db: Session, title: str, raw_text: str, skills: dict | None = None):
    j = models.JobDescription(title=title, raw_text=raw_text, skills=skills or {})
    db.add(j)
    db.commit()
    db.refresh(j)

    emb = generate_embeddings(raw_text)
    vector_id = f"JD_{j.id}"
    
    upsert_vector(vector_id, emb, payload={"job_id": j.id})
    j.embedding_id = vector_id
    db.commit()
    db.refresh(j)
    return j

def save_match(db: Session, jd_id: int, resume_id: int, semantic_score: float, match_percentage: float, missing_skills: list, explanation: str):
    m = models.MatchResult(jd_id=jd_id, resume_id=resume_id, semantic_score=semantic_score, match_percentage=match_percentage, missing_skills=missing_skills, explanation=explanation)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m