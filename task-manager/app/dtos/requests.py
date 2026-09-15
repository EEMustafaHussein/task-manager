from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.enums import Priority

class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3)
    email: str
    password: str = Field(..., min_length=6)

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None
    priority: Priority = Priority.medium
    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be whitespace only")
        return v

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: datetime | None) -> datetime | None:
        if v and v < datetime.utcnow():
            raise ValueError("Due date cannot be in the past")
        return v

class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    priority: Priority | None = None
    due_date: datetime | None = None