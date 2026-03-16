from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Item, Order, User
from app.schemas import OrderCreate, OrderOut
from app.utils.response import err, ok

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("")
def create_order(payload: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    user = db.query(User).filter(User.id == payload.user_id, User.is_deleted.is_(False)).first()
    if not user:
        return err("user not found", 10001, 404)
    item = db.query(Item).filter(Item.id == payload.item_id).first()
    if not item:
        return err("item not found", 20001, 404)
    if item.stock < payload.quantity:
        return err("stock not enough", 30001, 409)

    item.stock -= payload.quantity
    order = Order(
        user_id=user.id,
        item_id=item.id,
        quantity=payload.quantity,
        unit_price=item.price,
        total_amount=item.price * payload.quantity,
        status="created",
        note=payload.note,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return ok(OrderOut.model_validate(order).model_dump(), status_code=201)


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return err("order not found", 30002, 404)
    return ok(OrderOut.model_validate(order).model_dump())


@router.get("")
def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _ = current_user
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    total = query.count()
    orders = query.offset((page - 1) * page_size).limit(page_size).all()
    return ok({"total": total, "list": [OrderOut.model_validate(o).model_dump() for o in orders]})


@router.post("/{order_id}/pay")
def pay_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return err("order not found", 30002, 404)
    if order.status == "paid":
        return err("order already paid", 30003, 409)
    if order.status == "cancelled":
        return err("cancelled order cannot be paid", 30004, 409)
    order.status = "paid"
    db.commit()
    db.refresh(order)
    return ok(OrderOut.model_validate(order).model_dump())


@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _ = current_user
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return err("order not found", 30002, 404)
    if order.status == "cancelled":
        return err("order already cancelled", 30005, 409)
    if order.status == "paid":
        return err("paid order cannot be cancelled", 30006, 409)
    order.status = "cancelled"
    item = db.query(Item).filter(Item.id == order.item_id).first()
    if item:
        item.stock += order.quantity
    db.commit()
    db.refresh(order)
    return ok(OrderOut.model_validate(order).model_dump())
