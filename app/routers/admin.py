from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_admin
from app.models import Item, Order, User
from app.schemas import UserOut
from app.utils.response import ok

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def stats(db: Session = Depends(get_db), admin=Depends(require_admin)):
    _ = admin
    return ok(
        {
            "users": db.query(User).filter(User.is_deleted.is_(False)).count(),
            "items": db.query(Item).count(),
            "orders": db.query(Order).count(),
        }
    )


@router.get("/users")
def admin_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    _ = admin
    users = db.query(User).filter(User.is_deleted.is_(False)).all()
    return ok([UserOut.model_validate(u).model_dump() for u in users])
