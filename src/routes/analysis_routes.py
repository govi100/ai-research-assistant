from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.llm_service import generate_rag_answer

router = APIRouter(prefix="/analysis", tags=["Analysis"])

class QueryRequest(BaseModel):
    query: str

class SummaryRequest(BaseModel):
    document_name: str

# 1. Added schema for comparison request
class CompareRequest(BaseModel):
    query: str
    doc_1: str
    doc_2: str

@router.post("/ask")
async def ask_question(request: QueryRequest):
    """RAG Endpoint: Answers questions using ChromaDB context."""
    try:
        answer = generate_rag_answer(request.query)
        return {"query": request.query, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
async def summarize_document(request: SummaryRequest):
    """Generates an executive summary of a specific document."""
    query = f"Provide a comprehensive executive summary of {request.document_name} covering key highlights."
    try:
        summary = generate_rag_answer(query)
        return {"document": request.document_name, "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Added new /compare endpoint
@router.post("/compare")
async def compare_documents(request: CompareRequest):
    """Compares two uploaded documents based on a specific prompt."""
    prompt = (
        f"Compare and contrast the content of '{request.doc_1}' and '{request.doc_2}' "
        f"specifically regarding this request: {request.query}"
    )
    try:
        comparison_result = generate_rag_answer(prompt)
        return {
            "query": request.query,
            "document_1": request.doc_1,
            "document_2": request.doc_2,
            "comparison": comparison_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))