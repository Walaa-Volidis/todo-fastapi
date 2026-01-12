from typing import Optional, List
from enum import IntEnum
from fastapi import FastAPI
from pydantic import BaseModel, Field

api = FastAPI()

class PriorityLevel(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description="Name of the todo item")
    todo_description: str = Field(..., max_length=1024, description="Description of the todo item")
    priority: PriorityLevel = Field(default=PriorityLevel.LOW, description="Priority level of the todo item")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    pass

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description="Name of the todo item")
    todo_description: Optional[str] = Field(None, max_length=1024, description="Description of the todo item")
    priority: Optional[PriorityLevel] = Field(None, description="Priority level of the todo item")

all_todos = [
    {"todo_id": 1, "todo_name": "Buy groceries", "todo_description": "Milk, Bread, Eggs"},
    {"todo_id": 2, "todo_name": "Walk the dog", "todo_description": "Evening walk in the park"},
    {"todo_id": 3, "todo_name": "Read a book", "todo_description": "Finish reading '1984'"},
    {"todo_id": 4, "todo_name": "Exercise", "todo_description": "30 minutes of cardio"},
    {"todo_id": 5, "todo_name": "Call mom", "todo_description": "Catch up with family"}
]

# GET, POST, PUT, DELETE

@api.get("/")
def index():
    return {"message": "Hello, World!"}

@api.get("/calculation")
def calculation():
    pass
    return {"message": "This is the calculation endpoint."}

@api.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo["todo_id"] == todo_id:
            return {"restult": todo}
    return {"error": "Todo not found."}

@api.get("/todos")
def get_all_todos(first_n: int =  None):
    if(first_n):
        return {"result": all_todos[:first_n]}
    return {"result": all_todos}

@api.post("/todos")
def create_todo(todo: dict):
    new_todo_id = len(all_todos) + 1
    new_todo = {
        "todo_id": new_todo_id,
        "todo_name": todo["todo_name"],
        "todo_description": todo["todo_description"]
    }
    all_todos.append(new_todo)
    return {"message": "Todo created successfully.", "todo": new_todo}


@api.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo["todo_id"]== todo_id:
            todo["todo_name"] = updated_todo["todo_name"]
            todo["todo_description"] = updated_todo["todo_description"]
            return {"message": "Todo updated successfully.", "todo": todo}
    return {"error": "Todo not found."}

@api.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for todo in all_todos:
        if todo["todo_id"] == todo_id:
            all_todos.remove(todo)
            return {"message": "Todo deleted successfully.", "todo": todo}
    return {"error": "Todo not found."}