from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from starlette.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="My Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    done: Optional[bool] = None


class Todo(BaseModel):
    id: int
    title: str
    done: bool


todos_store: Dict[int, Todo] = {}
next_id: int = 1


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI", "docs": "/docs", "ui": "/ui"}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/api/todos", response_model=List[Todo])
def list_todos():
    return list(todos_store.values())


@app.post("/api/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoCreate):
    global next_id
    todo = Todo(id=next_id, title=payload.title, done=payload.done)
    todos_store[next_id] = todo
    next_id += 1
    return todo


@app.put("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate):
    if todo_id not in todos_store:
        raise HTTPException(status_code=404, detail="Todo not found")
    current = todos_store[todo_id]
    updated = current.model_copy(update={
        "title": payload.title if payload.title is not None else current.title,
        "done": payload.done if payload.done is not None else current.done,
    })
    todos_store[todo_id] = updated
    return updated


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos_store:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_store[todo_id]
    return


# Static UI at /ui
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/ui", StaticFiles(directory=str(static_dir), html=True), name="ui")