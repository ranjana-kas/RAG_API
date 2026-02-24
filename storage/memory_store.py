from typing import List
from schemas.ingest import Chunk

class MemoryStore:
    def __init__(self):
        self.chunks: List[Chunk] = []
        self._current_id: int = 0

    def add_chunk(self, text: str, embedding: List[float]) -> Chunk:
        self._current_id += 1
        chunk = Chunk(id=self._current_id, text=text, embedding=embedding)
        self.chunks.append(chunk)
        return chunk

    def get_all_chunks(self) -> List[Chunk]:
        return self.chunks

# We initialize a single instance to act as our database
vector_store = MemoryStore()