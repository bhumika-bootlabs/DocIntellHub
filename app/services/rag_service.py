from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an AI assistant for document analysis.

Answer the user's question using ONLY the provided context.
If the answer is not present in the context, say:
"I could not find this information in the uploaded documents."
"""

def generate_answer(context_chunks: list[str], question: str) -> str:
    context = "\n\n".join(context_chunks)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}
"""
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

