from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.utility.users import UserSignup, UserLogin
from app.api.utility.db import get_db
from app.services.auth_service import create_user, authenticate_user
from app.api.utility.deps import get_current_user
from app.services.upload_service import upload_document
router = APIRouter()


@router.post("/auth/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    create_user(db, user.username, user.email, user.password)
    return {"message": "User registered successfully"}

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

@router.post("/upload/file")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    doc = upload_document(db, file, owner_id=1)  # owner_id mapping next phase
    return {
        "message": "File uploaded successfully",
        "file_id": doc.id
    }