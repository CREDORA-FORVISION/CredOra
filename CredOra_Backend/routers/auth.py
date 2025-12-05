from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.bank_client import verify_employee, verify_customer
from services.jwt_utils import create_jwt

router = APIRouter(prefix="/auth", tags=["auth"])

class EmployeeLogin(BaseModel):
    bank_id: str
    email: str

class UserLogin(BaseModel):
    bank_id: str
    account_number: str

@router.post("/employee-login")
async def employee_login(data: EmployeeLogin):
    resp = await verify_employee(data.bank_id, data.email)
    if not resp.get("valid"):
        raise HTTPException(status_code=403, detail="Invalid employee")

    token = create_jwt({
        "kind": "employee",
        "bank_id": data.bank_id,
        "employee_id": resp["employee_id"],
        "role": resp["role"]
    })

    return {"token": token, "role": resp["role"]}

@router.post("/user-login")
async def user_login(data: UserLogin):
    resp = await verify_customer(data.bank_id, data.account_number)
    if not resp.get("valid"):
        raise HTTPException(status_code=403, detail="Invalid user")

    token = create_jwt({
        "kind": "user",
        "bank_id": data.bank_id,
        "user_id": resp["user_id"],
        "account_masked": resp["masked_account"]
    })

    return {"token": token, "user_id": resp["user_id"]}
