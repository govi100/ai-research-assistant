# AI Research Assistant API

An end-to-end FastAPI backend for document uploading, semantic chunking, vector indexing in ChromaDB, document categorization, and RAG Q&A / Summarization / Comparison powered by Google Gemini.

## Features
- **Document Management:** PDF/TXT parsing, chunking, and auto-categorization.
- **Vector Search:** Embeddings stored and queried via ChromaDB (`GET /search/`).
- **RAG Analysis:** Grounded Q&A (`/analysis/ask`), Document Summarization (`/analysis/summarize`), and Document Comparison (`/analysis/compare`).

## Setup Instructions

1. **Activate Virtual Environment:**
   ```bash
   source venv/bin/activate