import os

JWT_SECRET = os.getenv("CREDORA_JWT_SECRET", "CHANGE_THIS_SECRET")
JWT_ALG = "HS256"
JWT_EXP_MINUTES = 60

BANKS = {
    "bank_hdfc": {
        "bank_id": "bank_hdfc",
        "bank_name": "HDFC Bank Demo",
        "verify_base_url": "http://127.0.0.1:5000",
        "shared_token": "hdfc-demo-shared-token"
    }
}

MODEL_PATHS = {
    "emi": "models/emi_stress_model.joblib",
    "stability": "models/stability_model.joblib",
    "hidden": "models/hidden_debt_model.joblib"
}
