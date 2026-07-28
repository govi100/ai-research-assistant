from typing import Any, Dict, List
import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB client (stores vectors on disk under ./chroma_db)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Use Chroma's default ONNX embedding model (uses under 100MB RAM, no PyTorch required)
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="research_documents", embedding_function=default_ef
)


def add_chunks_to_vector_store(doc_name: str, chunks: List[str]):
  """Embeds text chunks and saves them into ChromaDB."""
  if not chunks:
    return

  ids = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
  metadatas = [
      {"source": doc_name, "chunk_index": i} for i in range(len(chunks))
  ]

  # Chroma automatically embeds the documents using default_ef
  collection.add(documents=chunks, metadatas=metadatas, ids=ids)


def query_vector_store(query_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
  """Searches ChromaDB for top matching document chunks."""
  # Querying by text directly uses default_ef under the hood
  results = collection.query(query_texts=[query_text], n_results=n_results)

  output = []
  if results and "documents" in results and results["documents"]:
    docs = results["documents"][0]
    metas = (
        results["metadatas"][0]
        if ("metadatas" in results and results["metadatas"])
        else []
    )
    for doc, meta in zip(docs, metas):
      output.append({"text": doc, "metadata": meta})

  return output