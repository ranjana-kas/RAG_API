import faiss
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class FAISSStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.chunk_data = {}
        self._current_id = 0

    def add_chunks(self, texts: List[str], embeddings: List[List[float]], filename: str):
        if not embeddings:
            return

        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)

        for text in texts:
            self.chunk_data[self._current_id] = {
                "text": text,
                "source": filename
            }
            self._current_id += 1

        logger.info(f"Added {len(texts)} chunks to FAISS")

    def search(self, query_embedding: List[float], top_k: int):
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx in self.chunk_data:
                chunk = self.chunk_data[idx]
                results.append({
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "score": float(dist)
                })

        return results


vector_store = FAISSStore()