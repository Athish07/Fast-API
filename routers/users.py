from passlib.context import CryptContext
from fastapi import APIRouter,status, Depends
from database import get_db
from sqlalchemy.orm import Session
from models import Users
from routers.auth import get_current_user


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get("/profiledetails", status_code=status.HTTP_200_OK)
async def get_user_details(
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user)
    ):
    pass

    