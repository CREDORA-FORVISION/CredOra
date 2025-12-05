from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io

from ml.ml_engine import (
    extract_features_from_csv,
    run_full_risk_analysis,
)

router = APIRouter(prefix="/ml", tags=["ML Models"])


# ---------------------------------------------------
# 1) JSON-based prediction (for direct API / frontend)
# ---------------------------------------------------
@router.post("/predict")
async def predict_all(features: dict):
    """
    Takes a JSON with all required features and returns:
    - emi_stress
    - stability
    - hidden_debt
    - overall_risk (score + bucket + recommendation)
    """
    try:
        result = run_full_risk_analysis(features)
        return result
    except KeyError as e:
        # Helps you debug missing fields quickly
        missing = str(e).strip("'")
        raise HTTPException(
            status_code=400,
            detail=f"Missing required feature in JSON body: '{missing}'",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------
# 2) CSV upload prediction (bank statement file)
# ---------------------------------------------------
@router.post("/predict-from-csv")
async def predict_from_csv(file: UploadFile = File(...)):
    """
    Upload a bank statement CSV (training-like format) and we:
    - parse the CSV
    - build features
    - run all 3 models
    - return the same structure as /predict
    """
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        features = extract_features_from_csv(df)
        if features is None:
            raise HTTPException(
                status_code=400,
                detail="CSV format not supported or missing required columns.",
            )

        result = run_full_risk_analysis(features)
        # Optionally include raw features so frontend can show them
        result["features_used"] = features

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
