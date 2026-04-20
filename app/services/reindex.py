# from sqlalchemy.orm import Session
# from app.api.utility.db import SessionLocal
# from app.models.extracted_text import ExtractedText
# from app.services.embedding_service import chunk_text, embed_and_store, retrieve_top_k
# # from app.services.vector_store import vector_store


# def rebuild_index():
#     db: Session = SessionLocal()

#     records = db.query(ExtractedText).all()

#     texts = [r.content for r in records]

#     if texts:
#         vector_store.build_index(texts)

#     db.close()
from app.api.utility.db import SessionLocal
from app.models.extracted_text import ExtractedText
from app.services.embedding_service import chunk_text, embed_and_store


def rebuild_index():
    db = SessionLocal()
    try:
        # 1. Clear existing in-memory vector store
        # VECTOR_STORE.clear()

        # 2. Fetch all extracted text (PDF + audio)
        records = db.query(ExtractedText).all()

        if not records:
            print("Reindex skipped: no extracted text found")
            return

        # 3. Re-chunk, re-embed, re-store
        for record in records:
            chunks = chunk_text(record.content)
            embed_and_store(
                chunks=chunks,
                source_id=str(record.document_id),
                metadata={"document_id": record.document_id}
            )

        print(f"Reindexed VECTOR_STORE with {len(VECTOR_STORE)} chunks")

    finally:
        db.close()
