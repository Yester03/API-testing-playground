from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TokenBlacklist, User
from app.utils.auth import decode_token


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise PermissionError("missing bearer token")

    token = authorization.replace("Bearer ", "", 1).strip()
    if db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first():
        raise PermissionError("token is logged out")

    payload = decode_token(token)
    username = payload.get("sub")
    if not username:
        raise PermissionError("invalid token payload")

    user = db.query(User).filter(User.username == username, User.is_deleted.is_(False)).first()
    if not user:
        raise PermissionError("user not found")
    if user.status != "active":
        raise PermissionError("user inactive")
    return user


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise PermissionError("admin required")
    return current_user
