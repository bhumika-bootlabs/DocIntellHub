from sqlalchemy import Column, Integer, Text, ForeignKey
from app.models.base import Base

class ExtractedText(Base):
    __tablename__ = "extracted_text"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
