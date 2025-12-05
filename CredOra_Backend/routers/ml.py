from fastapi import APIRouter, UploadFile, File, Depends, Header, HTTPException
import pandas as pd
from services.jwt_utils import decode_jwt
from services.ml_engine import run_full_pipeline

router = APIRouter(prefix="/ml", tags=["ml"])

def get_user(token: str = Header(...)):
    if not token.lower().startswith("bearer "):
        raise HTTPException(status_code=401)
    jwt_token = token.split(" ")[1]
    return decode_jwt(jwt_token)

@router.post("/full-analysis")
async def full_analysis(
    file: UploadFile = File(...),
    emi_amount: float = 0,
    customer_age: int = 25,
    current_user=Depends(get_user)
):
    content = await file.read()
    df = pd.read_csv(pd.io.common.StringIO(content.decode()))

    result = run_full_pipeline(df, emi_amount, customer_age)
    return {"user": current_user, "result": result}
