from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/demo")
async def demo_report():
    return {"message": "Reports module placeholder"}
