import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "data/documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file: UploadFile):
    ext = file.filename.split(".")[-1]
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return filename, file_path

