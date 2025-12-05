import joblib
import numpy as np
import pandas as pd
import json
import os

# ---------------------------------------------------
# LOAD MODELS
# ---------------------------------------------------
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

MODEL_EMI = joblib.load(os.path.join(MODEL_DIR, "emi_stress_model.joblib"))
MODEL_STABILITY = joblib.load(os.path.join(MODEL_DIR, "stability_model.joblib"))
MODEL_HIDDEN = joblib.load(os.path.join(MODEL_DIR, "hidden_debt_model.joblib"))

FEATURES_EMI = json.load(open(os.path.join(MODEL_DIR, "emi_stress_features.json")))
FEATURES_STABILITY = json.load(open(os.path.join(MODEL_DIR, "stability_features.json")))
FEATURES_HIDDEN = json.load(open(os.path.join(MODEL_DIR, "hidden_features.json")))


# ===============================================================
# CSV FEATURE EXTRACTOR  (used for uploaded bank statements)
# ===============================================================
def extract_features_from_csv(df: pd.DataFrame):
    required = ["TransactionAmount", "TransactionType", "AccountBalance"]

    if not all(col in df.columns for col in required):
        return None

    df["TransactionAmount"] = pd.to_numeric(df["TransactionAmount"], errors="coerce")
    df["is_credit"] = df["TransactionType"].str.contains("credit", case=False).astype(int)
    df["is_debit"] = df["TransactionType"].str.contains("debit", case=False).astype(int)

    income = df[df["is_credit"] == 1]["TransactionAmount"].sum()
    expense = df[df["is_debit"] == 1]["TransactionAmount"].abs().sum()

    net_savings = income - expense
    savings_rate = net_savings / income if income > 0 else 0

    emi_amount = df[df["TransactionType"].str.contains("emi", case=False)]["TransactionAmount"].abs().sum()
    foir = emi_amount / income if income > 0 else 0

    features = {
        "income": float(income),
        "expense": float(expense),
        "net_savings": float(net_savings),
        "savings_rate": float(savings_rate),
        "emi_amount": float(emi_amount),
        "foir": float(foir),
        "avg_balance": float(df["AccountBalance"].mean()),
        "min_balance": float(df["AccountBalance"].min()),
        "num_transactions": int(len(df)),
        "num_emi_txns": int(len(df[df["TransactionType"].str.contains('emi', case=False)])),
        "customer_age": int(df["CustomerAge"].mean()) if "CustomerAge" in df.columns else 30,
        "hidden_debt_risk": 0.0,    # can be refined
        "missed_payments": 0,
        "customer_age": 30,
        "num_credit_lines": 1,
        "foir_current": foir,
        "foir_new": foir + 0.05
    }

    return features


# ===============================================================
# PREDICT EMI STRESS
# ===============================================================
def predict_emi_stress(features_dict):
    row = np.array([[features_dict[f] for f in FEATURES_EMI]])
    pred = MODEL_EMI.predict(row)[0]
    probs = MODEL_EMI.predict_proba(row)[0]

    label_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}

    return {
        "emi_stress_label": label_map[pred],
        "probability_low": float(probs[0]),
        "probability_medium": float(probs[1]),
        "probability_high": float(probs[2])
    }


# ===============================================================
# PREDICT FINANCIAL STABILITY
# ===============================================================
def predict_stability(features_dict):
    row = np.array([[features_dict[f] for f in FEATURES_STABILITY]])
    prob = MODEL_STABILITY.predict_proba(row)[0][1]
    pred = bool(prob >= 0.5)

    return {
        "financial_stability_probability": float(round(prob, 4)),
        "is_financially_stable": pred
    }


# ===============================================================
# PREDICT HIDDEN DEBT
# ===============================================================
def predict_hidden_debt(features_dict):
    row = np.array([[features_dict[f] for f in FEATURES_HIDDEN]])
    prob = MODEL_HIDDEN.predict_proba(row)[0][1]

    return {
        "hidden_debt_risk_probability": float(round(prob, 4)),
        "high_hidden_debt_risk": bool(prob >= 0.5)
    }
