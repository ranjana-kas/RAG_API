import streamlit as st
import httpx
import uuid

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Conversational RAG", page_icon="🤖", layout="centered")

# -------- SESSION --------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "current_file" not in st.session_state:
    st.session_state.current_file = None


# =========================================
# HEADER
# =========================================
st.title("🤖 Conversational RAG Assistant")
st.caption("Upload a document and chat with it intelligently")

st.divider()


# =========================================
# 📄 DOCUMENT UPLOAD SECTION (MAIN AREA)
# =========================================
st.subheader("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a file (PDF, DOCX, TXT)",
    type=["txt", "pdf", "docx"]
)

col1, col2 = st.columns([1,1])

with col1:
    if st.button("🚀 Process Document", use_container_width=True):
        if uploaded_file is None:
            st.warning("Please upload a file first")
        else:
            with st.spinner("Indexing document..."):
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                }

                try:
                    with httpx.Client(timeout=60.0) as client:
                        response = client.post(f"{API_URL}/ingest", files=files)

                    if response.is_success:
                        st.session_state.document_uploaded = True
                        st.session_state.current_file = uploaded_file.name
                        st.success("Document processed successfully!")
                        st.session_state.messages = []
                    else:
                        st.error(response.text)

                except Exception as e:
                    st.error(f"Backend connection error: {e}")


with col2:
    if st.session_state.document_uploaded:
        if st.button("🗑 Upload Another Document", use_container_width=True):
            st.session_state.document_uploaded = False
            st.session_state.messages = []
            st.session_state.current_file = None
            st.rerun()


# =========================================
# STATUS BAR
# =========================================
if st.session_state.document_uploaded:
    st.success(f"✅ Active document: {st.session_state.current_file}")
else:
    st.info("No document loaded")

st.divider()


# =========================================
# 💬 CHAT SECTION
# =========================================
st.subheader("💬 Chat With Your Document")

if not st.session_state.document_uploaded:
    st.warning("Upload and process a document first.")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------- CHAT INPUT --------
if prompt := st.chat_input("Ask anything about your document..."):

    # show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    payload = {
        "question": prompt,
        "top_k": 3,
        "stream": False,
        "session_id": st.session_state.session_id,
    }

    # assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                with httpx.Client(timeout=60.0) as client:
                    response = client.post(f"{API_URL}/query", json=payload)

                if response.is_success:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])

                    st.markdown(answer)

                    # show sources nicely
                    if sources:
                        with st.expander("📚 Sources"):
                            for s in sources:
                                st.write(f"- {s}")

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                else:
                    st.error(response.text)

            except Exception as e:
                st.error(f"Connection error: {e}")