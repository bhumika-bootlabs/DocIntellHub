
from app.services.embedding_service import chunk_text, embed_and_store, retrieve_top_k
from app.services.evaluation_service import evaluate_response

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

    # 🔍 Retrieval
    chunks = vector_store.search(question)[:5]

    contexts = [c for c in contexts if isinstance(c, str) and c.strip()]

    for chunk in chunks:
        if isinstance(chunk, str):
            contexts.append(chunk)

        elif isinstance(chunk, dict):
            # Weaviate-like response
            if "properties" in chunk:
                contexts.append(chunk["properties"].get("text", ""))
            else:
                contexts.append(chunk.get("text", ""))

        elif hasattr(chunk, "properties"):
            contexts.append(chunk.properties.get("text", ""))

        else:
            print("UNKNOWN CHUNK TYPE:", type(chunk))

    context = "\n\n".join(contexts)

    # 🧠 LLM
    prompt = get_prompt(mode, context, question)
    answer = call_llm(prompt)

    # 📊 Evaluation
    from app.services.evaluation_service import evaluate_response
    scores = evaluate_response(question, answer, contexts)

    return {
        "mode": mode,
        "answer": answer,
        "evaluation": scores
    }