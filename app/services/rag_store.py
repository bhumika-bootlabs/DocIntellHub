# from app.services.vector_store import VectorStore
# from app.services.embedding_service import chunk_text, embed_and_store, retrieve_top_k

# Init store once
# vector_store = VectorStore(dim=384)  # all-MiniLM-L6-v2 = 384 dims

# def store_chunks(chunks: list[str]):
#     embeddings = embed_text(chunks)
#     # vector_store.add(embeddings, chunks)

# def retrieve_chunks(query: str, k=5):
#     query_emb = embed_text([query])[0]
    # return vector_store.search(query_emb, k)
