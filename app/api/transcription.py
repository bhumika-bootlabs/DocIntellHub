from fastapi import APIRouter, UploadFile, File, Depends
from app.core.security import require_roles
from app.core.roles import ADMIN, LAWYER, DOCTOR, RESEARCHER, FINANCE, BUSINESS
from app.services.audio_service import transcribe_audio_file
from app.services.summarization import effective_extractive_summary
from app.services.rag_ingest import ingest_text_to_rag
import os

router = APIRouter(prefix="/transcription", tags=["Transcription"])

ALLOWED_ROLES = [ADMIN, LAWYER, DOCTOR, RESEARCHER, FINANCE, BUSINESS]


# -------------------------
# 1️⃣ Transcribe only
# -------------------------
@router.post("/audio")
async def transcribe_audio(
    file: UploadFile = File(...),
    user=Depends(require_roles(ALLOWED_ROLES))
):

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    transcript = transcribe_audio_file(file_path)

    return {
        "filename": file.filename,
        "text": transcript
    }


# -------------------------
# 2️⃣ Full processing
# -------------------------
@router.post("/audio/process")
async def process_audio(
    file: UploadFile = File(...),
    user=Depends(require_roles(ALLOWED_ROLES))
):

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1️⃣ Transcribe
    transcript = transcribe_audio_file(file_path)

    # 2️⃣ Store in RAG
    ingest_text_to_rag(
        text=transcript,
        source_id=f"audio:{file.filename}",
        metadata={
            "type": "audio",
            "filename": file.filename,
            "uploaded_by": str(user)
        }
    )

    # 3️⃣ Summarize
    summary = effective_extractive_summary(transcript)

    return {
        "filename": file.filename,
        "transcript": transcript,
        "summary": summary
    }