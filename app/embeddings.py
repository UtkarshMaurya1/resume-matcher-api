from .config import settings
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-mpnet-base-v2')

def generate_embeddings(text: str) -> list[float]:
    
    try:
        return embedding_model.encode(text).tolist()
    
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

