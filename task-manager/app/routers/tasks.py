from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from app.database import get_session
from app.models import Task, User
from app.enums import Status, Priority, Role
from app.dtos.requests import TaskCreateRequest, TaskUpdateRequest
from app.dtos.responses import TaskResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task_in: TaskCreateRequest, current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    new_task = Task(
        title=task_in.title,
        description=task_in.description,
        priority=task_in.priority,
        status=Status.todo,
        due_date=task_in.due_date,
        user_id=current_user.id
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.get("", response_model=list[TaskResponse])
def list_tasks(
        status: Status | None = None,
        priority: Priority | None = None,
        skip: int = 0,
        limit: int = 10,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    query = select(Task)
    if current_user.role != Role.admin:
        query = query.where(Task.user_id == current_user.id)

    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)

    return session.exec(query.offset(skip).limit(limit)).all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != Role.admin and task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdateRequest, current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != Role.admin and task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, current_user: User = Depends(get_current_user),
                  session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != Role.admin and task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == Status.done:
        raise HTTPException(status_code=400, detail="Task is already completed")

    task.status = Status.done
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != Role.admin and task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return None