from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from db import get_db
from models_db import User, Bank

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "CREDORA_SUPER_SECRET_KEY"   # for deploy: move to .env
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class RegisterBankBody(BaseModel):
  bank_name: str
  bank_code: str
  admin_email: EmailStr
  admin_password: str


class RegisterBody(BaseModel):
  username: str
  email: EmailStr | None = None
  password: str
  role: str              # "user" or "banker"
  bank_code: str | None = None  # required only for banker


class LoginBody(BaseModel):
  username: str     # can be username OR email
  password: str


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
      "bank_id": user.bank_id,
      "exp": datetime.utcnow() + timedelta(hours=24),
  }
  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# Register BANK (Bank admin)
# ---------------------------------------------------------
@router.post("/register-bank")
def register_bank(body: RegisterBankBody, db: Session = Depends(get_db)):
  # check unique bank_code
  existing = db.query(Bank).filter(Bank.code == body.bank_code).first()
  if existing:
      raise HTTPException(status_code=400, detail="Bank code already exists")

  # create bank
  admin_pw_hash = pwd_context.hash(body.admin_password)
  bank = Bank(
      name=body.bank_name,
      code=body.bank_code,
      admin_email=body.admin_email,
      admin_password_hash=admin_pw_hash,
  )
  db.add(bank)
  db.commit()
  db.refresh(bank)

  # also create a banker user for this admin
  user = User(
      username=body.admin_email,    # admin logs in with email as username
      email=body.admin_email,
      password_hash=admin_pw_hash,
      role="banker",
      bank_id=bank.id,
  )
  db.add(user)
  db.commit()
  db.refresh(user)

  token = create_jwt(user)

  return {
      "message": "Bank registered successfully",
      "bank_code": bank.code,
      "token": token,
      "role": user.role,
      "username": user.username,
  }


# ---------------------------------------------------------
# Register USER / BANKER
# ---------------------------------------------------------
@router.post("/register")
def register(body: RegisterBody, db: Session = Depends(get_db)):
  # username unique
  existing = db.query(User).filter(User.username == body.username).first()
  if existing:
      raise HTTPException(status_code=400, detail="Username already exists")

  bank = None
  bank_id = None

  # if registering banker → must have valid bank_code
  if body.role == "banker":
      if not body.bank_code:
          raise HTTPException(status_code=400, detail="Bank code is required for banker registration")
      bank = db.query(Bank).filter(Bank.code == body.bank_code).first()
      if not bank:
          raise HTTPException(status_code=404, detail="Bank not found")
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

  return {
      "message": "Registered successfully",
      "token": token,
      "role": new_user.role,
      "username": new_user.username,
      "bank_code": bank.code if bank else None,
  }


# ---------------------------------------------------------
# Login (user + banker)
# ---------------------------------------------------------
@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
  # username field can be username OR email
  user = (
      db.query(User)
      .filter((User.username == body.username) | (User.email == body.username))
      .first()
  )

  if not user:
      raise HTTPException(status_code=404, detail="User not found")

  if not pwd_context.verify(body.password, user.password_hash):
      raise HTTPException(status_code=400, detail="Incorrect password")

  token = create_jwt(user)

  bank = None
  if user.bank_id:
      bank = db.query(Bank).filter(Bank.id == user.bank_id).first()

  return {
      "message": "Login successful",
      "token": token,
      "role": user.role,
      "username": user.username,
      "bank_code": bank.code if bank else None,
  }


# ---------------------------------------------------------
# Verify token / get user profile
# ---------------------------------------------------------
@router.post("/me")
def me(body: TokenBody, db: Session = Depends(get_db)):
  try:
      decoded = jwt.decode(body.token, SECRET_KEY, algorithms=[ALGORITHM])
      username = decoded.get("sub")

      user = db.query(User).filter(User.username == username).first()
      if not user:
          raise HTTPException(status_code=404, detail="Invalid token user")

      bank_code = None
      if user.bank_id:
          bank = db.query(Bank).filter(Bank.id == user.bank_id).first()
          bank_code = bank.code if bank else None

      return {
          "username": user.username,
          "role": user.role,
          "email": user.email,
          "created_at": user.created_at,
          "bank_code": bank_code,
      }

  except jwt.ExpiredSignatureError:
      raise HTTPException(status_code=401, detail="Token expired")
  except jwt.InvalidTokenError:
      raise HTTPException(status_code=401, detail="Invalid token")
