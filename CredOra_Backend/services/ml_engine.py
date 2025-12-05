import joblib
import pandas as pd
from config import MODEL_PATHS
from services.feature_builder import (
    extract_base_features,
    build_emi_features,
    build_stability_features,
    build_hidden_debt_features
)

emi_model = joblib.load(MODEL_PATHS["emi"])
stab_model = joblib.load(MODEL_PATHS["stability"])
hidden_model = joblib.load(MODEL_PATHS["hidden"])

def run_full_pipeline(df: pd.DataFrame, emi_amount, customer_age):
    base = extract_base_features(df)

    # ============ Model 1 =============
    emi_features = build_emi_features(base, emi_amount, customer_age)
    emi_before = emi_model.predict_proba([list(emi_features.values())])[0][1]
    emi_after = emi_model.predict_proba([list(emi_features.values())])[0][1]

    # ============ Model 2 =============
    stability_features = build_stability_features(base, 0, emi_amount, customer_age)
    stab_score = stab_model.predict_proba([list(stability_features.values())])[0][1]

    # ============ Model 3 =============
    hidden_features = build_hidden_debt_features(df, base)
    hid_score = hidden_model.predict_proba([list(hidden_features.values())])[0][1]

    return {
        "emi_stress": {
            "before": emi_before,
            "after": emi_after,
        },
        "stability": {
            "score": stab_score
        },
        "hidden_debt": {
            "score": hid_score,
            "flags": hidden_features
        }
    }
