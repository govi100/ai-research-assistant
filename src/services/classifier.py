def classify_document(text: str) -> str:
    """
    Classifies a document based on text content.
    """
    text_lower = text.lower()
    
    if "education" in text_lower or "experience" in text_lower or "skills" in text_lower:
        return "Resume / CV"
    elif "abstract" in text_lower or "methodology" in text_lower or "references" in text_lower:
        return "Research Paper"
    elif "revenue" in text_lower or "valuation" in text_lower or "financial" in text_lower:
        return "Financial Report"
    else:
        return "General Document"