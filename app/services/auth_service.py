from sqlalchemy.orm import Session
from app.models.users import User
from app.core.security import hash_password, verify_password, create_access_token

def create_user(db: Session, email: str, password: str,role: str):
    user = User(
        # username=username,
        email=email,
        hashed_password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# def authenticate_user(db: Session, email: str, password: str):
#     user = db.query(User).filter(User.email == email).first()
#     if not user or not verify_password(password, user.hashed_password):
#         return None
#     token = create_access_token({"sub": user.email, "role": user.role})
#     return token
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user  

