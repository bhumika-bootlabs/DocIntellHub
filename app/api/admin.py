from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.utility.db import get_db  
from app.models.users import User
from app.core.security import require_roles
from app.core.roles import ADMIN
from app.api.utility.users import UserOut

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["admin"]))
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}
