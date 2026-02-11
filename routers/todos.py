from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Todo,Users
from routers.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


        
@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request, 
    db: Session = Depends(get_db)
    ):
    tasks = db.query(Todo).order_by(Todo.date_created.asc()).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "tasks": tasks}
    )

@router.post("/", response_class=HTMLResponse)
async def create_task(
    content: str = Form(...), db: Session = Depends(get_db),
    # user: Users = Depends(get_current_user)
    ):
    todo = Todo(content=content, date_created=datetime.now(timezone.utc))
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/delete/{id}")
async def delete_task(
    id: int, 
    db: Session = Depends(get_db),
    #user: Users = Depends(get_current_user)
    ):
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/update/{id}", response_class=HTMLResponse)
async def show_update(
    id: int, 
    request: Request, db: Session = Depends(get_db),
    #user: Users = Depends(get_current_user)
    ):
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse(
        "update.html",
        {"request": request, "task": todo}
    )

@router.post("/update/{id}")
async def submit_update(
    id: int, 
    content: str = Form(...), 
    db: Session = Depends(get_db),
    #users: Users = Depends(get_current_user)
    ):
    todo = db.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    todo.content = content
    db.commit()
    return RedirectResponse(url="/", status_code=303)