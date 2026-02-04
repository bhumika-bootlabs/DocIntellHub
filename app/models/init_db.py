from app.core.config import engine
from app.models.base import Base
from app.models.users import User
from app.models.documents import Document
from app.models.extracted_text import ExtractedText

def init_db():
    Base.metadata.create_all(bind=engine)
