from app.services.chunker import chunk_text
from app.services.embedding_service import embed_and_store

def ingest_text_to_rag(text: str, source_id: str, metadata: dict):
    chunks = chunk_text(text)
    embed_and_store(chunks, source_id=source_id, metadata=metadata)
    print(f"Ingested {len(chunks)} chunks for source {source_id}")
