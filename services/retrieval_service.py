from typing import List, Dict, Any
from storage.faiss_store import vector_store
from services.embedding_service import generate_embedding

async def retrieve_top_k(query: str, top_k: int) -> List[Dict[str, Any]]:
    query_embedding = await generate_embedding(query)
    # FAISS handles the math instantly
    return vector_store.search(query_embedding, top_k)