from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserUpdate(UserBase):
    # password: str | None = None
    name: str | None = None
    email: str | None = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    avatar: str | None = None
    bio: str | None = None

    class Config:
        orm_mode = True


class MinimalUser(UserUpdate):
    id: int
    is_active: bool
    role: int

    class Config:
        orm_mode = True
