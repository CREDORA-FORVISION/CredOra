from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from db import get_db
from models_db import User

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "CREDORA_SUPER_SECRET_KEY"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class RegisterBody(BaseModel):
    username: str
    email: str | None = None
    password: str
    role: str  # "user" or "banker"


class LoginBody(BaseModel):
    username: str
    password: str


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
def create_jwt(user: User):
    payload = {
        "sub": user.username,
        "role": user.role,
        "uid": user.id,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# Register
# ---------------------------------------------------------
@router.post("/register")
def register(body: RegisterBody, db: Session = Depends(get_db())):

    # username must be unique
    existing = db.query(User).filter(User.username == body.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = pwd_context.hash(body.password)

    new_user = User(
        username=body.username,
        email=body.email,
        password_hash=hashed_pw,
        role=body.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_jwt(new_user)

    return {
        "message": "Registered successfully",
        "token": token,
        "role": new_user.role,
        "username": new_user.username
    }


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------
@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db())):

    user = db.query(User).filter(User.username == body.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(body.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_jwt(user)

    return {
        "message": "Login successful",
        "token": token,
        "role": user.role,
        "username": user.username,
    }


# ---------------------------------------------------------
# Verify token / get user profile
# ---------------------------------------------------------
class TokenBody(BaseModel):
    token: str


@router.post("/me")
def me(body: TokenBody, db: Session = Depends(get_db())):
    """
    Used by frontend to validate stored token and get user info.
    """
    try:
        decoded = jwt.decode(body.token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded.get("sub")

        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="Invalid token user")

        return {
            "username": user.username,
            "role": user.role,
            "email": user.email,
            "created_at": user.created_at,
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
