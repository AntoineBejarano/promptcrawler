"""
User schemas
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user import UserPlan


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    plan: UserPlan
    jobs_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class User(UserResponse):
    pass

