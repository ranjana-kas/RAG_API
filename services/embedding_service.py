from typing import List
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

_model = None

def get_model():
    global _model
    if _model is None:
        logger.info("Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


async def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    model = get_model()
    logger.info(f"Generating embeddings for {len(texts)} chunks")
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()


async def generate_embedding(text: str) -> List[float]:
    model = get_model()
    embedding = model.encode([text], convert_to_numpy=True)
    return embedding[0].tolist()