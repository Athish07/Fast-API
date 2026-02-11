from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter()

SECRET_KEY = '2a35948981b2c3913f736e7b4ed8550f076969337db698426c9607c518344312'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token") 


class CreateUserRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


def authenticate_user(username: str, password: str, db: Session) -> Users | None:
    user = db.query(Users).filter(Users.email == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    if hasattr(user, "is_active") and not user.is_active:
        return None
    return user


def generate_jwt_token(email: str, user_id: int, expires_delta: timedelta) -> str:
    payload = {'sub': email, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    payload['exp'] = expires
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        user_id: int = payload.get("id")

        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return payload 
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
        
@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: CreateUserRequest,
                      db: Session = Depends(get_db)):
    existing = db.query(Users).filter(Users.email == user_request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    create_user_model = Users(
        email=user_request.email,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        is_active=True,
        role=user_request.role
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "User created", "user_id": create_user_model.id}

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = generate_jwt_token(user.email, user.id, expires_delta)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=int(expires_delta.total_seconds())
    )