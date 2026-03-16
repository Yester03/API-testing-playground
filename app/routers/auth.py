from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.models import TokenBlacklist, User
from app.schemas import LoginRequest, UserCreate, UserOut
from app.utils.auth import create_access_token, hash_password, verify_password
from app.utils.response import err, ok

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first()
    if exists:
        return err("username or email already exists", 10010, 409)
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        status=payload.status,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return ok(UserOut.model_validate(user).model_dump(), status_code=201)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username, User.is_deleted.is_(False)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        return err("invalid username or password", 10011, 401)
    token, expires_in = create_access_token(user.username, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return ok({"access_token": token, "token_type": "bearer", "expires_in": expires_in})


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return ok(UserOut.model_validate(current_user).model_dump())


@router.post("/logout")
def logout(authorization: str | None = Header(default=None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _ = current_user
    token = authorization.replace("Bearer ", "", 1).strip() if authorization else ""
    if token:
        db.add(TokenBlacklist(token=token))
        db.commit()
    return ok(message="logout success")


@router.get("/forbidden-demo")
def forbidden_demo(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        return err("forbidden", 10013, 403)
    return ok({"hint": "you are admin"})
