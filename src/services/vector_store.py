import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# Initialize ChromaDB client (stores vectors on disk under ./chroma_db)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="research_documents")

# Load lightweight embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def add_chunks_to_vector_store(doc_name: str, chunks: List[str]):
    """Embeds text chunks and saves them into ChromaDB."""
    if not chunks:
        return
    
    embeddings = embedding_model.encode(chunks).tolist()
    ids = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": doc_name, "chunk_index": i} for i in range(len(chunks))]
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_vector_store(query_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """Searches ChromaDB for top matching document chunks."""
    query_embedding = embedding_model.encode([query_text]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    output = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if "metadatas" in results else []
        for doc, meta in zip(docs, metas):
            output.append({"text": doc, "metadata": meta})
            
    return output