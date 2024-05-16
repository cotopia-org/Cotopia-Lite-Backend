from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class UserUpdate(UserCreate):
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class User(UserUpdate):
    id: int
    is_active: bool
    role: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class MinimalUser(UserUpdate):
    id: int
    is_active: bool
    role: int

    class Config:
        orm_mode = True
