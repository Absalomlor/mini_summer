from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Todo(BaseModel):
    id: int
    task: str
    done: bool = False

# Temporary storage for todos (in-memory)
todos: List[str] = []
next_id = 1

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/create-todo")
def create_todo(item: str = Form(...)):
    global next_id
    todo = Todo(id=next_id, task=item, done=False)
    todos.append(todo)
    next_id += 1
    return RedirectResponse("/", status_code=303)

@app.put("/update-todo/{todo_id}")
def update_todo(todo_id: int, item: str = Form(...)):
    for todo in todos:
        if todo.id == todo_id:
            todo.done = True
            todo.task = item
            return RedirectResponse("/", status_code=303)
    return {"error": "Todo not found"}

@app.get("/todos/pending")
def get_pending_todos():
    pending_todos = [todo for todo in todos if not todo.done]
    return {"pending_todos": pending_todos}

@app.delete("/delete-todo/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]
    return RedirectResponse("/", status_code=303)