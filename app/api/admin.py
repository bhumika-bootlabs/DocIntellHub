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
    user=Depends(require_roles([ADMIN]))
):
    users = db.query(User).all()
    return users
