from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.roles import  ROLE_DOMAIN_MAP

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"user_id": user_id, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token validation failed")


from app.core.roles import ADMIN

def require_roles(allowed_roles: list):
    def checker(user=Depends(get_current_user)):
        # Admin can access everything
        if user["role"] == ADMIN:
            return user

        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied for your role"
            )
        return user
    return checker

