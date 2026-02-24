import io
from pypdf import PdfReader
import docx  # The modern library for handling Word documents

async def extract_text_from_file(file_content: bytes, filename: str) -> str:
    if filename.endswith(".pdf"):
        # Load PDF bytes directly into memory
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
        
    elif filename.endswith(".docx"):
        # Load Word document bytes directly into memory
        doc = docx.Document(io.BytesIO(file_content))
        # Join all paragraphs with a newline character
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
        
    else:
        # Standard fallback for .txt files
        # We use strict UTF-8 decoding for safety
        return file_content.decode("utf-8")