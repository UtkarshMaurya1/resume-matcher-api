# app/vector_client.py
from typing import List
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(path="./chroma_data")

def upsert_vector(vector_id: str, vector: list, payload: dict = None, collection_name: str = "resumes"):
    collection = client.get_or_create_collection(name=collection_name)
    print(f"[Chroma] Adding vector {vector_id} to collection '{collection_name}' with metadata {payload}")
    collection.add(
        ids=[str(vector_id)],
        embeddings=[vector],
        metadatas=[payload or {}]
    )

def search_vector(query_embedding: List[float], top_k: int = 10, collection_name: str = "resumes"):
    collection = client.get_or_create_collection(name=collection_name)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    print('🔍 Chroma raw search result =>', results)

    formatted = []
    if results["ids"] and len(results["ids"][0]) > 0:
        for i in range(len(results["ids"][0])):
            formatted.append({
                "id": results["ids"][0][i],
                "metadata": results["metadatas"][0][i],
                "document": results["documents"][0][i],
                "distance": results["distances"][0][i],
            })
    else:
        print("⚠️ No matching results found in ChromaDB")

    print('✅ Formatted result =>', formatted)
    return formatted
