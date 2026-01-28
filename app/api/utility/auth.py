from app.models.users import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

fake_users_db = []

def register_user(user: UserCreate):
    hashed_pwd = hash_password(user.password)
    user_data = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_pwd
    }
    fake_users_db.append(user_data)
    return {"message": "User registered successfully!"}

def authenticate_user(email: str, password: str):
    for user in fake_users_db:
        if user["email"] == email and verify_password(password, user["hashed_password"]):
            token = create_access_token({"sub": user["email"]})
            return {"access_token": token, "token_type": "bearer"}
    return None

