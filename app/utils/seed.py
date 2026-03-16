from sqlalchemy.orm import Session

from app.models import Item, User
from app.utils.auth import hash_password


def seed_data(db: Session):
    if db.query(User).count() == 0:
        db.add_all(
            [
                User(
                    username="admin",
                    email="admin@example.com",
                    hashed_password=hash_password("Admin123456"),
                    role="admin",
                    status="active",
                ),
                User(
                    username="tester",
                    email="tester@example.com",
                    hashed_password=hash_password("Test123456"),
                    role="user",
                    status="active",
                ),
            ]
        )

    if db.query(Item).count() == 0:
        db.add_all(
            [
                Item(name="Keyboard", price=99.9, stock=50, category="hardware", tags=["office", "usb"]),
                Item(name="Mouse", price=49.5, stock=100, category="hardware", tags=["wireless"]),
                Item(name="Notebook", price=9.9, stock=200, category="stationery", tags=["paper"]),
            ]
        )

    db.commit()
