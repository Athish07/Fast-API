# models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(200), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"