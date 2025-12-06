from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from db import get_db
from models_db import User, Bank

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
  bank_code: str | None = None   # required if role == "banker"


class LoginBody(BaseModel):
  username: str
  password: str


class RegisterBankBody(BaseModel):
  bank_name: str
  bank_code: str
  admin_email: str
  admin_password: str


class TokenBody(BaseModel):
  token: str


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
# Bank Registration (done once per bank)
# ---------------------------------------------------------
@router.post("/register-bank")
def register_bank(body: RegisterBankBody, db: Session = Depends(get_db)):
  # 1) Check bank_code is unique
  existing_bank = db.query(Bank).filter(Bank.bank_code == body.bank_code).first()
  if existing_bank:
    raise HTTPException(status_code=400, detail="Bank code already registered.")

  # 2) Create Bank record
  bank = Bank(
    name=body.bank_name,
    bank_code=body.bank_code,
  )
  db.add(bank)
  db.commit()
  db.refresh(bank)

  # 3) Create initial banker admin (username = admin_email for simplicity)
  hashed_pw = pwd_context.hash(body.admin_password)
  admin_user = User(
    username=body.admin_email,
    email=body.admin_email,
    password_hash=hashed_pw,
    role="banker",
    bank_id=bank.id,
  )
  db.add(admin_user)
  db.commit()
  db.refresh(admin_user)

  token = create_jwt(admin_user)

  return {
    "message": "Bank registered successfully. Admin banker account created.",
    "token": token,
    "role": admin_user.role,
    "username": admin_user.username,
    "bank_code": bank.bank_code,
  }


# ---------------------------------------------------------
# Register normal user OR banker (under an existing bank)
# ---------------------------------------------------------
@router.post("/register")
def register(body: RegisterBody, db: Session = Depends(get_db)):

  # username unique
  existing = db.query(User).filter(User.username == body.username).first()
  if existing:
    raise HTTPException(status_code=400, detail="Username already exists.")

  bank_id = None

  if body.role == "banker":
    # banker must be attached to a bank
    if not body.bank_code:
      raise HTTPException(
        status_code=400,
        detail="Bank code is required to register as banker.",
      )
    bank = db.query(Bank).filter(Bank.bank_code == body.bank_code).first()
    if not bank:
      raise HTTPException(status_code=400, detail="Invalid bank code.")
    bank_id = bank.id

  hashed_pw = pwd_context.hash(body.password)

  new_user = User(
    username=body.username,
    email=body.email,
    password_hash=hashed_pw,
    role=body.role,
    bank_id=bank_id,
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  token = create_jwt(new_user)

  response = {
    "message": "Registered successfully",
    "token": token,
    "role": new_user.role,
    "username": new_user.username,
  }

  if new_user.role == "banker" and bank_id:
    response["bank_code"] = body.bank_code

  return response


# ---------------------------------------------------------
# Login  (username OR email)
# ---------------------------------------------------------
@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):

  user = (
    db.query(User)
    .filter(
      or_(
        User.username == body.username,
        User.email == body.username,
      )
    )
    .first()
  )

  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  if not pwd_context.verify(body.password, user.password_hash):
    raise HTTPException(status_code=400, detail="Incorrect password")

  token = create_jwt(user)

  bank_code = None
  if user.role == "banker" and user.bank_id:
    bank = db.query(Bank).filter(Bank.id == user.bank_id).first()
    bank_code = bank.bank_code if bank else None

  response = {
    "message": "Login successful",
    "token": token,
    "role": user.role,
    "username": user.username,
  }

  if bank_code:
    response["bank_code"] = bank_code

  return response


# ---------------------------------------------------------
# Verify token / get user profile
# ---------------------------------------------------------
@router.post("/me")
def me(body: TokenBody, db: Session = Depends(get_db)):
  """
  Used by frontend to validate stored token and get user info.
  """
  try:
    decoded = jwt.decode(body.token, SECRET_KEY, algorithms=[ALGORITHM])
    username = decoded.get("sub")

    user = db.query(User).filter(User.username == username).first()
    if not user:
      raise HTTPException(status_code=404, detail="Invalid token user")

    bank_code = None
    if user.role == "banker" and user.bank_id:
      bank = db.query(Bank).filter(Bank.id == user.bank_id).first()
      bank_code = bank.bank_code if bank else None

    return {
      "username": user.username,
      "role": user.role,
      "email": user.email,
      "created_at": user.created_at,
      "bank_code": bank_code,
    }

  except jwt.ExpiredSignatureError:
    raise HTTPException(401, "Token expired")
  except jwt.InvalidTokenError:
    raise HTTPException(401, "Invalid token")
