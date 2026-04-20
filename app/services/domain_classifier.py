# def detect_domain(text: str) -> str:
#     text = text.lower()

#     legal_keywords = [
#         "contract", "agreement", "clause", "party",
#         "liability", "jurisdiction", "law"
#     ]

#     finance_keywords = [
#         "invoice", "tax", "revenue", "balance",
#         "profit", "loss", "financial"
#     ]

#     medical_keywords = [
#         "patient", "diagnosis", "treatment",
#         "hospital", "prescription"
#     ]

#     if any(word in text for word in legal_keywords):
#         return "legal"

#     if any(word in text for word in finance_keywords):
#         return "finance"

#     if any(word in text for word in medical_keywords):
#         return "medical"

#     return None
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detect_domain(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Classify this document as: legal, medical, or finance. Only return one word."
            },
            {
                "role": "user",
                "content": text[:1000]
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip().lower()