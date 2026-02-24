

# 🤖 Conversational RAG Assistant

A  Retrieval-Augmented Generation (RAG) system built using **FastAPI + Streamlit + FAISS + Sentence Transformers + Gemini**.

Upload a document and chat with it intelligently using semantic search and conversational memory.

---

## 🚀 Features

- 📄 Upload `.txt`, `.pdf`, `.docx` documents
- 🧠 Semantic chunking
- 🔎 Vector similarity search using FAISS
- 💬 Conversational memory (context-aware follow-ups)
- ⚡ Local embeddings (`all-MiniLM-L6-v2`)
- 🤖 Gemini LLM integration
- 🎨 Clean Streamlit Chat UI
- 🧱 Modular production-style architecture
- 🏥 Health check endpoint


## 🧠 How It Works

### 1️⃣ Document Ingestion
- File uploaded via frontend
- Text extracted
- Split into semantic chunks
- Embeddings generated locally
- Stored in FAISS index

### 2️⃣ Query Flow
- User question embedded
- Top-K similar chunks retrieved
- Conversation history injected
- Prompt sent to Gemini
- Answer returned to frontend


## 🛠️ Installation

### 1️⃣ Clone Repository

```bash
git clone <https://github.com/ranjana-kas/RAG_API>
cd mini_rag_api
````

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If no requirements file:

```bash
pip install fastapi uvicorn streamlit sentence-transformers faiss-cpu google-generativeai python-dotenv httpx pypdf python-docx
```

---

### 4️⃣ Add Environment Variables

Create `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

Get key from:
[https://ai.google.dev/](https://ai.google.dev/)

---

## ▶️ Run The Application

### Start Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

### Start Frontend

Open new terminal:

```bash
streamlit run frontend.py
```

---

## 📡 API Endpoints

### 🔹 POST /ingest

Upload document.

**Input**

* Multipart file (.txt, .pdf, .docx)

**Response**

```json
{
  "message": "Success",
  "chunks": 14
}
```

---

### 🔹 POST /query

Ask a question.

**Request**

```json
{
  "question": "What is this document about?",
  "top_k": 3,
  "stream": false,
  "session_id": "unique-id"
}
```

**Response**

```json
{
  "answer": "Generated answer...",
  "sources": ["file1.pdf"]
}
```

---

### 🔹 GET /health

```json
{ "status": "ok" }
```

---

## 🧠 Key Engineering Decisions

| Component             | Why                             |
| --------------------- | ------------------------------- |
| Sentence Transformers | Fast local embeddings           |
| FAISS                 | Efficient similarity search     |
| Gemini Flash          | Fast LLM responses              |
| Lazy Loading          | Faster startup + better scaling |
| Conversation Store    | Enables contextual follow-ups   |
| Modular Services      | Clean architecture              |

---

## ⚡ Performance

* Embedding model: ~90MB
* CPU inference supported
* Handles documents up to 1MB
* Retrieval latency < 100ms (excluding LLM)

---
