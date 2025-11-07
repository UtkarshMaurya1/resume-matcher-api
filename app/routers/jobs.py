from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..crud import create_job

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create')
async def create_resume(title: str = Body(...), raw_text = Body(...), db: Session = Depends(get_db)):

    j = create_job(db, title=title, raw_text=raw_text, skills={})
    return {"jd_id": j.id}
