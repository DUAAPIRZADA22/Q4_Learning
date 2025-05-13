from fastapi import FastAPI, HTTPException
from typing import List
from models import UserCreate, UserRead, Task, TaskCreate, TaskUpdateStatus
from datetime import date

app = FastAPI()

# In-Memory Storage
users_db = {}
tasks_db = {}
user_counter = 1
task_counter = 1

# User Endpoints
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    global user_counter
    user_data = user.dict()
    user_data["id"] = user_counter
    users_db[user_counter] = user_data
    user_counter += 1
    return user_data

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Task Endpoints
@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    global task_counter
    if task.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    task_data = task.dict()
    task_data["id"] = task_counter
    task_data["status"] = "pending"
    tasks_db[task_counter] = task_data
    task_counter += 1
    return task_data

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: int, status_update: TaskUpdateStatus):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task["status"] = status_update.status
    return task

@app.get("/users/{user_id}/tasks", response_model=List[Task])
def list_user_tasks(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_tasks = [task for task in tasks_db.values() if task["user_id"] == user_id]
    return user_tasks