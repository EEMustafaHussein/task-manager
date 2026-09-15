from datetime import datetime
from sqlmodel import SQLModel, Field
from app.enums import Priority, Status, Role


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: Role = Field(default=Role.user)
    is_active: bool = Field(default=True)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    title: str
    description: str | None = Field(default=None)
    priority: Priority = Field(default=Priority.medium)
    status: Status = Field(default=Status.todo)
    due_date: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # ربط المهمة بالمستخدم صاحبها
    user_id: int = Field(foreign_key="users.id")