from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoOut

app = FastAPI(
    title="Todo CRUD (HTML + JSON)",
    description="Server-rendered pages + JSON API using FastAPI, SQLite, SQLAlchemy",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Todo).order_by(Todo.date_created.asc()).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "tasks": tasks}
    )

@app.post("/", response_class=HTMLResponse)
async def create_task(content: str = Form(...), db: Session = Depends(get_db)):
    todo = Todo(content=content, date_created=datetime.utcnow())
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
   
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/update/{id}", response_class=HTMLResponse)
async def show_update(id: int, request: Request, db: Session = Depends(get_db)):
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse(
        "update.html",
        {"request": request, "task": todo}
    )

@app.post("/update/{id}")
async def submit_update(id: int, content: str = Form(...), db: Session = Depends(get_db)):
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    todo.content = content
    db.commit()
    return RedirectResponse(url="/", status_code=303)
