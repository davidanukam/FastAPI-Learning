from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI

app = FastAPI()

all_todos = [
    {'todo_id' : 1, 'todo_name': 'Sports', 'todo_description': 'Go to the gym'},
    {'todo_id' : 2, 'todo_name': 'Read', 'todo_description': 'Read 10 pages'},
    {'todo_id' : 3, 'todo_name': 'Shop', 'todo_description': 'Go shopping'},
    {'todo_id' : 4, 'todo_name': 'Study', 'todo_description': 'Study for exams'},
    {'todo_id' : 5, 'todo_name': 'Meditate', 'todo_description': 'Meditate for 30 minutes'},
]

@app.get("/")
def index():
    return {"message" : "Hello World"}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return {'result': todo}
        
@app.get("/todos")
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos

@app.post("/todos")
def create_todo(todo: dict):
    new_todo_id = max(todo['todo_id'] for todo in all_todos) + 1
    new_todo = {
        'todo_id': new_todo_id,
        'todo_name' : todo['todo_name'],
        'todo_description': todo['todo_description']
    }
    all_todos.append(new_todo)
    return new_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            todo['todo_name'] = updated_todo['todo_name']
            todo['todo_description'] = updated_todo['todo_description']
            return todo
    return "Error, not found"

@app.delete("/todos/{todo_id}")
def update_todo(todo_id: int):
    deleted_todo = {}
    for index, todo in enumerate(all_todos):
        if todo['todo_id'] == todo_id:
            deleted_todo = all_todos.pop(index)
            break
    if deleted_todo:
        for todo in all_todos:
            if todo['todo_id'] > todo_id:
                todo['todo_id'] -= 1
        return deleted_todo
    return "Error, not found"