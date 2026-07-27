from fastapi import FastAPI
from src.routes.document_routes import router as document_router
from src.routes.search_routes import router as search_router
from src.routes.analysis_routes import router as analysis_router

app = FastAPI(
    title="AI Research Assistant",
    description="API for document uploading, chunking, vector search, and LLM analysis."
)

# Connect all routes
app.include_router(document_router)
app.include_router(search_router)
app.include_router(analysis_router)

@app.get("/")
def read_root():
    return {"message": "AI Research Assistant API is running!"}