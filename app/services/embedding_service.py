from sentence_transformers import SentenceTransformer
import numpy as np
from app.core.weaviate_client import client
from weaviate.classes.query import Filter

schema = {
    "class": "DocumentChunk",
    "vectorizer": "none",
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {"name": "source_id", "dataType": ["text"]},
        {"name": "domain", "dataType": ["text"]}
    ]
}

def create_schema():
    if not client.schema.contains(schema):
        client.schema.create_class(schema)

model = SentenceTransformer("all-MiniLM-L6-v2")

# VECTOR_STORE = []

def chunk_text(text: str, chunk_size=500, overlap=50) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
    return chunks

def embed_and_store(chunks: list[str], source_id: str, metadata: dict):
    embeddings = model.encode(chunks, convert_to_numpy=True)

    collection = client.collections.get("DocumentChunk")

    for chunk, vector in zip(chunks, embeddings):
        collection.data.insert(
            properties={
                "text": chunk,
                "source_id": source_id,
                "domain": metadata["domain"]
            },
            vector=vector.tolist()
        )

    print("Stored chunk with metadata:", metadata)

# def retrieve_top_k(query: str, domain:str, k: int = 4):
    
#     query_vec = model.encode([query], convert_to_numpy=True)[0]

    # def cosine_sim(a, b):
    #     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # scored = []
    # for item in VECTOR_STORE:
    #     score = cosine_sim(query_vec, item["embedding"])
    #     scored.append((score, item))

    # scored.sort(reverse=True, key=lambda x: x[0])
    # results = [item["text"] for _, item in scored[:k]]

    # for item in VECTOR_STORE:

    #     # 🔒 Domain filter
    #     if item["metadata"]["domain"] != domain:
    #         continue

    #     score = cosine_sim(query_vec, item["embedding"])
    #     scored.append((score, item))

    # scored.sort(reverse=True, key=lambda x: x[0])

    # results = [item["text"] for _, item in scored[:k]]



def retrieve_top_k(query: str, domain: str, k: int = 4):

    query_vec = model.encode([query], convert_to_numpy=True)[0]
    print("Filtering for domain:", domain)

    # Access collection
    collection = client.collections.get("DocumentChunk")

    # Query with vector similarity + filter
    response = collection.query.near_vector(
    near_vector=query_vec.tolist(),
    limit=k,
    filters=Filter.by_property("domain").equal(domain)
    )

    # Extract results
    results = [
        obj.properties["text"]
        for obj in response.objects
    ]

    print("\n--- RAG Retrieved Chunks ---")
    for i, r in enumerate(results, 1):
        print(f"\nChunk {i}:\n{r[:300]}")
    print("----------------------------")

    return results