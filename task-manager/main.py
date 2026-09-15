from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routers import auth, tasks

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Task Manager API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome to Task Manager API!"}