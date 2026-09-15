from datetime import datetime
from app.enums import Priority, Status, Role
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Role
    is_active: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: Priority
    status: Status
    due_date: datetime | None
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True