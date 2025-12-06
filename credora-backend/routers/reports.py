# routers/reports.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models_db import User, RiskReport
import json

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/save")
def save_report(payload: dict, db: Session = Depends(get_db)):
  """
  payload:
  {
    "input_source": "manual" | "csv",
    "result": {... full ML result ...},
    "target_username": "user123"   <-- for banker
    OR
    "user_id": 5                    <-- for user
  }
  """

  # CASE 1 — banker saving for customer
  if "target_username" in payload:
    user = db.query(User).filter(User.username == payload["target_username"]).first()
    if not user:
      raise HTTPException(status_code=404, detail="Target user not found.")
    user_id = user.id

  # CASE 2 — user saving for self
  elif "user_id" in payload:
    user_id = payload["user_id"]

  else:
    raise HTTPException(status_code=400, detail="Must provide user_id or target_username")

  report = RiskReport(
    user_id=user_id,
    input_source=payload["input_source"],
    emi_stress_label=payload["result"]["emi_stress"]["emi_stress_label"],
    stability_probability=payload["result"]["stability"]["financial_stability_probability"],
    hidden_debt_probability=payload["result"]["hidden_debt"]["hidden_debt_risk_probability"],
    overall_risk_score=payload["result"]["overall_risk"]["overall_risk_score"],
    risk_bucket=payload["result"]["overall_risk"]["risk_bucket"],
    raw_result_json=json.dumps(payload["result"]),
  )

  db.add(report)
  db.commit()
  db.refresh(report)
  return {"status": "saved", "report_id": report.id}


@router.get("/user/{username}")
def get_user_with_reports(username: str, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.username == username).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  reports = (
    db.query(RiskReport)
    .filter(RiskReport.user_id == user.id)
    .order_by(RiskReport.created_at.desc())
    .all()
  )

  return {
    "user": {
      "id": user.id,
      "username": user.username,
      "email": user.email,
      "role": user.role,
      "created_at": user.created_at,
    },
    "reports": [
      {
        "id": r.id,
        "input_source": r.input_source,
        "emi_stress_label": r.emi_stress_label,
        "stability_probability": r.stability_probability,
        "hidden_debt_probability": r.hidden_debt_probability,
        "overall_risk_score": r.overall_risk_score,
        "risk_bucket": r.risk_bucket,
        "created_at": r.created_at,
      }
      for r in reports
    ],
  }
