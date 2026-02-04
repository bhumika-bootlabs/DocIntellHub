from fastapi import APIRouter, UploadFile, File, Depends
from app.core.security import require_roles
from app.core.roles import ADMIN, LAWYER, DOCTOR, RESEARCHER, FINANCE, BUSINESS
import whisper
from app.services.audio_service import transcribe_audio
from app.services.summarization import effective_extractive_summary
from app.core.security import get_current_user
import os
from app.services.rag_ingest import ingest_text_to_rag
# from app.services.rag_store import store_chunks
from app.services.embedding_service import chunk_text

router = APIRouter(prefix="/transcription", tags=["Transcription"])

# model = whisper.load_model("base")

# @router.post("/audio")
# def transcribe_audio(
#     file: UploadFile = File(...),
#     user=Depends(require_roles([ADMIN, LAWYER, DOCTOR, RESEARCHER, FINANCE, BUSINESS]))
# ):
#     with open("temp_audio.wav", "wb") as f:
#         f.write(file.file.read())

#     result = model.transcribe("temp_audio.wav")

#     return {
#         "filename": file.filename,
#         "text": result["text"]
#     }

@router.post("/audio")
async def transcribe_and_summarize_audio(
    file: UploadFile = File(...),
    current_user = Depends(require_roles([
        "admin", "lawyer", "researcher", "finance", "business", "doctor"
    ]))
):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1️⃣ Transcribe
    transcript = transcribe_audio(file_path)

    # 2️⃣ Ingest into RAG
    ingest_text_to_rag(
        text=transcript,
        source_id=f"audio:{file.filename}",
        metadata={
            "type": "audio",
            "filename": file.filename,
            "uploaded_by": current_user
        }
    )

    # 3️⃣ Summarize
    summary = effective_extractive_summary(transcript)

    return {
        "filename": file.filename,
        "transcript": transcript,
        "summary": summary
    }