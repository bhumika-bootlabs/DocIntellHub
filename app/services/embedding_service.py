from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_STORE = []

def chunk_text(text: str, chunk_size=500, overlap=50) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
    return chunks

def embed_and_store(chunks: list[str], source_id: str, metadata: dict):
    embeddings = model.encode(chunks, convert_to_numpy=True)
    for chunk, vector in zip(chunks, embeddings):
        VECTOR_STORE.append({
            "text": chunk,
            "embedding": vector,
            "source_id": source_id,
            "metadata": metadata
        })

def retrieve_top_k(query: str, k: int = 4):
    print("VECTOR_STORE size:", len(VECTOR_STORE))
    query_vec = model.encode([query], convert_to_numpy=True)[0]

    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    scored = []
    for item in VECTOR_STORE:
        score = cosine_sim(query_vec, item["embedding"])
        scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])
    results = [item["text"] for _, item in scored[:k]]

    print("\n--- RAG Retrieved Chunks ---")
    for i, r in enumerate(results, 1):
        print(f"\nChunk {i}:\n{r[:300]}")
    print("----------------------------")

    return results
