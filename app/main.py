from fastapi import FastAPI
from app.db import Base, engine
from app.routers import resume, jobs, match

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Resume Matcher")
app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(match.router)


@app.get("/")
def root():
    return {"message": "working"}

