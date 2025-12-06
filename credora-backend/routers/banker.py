# routers/banker.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from models_db import User
from services.risk_report_service import (
    get_latest_report_for_user,
    get_all_reports_for_user,
)
from schemas import UserOut, RiskReportOut, RiskReportList

router = APIRouter(prefix="/banker", tags=["Banker"])


@router.get("/users", response_model=List[UserOut])
def list_users(
    q: str | None = Query(default=None, description="Search by username/email"),
    db: Session = Depends(get_db),
):
  query = db.query(User).filter(User.role == "user")
  if q:
    like = f"%{q}%"
    query = query.filter(
      (User.username.ilike(like)) | (User.email.ilike(like))
    )
  return query.order_by(User.created_at.desc()).all()


@router.get("/users/{user_id}/latest-report", response_model=RiskReportOut)
def get_latest_user_report(user_id: int, db: Session = Depends(get_db)):
  report = get_latest_report_for_user(db, user_id)
  if not report:
    raise HTTPException(status_code=404, detail="No reports for this user yet")
  return report


@router.get("/users/{user_id}/reports", response_model=RiskReportList)
def get_all_user_reports(user_id: int, db: Session = Depends(get_db)):
  reports = get_all_reports_for_user(db, user_id)
  return {"items": reports}
