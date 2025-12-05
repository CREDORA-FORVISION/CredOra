# bank_server.py
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mock Bank Verification Server")

# This is the shared token between CredOra and the bank.
BANK_SHARED_TOKEN = "hdfc-demo-shared-token"

# Simulated employee records (in real life bank holds this)
EMPLOYEES = {
    "officer@hdfcbank.com": {
        "employee_id": "emp-001",
        "role": "underwriter",
        "bank_id": "bank_hdfc"
    },
    "manager@hdfcbank.com": {
        "employee_id": "emp-002",
        "role": "manager",
        "bank_id": "bank_hdfc"
    }
}

# Simulated customer records
CUSTOMERS = {
    "1234567890": {
        "user_id": "cust-789",
        "masked_account": "XXXXXX7890",
        "bank_id": "bank_hdfc"
    },
    "5555555555": {
        "user_id": "cust-101",
        "masked_account": "XXXXXX5555",
        "bank_id": "bank_hdfc"
    }
}

# ------------- Models -------------
class EmployeeVerifyRequest(BaseModel):
    email: str
    one_time_code: Optional[str] = None

class CustomerVerifyRequest(BaseModel):
    account_number: str
    phone: Optional[str] = None


# ------------- Employee Verification Endpoint -------------
@app.post("/verify-employee")
def verify_employee(data: EmployeeVerifyRequest,
                    shared_token: str = Header(None, alias="X-BANK-SHARED-TOKEN")):

    if shared_token != BANK_SHARED_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid shared token")

    email = data.email.lower()

    if email not in EMPLOYEES:
        return {"valid": False, "reason": "employee_not_found"}

    emp = EMPLOYEES[email]

    return {
        "valid": True,
        "employee_id": emp["employee_id"],
        "role": emp["role"],
        "bank_id": emp["bank_id"]
    }


# ------------- Customer Verification Endpoint -------------
@app.post("/verify-customer")
def verify_customer(data: CustomerVerifyRequest,
                    shared_token: str = Header(None, alias="X-BANK-SHARED-TOKEN")):

    if shared_token != BANK_SHARED_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid shared token")

    acc = data.account_number

    if acc not in CUSTOMERS:
        return {"valid": False, "reason": "not_found"}

    cust = CUSTOMERS[acc]

    return {
        "valid": True,
        "user_id": cust["user_id"],
        "masked_account": cust["masked_account"],
        "bank_id": cust["bank_id"]
    }