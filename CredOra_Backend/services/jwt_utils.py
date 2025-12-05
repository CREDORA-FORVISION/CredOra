import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from config import JWT_SECRET, JWT_ALG, JWT_EXP_MINUTES

def create_jwt(payload: dict):
    exp = datetime.utcnow() + timedelta(minutes=JWT_EXP_MINUTES)
    payload.update({"exp": exp})
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
