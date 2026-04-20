# placeholder
import whisper
import os
from app.services.reindex import rebuild_index



model = whisper.load_model("base")

def transcribe_audio_file(file_path: str) -> str:
    result = model.transcribe(file_path)
    return result["text"]
    rebuild_index()