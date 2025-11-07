from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from app import models, crud, vector_client, embeddings, llm_scorer

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/run/{jd_id}")
def run_match(jd_id: int, top_k: int = 50, db: Session = Depends(get_db)):
    jd = db.get(models.JobDescription, jd_id)
    if not jd:
        raise HTTPException(status_code=404, detail="JD not found")
    
    jd_emb = embeddings.generate_embeddings(jd.raw_text)

    print('emb ka size=> ', len(jd_emb))
    hits = vector_client.search_vector(jd_emb, top_k)
    print('hits==>>', hits)

    results = [] 

    for h in hits:
        payload = h.get('metadata', {})
        resume_id = payload.get('resume_id')
        if not resume_id:
            continue
        
        resume = db.get(models.Resume, resume_id)
        if not resume:
            continue

        # llm score calls
        llm_out = llm_scorer.call_llm_score(jd.raw_text, resume.raw_text)
        semantic = float(llm_out.get("semantic_score", 0.0))
        match_pct = float(llm_out.get("match_percentage", 0.0))
        missing = llm_out.get("missing_skills", [])
        explanation = llm_out.get("explanation", "")
        m = crud.save_match(db, jd_id=jd.id, resume_id=resume.id, semantic_score=semantic, match_percentage=match_pct, missing_skills=missing, explanation=explanation)
        results.append({
            "resume_id": resume.id,
            "filename": resume.filename,
            "semantic_score": semantic,
            "match_percentage": match_pct,
            "missing_skills": missing,
            "explanation": explanation
        })
    

    results = sorted(results, key=lambda x: x["match_percentage"], reverse=True)
    return {"jd_id": jd_id, "results": results}
