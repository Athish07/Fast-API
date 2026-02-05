# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime

class TodoCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=200)

class TodoUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=200)

class TodoOut(BaseModel):
    id: int
    content: str
    date_created: datetime

    class Config:
        from_attributes = True