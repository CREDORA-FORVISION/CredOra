import httpx
from fastapi import HTTPException
from config import BANKS

async def call_bank(bank_id, path, payload):
    bank = BANKS[bank_id]

    url = bank["verify_base_url"] + path
    headers = {
        "Content-Type": "application/json",
        "X-BANK-SHARED-TOKEN": bank["shared_token"]
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(url, json=payload, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail="Bank server error")

    return resp.json()

async def verify_employee(bank_id, email):
    return await call_bank(bank_id, "/verify-employee", {"email": email})

async def verify_customer(bank_id, acc_number):
    return await call_bank(bank_id, "/verify-customer", {"account_number": acc_number})
