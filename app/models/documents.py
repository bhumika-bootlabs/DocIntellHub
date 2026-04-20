from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.models.base import Base
from sqlalchemy.sql import func

# class Document(Base):
#     __tablename__ = "documents"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     filename = Column(String, nullable=False)
#     file_path = Column(String, nullable=False)
#     owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     uploaded_at = Column(DateTime(timezone=True), server_default=func.now())


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    domain = Column(String)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String)