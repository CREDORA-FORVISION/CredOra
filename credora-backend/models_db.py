# models_db.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base


class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)

    admin_email = Column(String(255), nullable=False)
    admin_password_hash = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # One bank → many users (bankers + customers)
    users = relationship("User", back_populates="bank")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, index=True)  # "user" or "banker"
    created_at = Column(DateTime, default=datetime.utcnow)

    # NEW: link to bank
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=True, index=True)
    bank = relationship("Bank", back_populates="users")

    risk_reports = relationship("RiskReport", back_populates="user")


class RiskReport(Base):
    __tablename__ = "risk_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    input_source = Column(String(20), nullable=False)  # "manual" or "csv"

    emi_stress_label = Column(String(20), nullable=True)
    stability_probability = Column(Float, nullable=True)
    hidden_debt_probability = Column(Float, nullable=True)
    overall_risk_score = Column(Float, nullable=True)
    risk_bucket = Column(String(20), nullable=True)

    raw_result_json = Column(Text, nullable=False)  # full JSON string

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="risk_reports")
