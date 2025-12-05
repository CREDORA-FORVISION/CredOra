from fastapi import APIRouter, UploadFile, File, HTTPException
from ml.ml_engine import (
    predict_emi_stress,
    predict_stability,
    predict_hidden_debt,
    extract_features_from_csv
)
import pandas as pd
import io

router = APIRouter(prefix="/ml", tags=["ML Models"])

# ------------------------------
# 1) Predict from CSV Upload
# ------------------------------
@router.post("/predict-from-csv")
async def predict_from_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        features = extract_features_from_csv(df)
        if features is None:
            raise HTTPException(status_code=400, detail="CSV format not supported")

        emi_result = predict_emi_stress(features)
        stability_result = predict_stability(features)
        hidden_result = predict_hidden_debt(features)

        return {
            "status": "success",
            "emi_stress": emi_result,
            "stability": stability_result,
            "hidden_debt": hidden_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# 2) Predict from API JSON data
# ------------------------------
@router.post("/predict")
def predict_all(features: dict):
    try:
        emi_result = predict_emi_stress(features)
        stability_result = predict_stability(features)
        hidden_result = predict_hidden_debt(features)

        return {
            "emi_stress": emi_result,
            "stability": stability_result,
            "hidden_debt": hidden_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
