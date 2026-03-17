from fastapi import APIRouter, Depends, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import UserCreate, UserOut, UserPatch, UserUpdate
from app.utils.auth import hash_password
from app.utils.response import err, ok
from app.utils.validators import validate_order, validate_sort

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _ = current_user
    query = db.query(User).filter(User.is_deleted.is_(False))
    if keyword:
        query = query.filter((User.username.contains(keyword)) | (User.email.contains(keyword)))
    if status:
        query = query.filter(User.status == status)

    sort_by = validate_sort(sort_by, {"id", "username", "created_at"}, "id")
    order = validate_order(order)
    sort_col = getattr(User, sort_by)
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))

    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok({"total": total, "list": [UserOut.model_validate(u).model_dump() for u in users]})


@router.post("")
def create_user(payload: UserCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
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


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    user = db.query(User).filter(User.id == user_id, User.is_deleted.is_(False)).first()
    if not user:
        return err("user not found", 10001, 404)
    return ok(UserOut.model_validate(user).model_dump())


@router.put("/{user_id}")
def put_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    user = db.query(User).filter(User.id == user_id, User.is_deleted.is_(False)).first()
    if not user:
        return err("user not found", 10001, 404)
    conflict = db.query(User).filter(
        User.id != user_id,
        User.is_deleted.is_(False),
        ((User.username == payload.username) | (User.email == payload.email)),
    ).first()
    if conflict:
        return err("username or email already exists", 10010, 409)
    user.username = payload.username
    user.email = payload.email
    user.role = payload.role
    user.status = payload.status
    db.commit()
    db.refresh(user)
    return ok(UserOut.model_validate(user).model_dump())


@router.patch("/{user_id}")
def patch_user(user_id: int, payload: UserPatch, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    user = db.query(User).filter(User.id == user_id, User.is_deleted.is_(False)).first()
    if not user:
        return err("user not found", 10001, 404)
    updates = payload.model_dump(exclude_unset=True)
    next_username = updates.get("username", user.username)
    next_email = updates.get("email", user.email)
    conflict = db.query(User).filter(
        User.id != user_id,
        User.is_deleted.is_(False),
        ((User.username == next_username) | (User.email == next_email)),
    ).first()
    if conflict:
        return err("username or email already exists", 10010, 409)
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return ok(UserOut.model_validate(user).model_dump())


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    user = db.query(User).filter(User.id == user_id, User.is_deleted.is_(False)).first()
    if not user:
        return err("user not found", 10001, 404)
    user.is_deleted = True
    user.status = "inactive"
    db.commit()
    return ok(message="deleted")
