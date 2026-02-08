from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoOut

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Todo).order_by(Todo.date_created.asc()).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "tasks": tasks}
    )

@router.post("/", response_class=HTMLResponse)
async def create_task(content: str = Form(...), db: Session = Depends(get_db)):
    todo = Todo(content=content, date_created=datetime.utcnow())
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/delete/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
   
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/update/{id}", response_class=HTMLResponse)
async def show_update(id: int, request: Request, db: Session = Depends(get_db)):
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse(
        "update.html",
        {"request": request, "task": todo}
    )

@router.post("/update/{id}")
async def submit_update(id: int, content: str = Form(...), db: Session = Depends(get_db)):
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    todo.content = content
    db.commit()
    return RedirectResponse(url="/", status_code=303)