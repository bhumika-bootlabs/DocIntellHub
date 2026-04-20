
from app.services.embedding_service import chunk_text, embed_and_store, retrieve_top_k

from pydantic import BaseModel

class Question(BaseModel):
    question: str

# @router.post("/ask")
# def ask_rag(question: str):
#     context_chunks = retrieve_top_k(question, k=4)
#     answer = generate_answer(context_chunks, question)
#     return {"answer": answer}

@router.post("/rag/ask") 
def ask_question(
    question: str,
    mode: str,
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()
    allowed = ROLE_MODE_MAP.get(current_user.role, [])
    if mode not in allowed:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to use this mode"
        )

    
    chunks = vector_store.search(question)

    context = "\n\n".join(chunks)

    prompt = get_prompt(mode, context, question)

    answer = call_llm(prompt)

    return {
        "mode": mode, 
        "answer": answer
    }
