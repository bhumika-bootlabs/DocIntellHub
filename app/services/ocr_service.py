import pytesseract
from PIL import Image
import pdfplumber
from pathlib import Path
from app.services.audio_service import transcribe_audio_file
import os
def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    # TXT files
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # PDF files
    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text

    # Audio transcription
    elif ext in [".mp3", ".wav", ".m4a","webm"]:
        result = whisper_model.transcribe(file_path)
        return result["text"]

    else:
        raise ValueError(f"Unsupported file type: {ext}")

def extract_text(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return extract_from_pdf(file_path)

    return extract_from_image(file_path)

def extract_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_from_image(file_path: str) -> str:
    image = Image.open(file_path)
    return pytesseract.image_to_string(image).strip()
