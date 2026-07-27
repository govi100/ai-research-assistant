import os
from google import genai
from src.services.vector_store import query_vector_store

# Set your API key in environment or load from a .env file
# os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"

def generate_rag_answer(user_query: str) -> str:
    """Retrieves relevant chunks from ChromaDB and uses an LLM to answer the query."""
    # 1. Fetch relevant context from ChromaDB
    search_results = query_vector_store(user_query, n_results=3)
    
    if not search_results:
        return "No relevant context found in the uploaded documents."

    # 2. Combine chunks into a single context string
    context = "\n\n".join([item["text"] for item in search_results])

    # 3. Build a grounded prompt
    prompt = f"""
You are a helpful research assistant. Answer the user's question accurately using ONLY the provided context below.
If the answer cannot be determined from the context, state that clearly.

--- CONTEXT ---
{context}

--- QUESTION ---
{user_query}

--- ANSWER ---
"""

    # 4. Call the LLM
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text