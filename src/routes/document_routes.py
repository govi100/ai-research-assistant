import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from pypdf import PdfReader
from src.services.vector_store import add_chunks_to_vector_store, collection
from src.services.classifier import classify_document  # 1. Import the classifier

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "./data/uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    extracted_text = ""
    
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            extracted_text = f.read()

    # 2. Determine the category of the extracted text
    document_category = classify_document(extracted_text)

    # Chunk text & store in ChromaDB
    chunks = chunk_text(extracted_text)
    add_chunks_to_vector_store(file.filename, chunks)
    
    # 3. Include "category" in the returned response!
    return {
        "filename": file.filename,
        "category": document_category,  # <-- Added attribute
        "total_pages": len(reader.pages) if file.filename.endswith(".pdf") else 1,
        "total_chunks": len(chunks),
        "status": "Document successfully processed and categorized!",
        "sample_chunk": chunks[0] if chunks else "No readable text found."
    }

@router.get("/")
async def list_documents():
    files = os.listdir(UPLOAD_DIR) if os.path.exists(UPLOAD_DIR) else []
    return {"uploaded_files": files}

@router.delete("/clear")
async def clear_database():
    existing_ids = collection.get()["ids"]
    if existing_ids:
        collection.delete(ids=existing_ids)
    return {"status": "Vector database successfully cleared!"}