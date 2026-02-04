# import faiss
# import numpy as np

# class VectorStore:
#     def __init__(self, dim: int):
#         self.index = faiss.IndexFlatL2(dim)
#         self.text_chunks = []

#     def add(self, embeddings, chunks):
#         self.index.add(embeddings)
#         self.text_chunks.extend(chunks)

#     def search(self, query_embedding, k=5):
#         if self.index is None or len(self.text_chunks) == 0:
#             return []

#         distances, indices = self.index.search(query_embedding, k)

#         results = []
#         for i in indices[0]:
#             if 0 <= i < len(self.text_chunks):
#                 results.append(self.text_chunks[i])

#         return results


#     def build_index(self, texts):
#         from app.services.embedding_service import chunk_text, embed_and_store, retrieve_top_k
#         import numpy as np
#         import faiss

#         embeddings = embed_text(texts)

#         self.index = faiss.IndexFlatL2(embeddings.shape[1])
#         self.index.add(embeddings)
#         self.text_chunks = texts


# vector_store = VectorStore(dim=384)

