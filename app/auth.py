from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer
from .database import SessionLocal
from .models import User
from passlib.hash import bcrypt
import os

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
serializer = URLSafeSerializer(SECRET_KEY, salt="auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login")
def login_form(request: Request):
    return RedirectResponse("/static/login.html")

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        return RedirectResponse("/login", status_code=303)

    token = serializer.dumps({"user_id": user.id})
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("session", token, httponly=True, max_age=3600)
    return response

from fastapi import HTTPException

@router.get("/register")
def register_form(request: Request):
    return RedirectResponse("/static/register.html")

@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_pw = bcrypt.hash(password)
    user = User(username=username, email=email, password_hash=hashed_pw, role="user")
    db.add(user)
    db.commit()

    token = serializer.dumps({"user_id": user.id})
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("session", token, httponly=True, max_age=3600)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("session")
    return response

def get_current_user(request: Request, db: Session = Depends(get_db)):
    session = request.cookies.get("session")
    if not session:
        return None
    try:
        data = serializer.loads(session)
        return db.query(User).get(data["user_id"])
    except Exception:
        return None
