import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from schemas.query import QueryRequest, QueryResponse
from services.chunker import chunk_text
from services.embedding_service import generate_embeddings_batch
from services.retrieval_service import retrieve_top_k
from services.llm_service import generate_answer_sync, generate_answer_stream
from storage.faiss_store import vector_store
from utils.file_parser import extract_text_from_file
from storage.conversation_store import conversation_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Advanced RAG API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".txt", ".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    content = await file.read()

    text = await extract_text_from_file(content, file.filename)

    chunks = chunk_text(text)
    embeddings = await generate_embeddings_batch(chunks)

    vector_store.add_chunks(chunks, embeddings, file.filename)

    return {"message": "Success", "chunks": len(chunks)}


@app.post("/query")
async def query_document(request: QueryRequest):

    if vector_store._current_id == 0:
        raise HTTPException(status_code=400, detail="Ingest document first")

    top_chunks = await retrieve_top_k(request.question, request.top_k)
    context_texts = [chunk["text"] for chunk in top_chunks]

  
    history = conversation_store.get_history(request.session_id)

    answer = await generate_answer_sync(
        request.question,
        context_texts,
        history
    )

    # store conversation
    conversation_store.add_message(request.session_id, "user", request.question)
    conversation_store.add_message(request.session_id, "assistant", answer)

    sources = list(set([chunk["source"] for chunk in top_chunks]))

    return QueryResponse(answer=answer, sources=sources)