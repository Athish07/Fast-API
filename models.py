from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base
from sqlalchemy import Boolean, Column

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key= True, index = True)
    email = Column(String, unique= True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable= True)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String)
    
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(200), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"