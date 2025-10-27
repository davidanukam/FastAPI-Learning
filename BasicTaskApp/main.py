from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI

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
    task_id: int

class TaskUpdate(BaseModel):
    task_name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of task')
    task_description: Optional[str] = Field(None, description='Description of the task')
    priority: Optional[Priority] = Field(None, description='Priority of the task')

all_tasks = [
    {'task_id' : 1, 'task_name': 'Sports', 'task_description': 'Go to the gym'},
    {'task_id' : 2, 'task_name': 'Read', 'task_description': 'Read 10 pages'},
    {'task_id' : 3, 'task_name': 'Shop', 'task_description': 'Go shopping'},
    {'task_id' : 4, 'task_name': 'Study', 'task_description': 'Study for exams'},
    {'task_id' : 5, 'task_name': 'Meditate', 'task_description': 'Meditate for 30 minutes'},
]

@app.get("/")
def index():
    return {"message" : "Hello World"}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in all_tasks:
        if task['task_id'] == task_id:
            return {'result': task}
        
@app.get("/tasks")
def get_tasks(first_n: int = None):
    if first_n:
        return all_tasks[:first_n]
    else:
        return all_tasks

@app.post("/tasks")
def create_task(task: dict):
    new_task_id = max(task['task_id'] for task in all_tasks) + 1
    new_task = {
        'task_id': new_task_id,
        'task_name' : task['task_name'],
        'task_description': task['task_description']
    }
    all_tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: dict):
    for task in all_tasks:
        if task['task_id'] == task_id:
            task['task_name'] = updated_task['task_name']
            task['task_description'] = updated_task['task_description']
            return task
    return "Error, not found"

@app.delete("/tasks/{task_id}")
def update_task(task_id: int):
    deleted_task = {}
    for index, task in enumerate(all_tasks):
        if task['task_id'] == task_id:
            deleted_task = all_tasks.pop(index)
            break
    if deleted_task:
        for task in all_tasks:
            if task['task_id'] > task_id:
                task['task_id'] -= 1
        return deleted_task
    return "Error, not found"