# services/risk_report_service.py
from sqlalchemy.orm import Session
import json
from typing import List, Optional

from models_db import RiskReport
from schemas import RiskReportOut


def save_risk_report(
    db: Session,
    *,
    user_id: int,
    input_source: str,
    model_result: dict,
) -> RiskReport:
    overall = model_result.get("overall_risk", {})
    emi = model_result.get("emi_stress", {})
    stability = model_result.get("stability", {})
    hidden = model_result.get("hidden_debt", {})

    report = RiskReport(
        user_id=user_id,
        input_source=input_source,
        emi_stress_label=emi.get("emi_stress_label"),
        stability_probability=stability.get("financial_stability_probability"),
        hidden_debt_probability=hidden.get("hidden_debt_risk_probability"),
        overall_risk_score=overall.get("overall_risk_score"),
        risk_bucket=overall.get("risk_bucket"),
        raw_result_json=json.dumps(model_result),
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_latest_report_for_user(db: Session, user_id: int) -> Optional[RiskReport]:
    return (
        db.query(RiskReport)
        .filter(RiskReport.user_id == user_id)
        .order_by(RiskReport.created_at.desc())
        .first()
    )


def get_all_reports_for_user(db: Session, user_id: int) -> List[RiskReport]:
    return (
        db.query(RiskReport)
        .filter(RiskReport.user_id == user_id)
        .order_by(RiskReport.created_at.desc())
        .all()
    )
