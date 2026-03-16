from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class APIResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Any = None


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: Literal["admin", "user"] = "user"
    status: Literal["active", "inactive"] = "active"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=64)


class UserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: Literal["admin", "user"] = "user"
    status: Literal["active", "inactive"] = "active"


class UserPatch(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = None
    role: Literal["admin", "user"] | None = None
    status: Literal["active", "inactive"] | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=50)
    tags: list[str] = Field(default_factory=list)
    is_active: bool = True

    @field_validator("tags")
    @classmethod
    def limit_tags(cls, v: list[str]) -> list[str]:
        if len(v) > 10:
            raise ValueError("tags max length is 10")
        return v


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemOut(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    user_id: int
    item_id: int
    quantity: int = Field(..., ge=1, le=100)
    note: str = Field(default="", max_length=255)


class OrderOut(BaseModel):
    id: int
    user_id: int
    item_id: int
    quantity: int
    unit_price: float
    total_amount: float
    status: str
    note: str
    created_at: datetime

    class Config:
        from_attributes = True
