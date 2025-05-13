from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date
from pydantic import constr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    due_date: date
    user_id: int

    @field_validator("due_date")
    def due_date_not_in_past(cls, v):
        if v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    user_id: int

    @field_validator("due_date")
    def due_date_not_in_past(cls, v):
        if v < date.today():
            raise ValueError("due_date cannot be in the past")
        return v

class TaskUpdateStatus(BaseModel):
    status: str

    @field_validator("status")
    def validate_status(cls, v):
        allowed = ["pending", "in_progress", "completed"]
        if v not in allowed:
            raise ValueError(f"Status must be one of: {allowed}")
        return v