from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TaskBase(BaseModel):
    task_name: str = Field(..., min_length=3, max_length=512, description='Name of task')
    task_description: str = Field(..., description='Description of the task')
    priority: Priority = Field(default=Priority.LOW, description='Priority of the task')

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    task_id: int = Field(..., description='Unique identifier of the task')

class TaskUpdate(BaseModel):
    task_name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of task')
    task_description: Optional[str] = Field(None, description='Description of the task')
    priority: Optional[Priority] = Field(None, description='Priority of the task')



task_db = {"tasks": [Task(task_id=1, task_name="test", task_description="the starting task")]}


        
@app.get("/tasks", response_model=List[Task])
def get_tasks(first_n: int = None):
    if first_n:
        return task_db["tasks"][:first_n]
    else:
        return task_db["tasks"]

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in task_db["tasks"]:
        if task.task_id == task_id:
            return task
    raise HTTPException(status_code=404, detail='Task not found')

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    new_task_id = max(task.task_id for task in task_db["tasks"]) + 1
    
    new_task = Task(task_id=new_task_id, task_name=task.task_name, task_description=task.task_description, priority=task.priority)
    
    task_db["tasks"].append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in task_db["tasks"]:
        if task.task_id == task_id:
            if updated_task.task_name is not None:
                task.task_name = updated_task.task_name
            if updated_task.task_description is not None:
                task.task_description = updated_task.task_description
            if updated_task.priority is not None:
                task.priority = updated_task.priority
            return task
    raise HTTPException(status_code=404, detail='Task not found')

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    deleted_task = {}
    for index, task in enumerate(task_db["tasks"]):
        if task.task_id == task_id:
            deleted_task = task_db["tasks"].pop(index)
            break
    if deleted_task:
        for task in task_db["tasks"]:
            if task.task_id > task_id:
                task.task_id -= 1
        return deleted_task
    raise HTTPException(status_code=404, detail='Task not found')