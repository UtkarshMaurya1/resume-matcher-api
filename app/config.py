from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    VECTOR_COLLECTION: str = "resumes"
    LLM_API_URL: str = "https://api.groq.com/openai/v1"
    LLM_API_KEY: str | None = os.getenv('LLM_API_KEY')
    EMBEDDING_DIM: int = 768

    class Config:
        env_file = '.env'
        env_file_encoding = "utf-8"

settings = Settings()
print("LLM API Key loaded:", "Yes" if settings.LLM_API_KEY else "No")
print("DATABASE_URL loaded:", "Yes" if settings.DATABASE_URL else "No")