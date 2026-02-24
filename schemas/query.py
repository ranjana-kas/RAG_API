from pydantic import BaseModel, Field
from typing import List

class QueryRequest(BaseModel):
    question: str = Field(...)
    top_k: int = Field(default=3)
    stream: bool = Field(default=False)
    session_id: str = Field(..., description="Unique session id")

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]