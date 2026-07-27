from fastapi import APIRouter, Query
from src.services.vector_store import query_vector_store

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
async def search_documents(q: str = Query(..., description="Semantic search query")):
    """Perform a vector similarity search across all indexed document chunks."""
    results = query_vector_store(q, n_results=3)
    return {
        "query": q,
        "total_results": len(results),
        "results": results
    }