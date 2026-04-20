import os
from sqlalchemy.orm import Session
from app.models.documents import Document
from app.common_utils.file_handler import save_file
from app.services.rag_ingest import ingest_text_to_rag
from app.services.ocr_service import extract_from_pdf
from app.services.audio_service import transcribe_audio_file


def upload_document(db: Session, file, owner_id: int):

    filename, path = save_file(file)

    doc = Document(
        filename=filename,
        file_path=path,
        owner_id=owner_id
    )
 
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Detect file extension
    ext = os.path.splitext(filename)[1].lower()

    text = ""

    # TXT processing
    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    # PDF processing
    elif ext == ".pdf":
        text = extract_text_from_pdf(path)

    # Audio processing
    elif ext in [".mp3", ".wav", ".m4a"]:
        text = transcribe_audio(path)

    else:
        raise ValueError("Unsupported file type")

    # Send extracted text to RAG
    ingest_text_to_rag(
        text=text,
        source_id=str(doc.id),
        metadata={
            "owner_id": owner_id,
            "filename": filename
        }
    )

    return doc