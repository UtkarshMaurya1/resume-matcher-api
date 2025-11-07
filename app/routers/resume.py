from fastapi import APIRouter, UploadFile, Depends, File
from sqlalchemy.orm import Session
import os
from ..db import SessionLocal
from ..resume_parser import parse_resume
from ..crud import create_resume

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/upload')
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs("temp_uploads", exist_ok=True)
    file_location = f"temp_uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    text = parse_resume(file_location)
    skills = []
    r = create_resume(db, filename=file.filename, raw_text=text, skills=skills)
    return {'resume_id': r.id, 'filename': r.filename}