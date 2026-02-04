
from app.services.embedding_service import chunk_text, embed_and_store, retrieve_top_k

from pydantic import BaseModel

class Question(BaseModel):
    question: str

@router.post("/ask")
def ask_rag(question: str):
    context_chunks = retrieve_top_k(question, k=4)
    answer = generate_answer(context_chunks, question)
    return {"answer": answer}

