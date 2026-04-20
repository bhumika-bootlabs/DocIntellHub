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
from app.services.rag_service import ask_llm
from app.models.documents import Document
from app.models.users import User
from app.services.ocr_service import extract_text_from_file
from app.api.utility import summarize, format
from sqlalchemy.exc import IntegrityError
from app.services.reindex import rebuild_index
from app.core.security import create_access_token
from app.core.roles import ROLE_DOMAIN_MAP
from app.services.domain_classifier import detect_domain
from app.services.rag_ingest import ingest_text_to_rag


import os, traceback
import shutil

router = APIRouter()

ROLE_MODE_MAP = {
    "lawyer": ["legal"],
    "doctor": ["healthcare"],
    "researcher": ["academic"],
    "finance": ["finance"],
    "business": ["business"],
    "admin": ["legal", "finance", "academic", "healthcare", "business"]
}



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
    # ✅ get user (NOT token)
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # ✅ create token here
    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
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

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @router.post("/upload/file")
# def upload_file(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user: str = Depends(get_current_user)
# ):
#     # get user object from email
#     user = db.query(User).filter(User.email == current_user).first()
    
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     file_path = f"{UPLOAD_DIR}/{file.filename}"

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

import os
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/file")
def upload_file(
    # domain: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    user = db.query(User).filter(User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Save temporarily first
    temp_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    extracted_text = extract_text_from_file(temp_path)

    # Detect domain automatically
    detected_domain = detect_domain(extracted_text)

    if not detected_domain:
        os.remove(temp_path)
        raise HTTPException(
            status_code=400,
            detail="Document domain could not be identified"
        )

    # Check role permission
    allowed_domains = ROLE_DOMAIN_MAP.get(user.role, [])

    if detected_domain not in allowed_domains:
        os.remove(temp_path)
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: Users with role '{user.role}' are not permitted to upload '{detected_domain}' domain documents."
        )

    # Create domain folder
    domain_dir = os.path.join(UPLOAD_DIR, detected_domain)
    os.makedirs(domain_dir, exist_ok=True)

    final_path = os.path.join(domain_dir, file.filename)

    # Move file to correct domain folder
    shutil.move(temp_path, final_path)

    # Save document in DB
    new_doc = Document(
        filename=file.filename,
        domain=detected_domain,
        uploaded_by=user.id,
        file_path=final_path
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Send to RAG
    ingest_text_to_rag(
        text=extracted_text,
        source_id=str(new_doc.id),
        metadata={
            "domain": detected_domain,
            "uploaded_by": user.id,
            "document_id": new_doc.id
        }
    )

    return {
        "message": "File uploaded successfully",
        "document_id": new_doc.id,
        "domain": detected_domain
    }


    # # create document
    # document = Document(
    #     user_id=user.id,
    #     owner_id=user.id,
    #     filename=file.filename,
    #     file_path=file_path
    # )

    # db.add(document)
    # db.commit()
    # db.refresh(document)

    # OCR
    # extracted = extract_text(file_path)

    # text_record = ExtractedText(
    #     document_id=document.id,
    #     content=extracted
    # )

    # db.add(text_record)
    # db.commit()

    # rebuild_index()


    # return {
    #     "message": "File uploaded and processed",
    #     "document_id": document.id
    # }

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
def ask_question(
    question: str,
    mode: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    # 1️⃣ get user
    user = db.query(User).filter(User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 2️⃣ role → allowed modes
    allowed_modes = ROLE_MODE_MAP.get(user.role, [])

    if mode not in allowed_modes:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to use this mode"
        )

    # 3️⃣ retrieve only domain chunks
    context_chunks = retrieve_top_k(
        query=question,
        domain=mode,
        k=4
    )

    # 4️⃣ generate answer
    context = "\n".join(context_chunks)

    answer = ask_llm(question=question, context=context)
    print(context_chunks)

    return {
        "mode": mode,
        "question": question,
        "answer": answer
    }

router.include_router(summarize.router, tags=["Summarization"])
router.include_router(format.router, tags=["Formatting"])