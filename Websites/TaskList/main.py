from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException

app = FastAPI()

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

all_tasks = [
    Task(task_id=1, task_name="Sports", task_description="Go to the gym", priority=Priority.MEDIUM),
    Task(task_id=2, task_name="Read", task_description="Read 10 pages", priority=Priority.LOW),
    Task(task_id=3, task_name="Shop", task_description="Go shopping", priority=Priority.HIGH),
    Task(task_id=4, task_name="Study", task_description="Study for exams'", priority=Priority.HIGH),
    Task(task_id=5, task_name="Meditate", task_description="Meditate for 30 minutes", priority=Priority.MEDIUM),
]

        
@app.get("/tasks", response_model=List[Task])
def get_tasks(first_n: int = None):
    if first_n:
        return all_tasks[:first_n]
    else:
        return all_tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in all_tasks:
        if task.task_id == task_id:
            return task
    raise HTTPException(status_code=404, detail='Task not found')

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    new_task_id = max(task.task_id for task in all_tasks) + 1
    
    new_task = Task(task_id=new_task_id, task_name=task.task_name, task_description=task.task_description, priority=task.priority)
    
    all_tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in all_tasks:
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
    for index, task in enumerate(all_tasks):
        if task.task_id == task_id:
            deleted_task = all_tasks.pop(index)
            break
    if deleted_task:
        for task in all_tasks:
            if task.task_id > task_id:
                task.task_id -= 1
        return deleted_task
    raise HTTPException(status_code=404, detail='Task not found')