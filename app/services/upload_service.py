from sqlalchemy.orm import Session
from app.models.documents import Document
from app.common_utils.file_handler import save_file

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

    return doc
