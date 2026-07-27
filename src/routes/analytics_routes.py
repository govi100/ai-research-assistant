from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/metrics")
async def get_metrics():
    """
    Get system usage and analytics metrics.
    """
    return {
        "total_documents": 2,
        "total_queries": 15,
        "system_status": "Healthy"
    }