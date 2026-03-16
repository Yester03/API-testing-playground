from fastapi import APIRouter, Depends, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Item
from app.schemas import ItemCreate, ItemOut, ItemUpdate
from app.utils.response import err, ok
from app.utils.validators import validate_order, validate_sort

router = APIRouter(prefix="/items", tags=["items"])


@router.get("")
def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = None,
    category: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    query = db.query(Item)
    if keyword:
        query = query.filter(Item.name.contains(keyword))
    if category:
        query = query.filter(Item.category == category)

    sort_by = validate_sort(sort_by, {"id", "name", "price", "stock", "created_at"}, "id")
    order = validate_order(order)
    sort_col = getattr(Item, sort_by)
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok({"total": total, "list": [ItemOut.model_validate(i).model_dump() for i in items]})


@router.post("")
def create_item(payload: ItemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return ok(ItemOut.model_validate(item).model_dump(), status_code=201)


@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return err("item not found", 20001, 404)
    return ok(ItemOut.model_validate(item).model_dump())


@router.put("/{item_id}")
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return err("item not found", 20001, 404)
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return ok(ItemOut.model_validate(item).model_dump())


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return err("item not found", 20001, 404)
    db.delete(item)
    db.commit()
    return ok(message="deleted")
