import json

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import IdempotencyRecord, Item, Order, User
from app.schemas import OrderCreate, OrderOut
from app.utils.response import err, ok
from app.utils.validators import make_request_hash

router = APIRouter(prefix="/idempotent", tags=["idempotent"])


@router.post("/orders")
def create_idempotent_order(
    payload: OrderCreate,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _ = current_user
    if not idempotency_key:
        return err("missing Idempotency-Key", 60001, 400)

    request_body = payload.model_dump_json()
    req_hash = make_request_hash(request_body)

    record = db.query(IdempotencyRecord).filter(IdempotencyRecord.key == idempotency_key).first()
    if record:
        if record.request_hash != req_hash:
            return err("idempotency key reused with different payload", 60002, 409)
        return ok(json.loads(record.response_body), message="idempotent replay", status_code=record.status_code)

    user = db.query(User).filter(User.id == payload.user_id, User.is_deleted.is_(False)).first()
    item = db.query(Item).filter(Item.id == payload.item_id).first()
    if not user:
        return err("user not found", 10001, 404)
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

    response_data = OrderOut.model_validate(order).model_dump(mode="json")
    rec = IdempotencyRecord(
        key=idempotency_key,
        endpoint="/idempotent/orders",
        request_hash=req_hash,
        response_body=json.dumps(response_data),
        status_code=201,
    )
    db.add(rec)
    db.commit()
    return ok(response_data, status_code=201)
