# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


# ---------- User ----------
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str
    role: str  # "user" or "banker"


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


# ---------- Risk Reports ----------
class RiskReportOut(BaseModel):
    id: int
    user_id: int
    input_source: str
    emi_stress_label: Optional[str] = None
    stability_probability: Optional[float] = None
    hidden_debt_probability: Optional[float] = None
    overall_risk_score: Optional[float] = None
    risk_bucket: Optional[str] = None
    raw_result_json: Any
    created_at: datetime

    class Config:
        orm_mode = True


class RiskReportList(BaseModel):
    items: List[RiskReportOut]
