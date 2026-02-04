from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.utility.users import UserSignup, UserLogin
from app.api.utility.db import get_db
from app.services.auth_service import create_user, authenticate_user
from app.api.utility.deps import get_current_user
from app.services.upload_service import upload_document
from app.models.extracted_text import ExtractedText
from app.services.embedding_service import chunk_text, embed_and_store, retrieve_top_k
# from app.services.vector_store import VectorStore
from app.services.rag_service import generate_answer
from app.models.documents import Document
from app.models.users import User
from app.services.ocr_service import extract_text
from app.api.utility import summarize, format
from sqlalchemy.exc import IntegrityError
from app.services.reindex import rebuild_index

import os, traceback
import shutil

router = APIRouter()


@router.post("/auth/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    try:
        create_user(db, email=user.email, password=user.password, role=user.role)
        return {"message": "User registered successfully"}
    except IntegrityError as e:
        db.rollback()
        print("DB ERROR:", e)
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

@router.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2 uses "username" field
    token = authenticate_user(db, form_data.username, form_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# @router.post("/upload/file")
# def upload_file(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user: str = Depends(get_current_user)
# ):
#     doc = upload_document(db, file, owner_id=1)  # owner_id mapping next phase
#     return {
#         "message": "File uploaded successfully",
#         "file_id": doc.id
#     }

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/file")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # get user object from email
    user = db.query(User).filter(User.email == current_user).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    

    # create document
    document = Document(
        user_id=user.id,
        owner_id=user.id,
        filename=file.filename,
        file_path=file_path
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # OCR
    extracted = extract_text(file_path)

    text_record = ExtractedText(
        document_id=document.id,
        content=extracted
    )

    db.add(text_record)
    db.commit()

    rebuild_index()


    return {
        "message": "File uploaded and processed",
        "document_id": document.id
    }

# vector_store = VectorStore(dim=384)
@router.post("/index/documents")
def index_documents(db: Session = Depends(get_db)):
    records = db.query(ExtractedText).all()

    all_chunks = []
    for record in records:
        all_chunks.extend(chunk_text(record.content))

    embeddings = embed_text(all_chunks)
    vector_store.add(embeddings, all_chunks)

    return {"indexed_chunks": len(all_chunks)}

@router.post("/search")
def semantic_search(query: str):
    query_embedding = embed_text([query])
    results = vector_store.search(query_embedding)

    return {"results": results}

@router.post("/ask")
def ask_question(question: str):
    # 1️⃣ Retrieve relevant chunks from VECTOR_STORE
    context_chunks = retrieve_top_k(question, k=4)

    # 2️⃣ Generate answer using Groq / LLM
    answer = generate_answer(context_chunks, question)

    return {
        "question": question,
        "answer": answer
    }

router.include_router(summarize.router, tags=["Summarization"])
router.include_router(format.router, tags=["Formatting"])