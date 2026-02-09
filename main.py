from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import engine, Base
from routers import todos, auth

app = FastAPI(
    title="Todo CRUD (HTML + JSON)",
    description="Server-rendered pages + JSON API using FastAPI, SQLite, SQLAlchemy",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
