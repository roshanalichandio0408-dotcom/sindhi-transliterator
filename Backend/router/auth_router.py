from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Register: requires username + email + password ──
class RegisterData(BaseModel):
    username: str
    email:    EmailStr
    password: str

@router.post("/register")
def register(data: RegisterData, db: Session = Depends(get_db)):
    data.username = data.username.strip().lower()
    data.email    = data.email.strip().lower()

    if len(data.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters.")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=409, detail="Username already exists.")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered.")

    db.add(User(
        username = data.username,
        email    = data.email,
        password = hash_password(data.password)
    ))
    db.commit()
    return {"message": "Account created successfully."}


# ── Login: accepts username OR email ──
class LoginData(BaseModel):
    login:    str   # username or email
    password: str

@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    identifier = data.login.strip().lower()

    # Try matching by email first, then by username
    user = (
        db.query(User).filter(User.email == identifier).first() or
        db.query(User).filter(User.username == identifier).first()
    )

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return {
        "access_token": create_access_token({"sub": user.username}),
        "token_type":   "bearer",
        "username":     user.username
    }