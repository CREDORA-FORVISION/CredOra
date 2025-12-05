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
    """
    Turn a raw bank statement CSV into a single feature dict
    that matches ALL 3 model feature lists.
    """

    required = ["TransactionAmount", "TransactionType", "AccountBalance"]
    if not all(col in df.columns for col in required):
        return None

    # Basic cleaning
    df["TransactionAmount"] = pd.to_numeric(df["TransactionAmount"], errors="coerce")
    df["AccountBalance"] = pd.to_numeric(df["AccountBalance"], errors="coerce")
    df = df.dropna(subset=["TransactionAmount", "AccountBalance"])

    df["TransactionType"] = df["TransactionType"].astype(str)

    df["is_credit"] = df["TransactionType"].str.contains("credit", case=False).astype(int)
    df["is_debit"] = df["TransactionType"].str.contains("debit", case=False).astype(int)

    # ---------- Core cash-flow ----------
    income = df[df["is_credit"] == 1]["TransactionAmount"].sum()
    expense = df[df["is_debit"] == 1]["TransactionAmount"].abs().sum()

    net_savings = income - expense
    savings_rate = net_savings / income if income > 0 else 0.0
    # *** this was missing – needed by stability model ***
    savings_months = net_savings / expense if expense > 0 else 0.0

    # EMI
    emi_mask = df["TransactionType"].str.contains("emi", case=False)
    emi_amount = df[emi_mask]["TransactionAmount"].abs().sum()
    foir = emi_amount / income if income > 0 else 0.0

    # ---------- Hidden debt style features ----------
    bnpl_mask = df["TransactionType"].str.contains("bnpl", case=False)
    microloan_mask = df["TransactionType"].str.contains("microloan", case=False)

    bnpl_txn_count = int(bnpl_mask.sum())
    microloan_txn_count = int(microloan_mask.sum())

    bnpl_spend = df[bnpl_mask]["TransactionAmount"].abs().sum()
    microloan_spend = df[microloan_mask]["TransactionAmount"].abs().sum()

    hidden_emi_amount = float(emi_amount * 1.2)  # simple proxy
    hidden_emi_to_income_ratio = (
        hidden_emi_amount / income if income > 0 else 0.0
    )

    # Income volatility as std of txns (rough proxy)
    income_volatility = float(df["TransactionAmount"].std() or 0.0)

    # “Spending growth” proxy: expense relative to income
    spending_growth = float(expense / income) if income > 0 else 0.0

    # High-risk merchants (toy example)
    high_risk_merchants = int(
        df["TransactionType"]
        .str.contains("casino|bet|gambling", case=False)
        .sum()
    )

    # Wallet usage proxy – balance range
    wallet_credit_usage = float(df["AccountBalance"].max() - df["AccountBalance"].min())

    # Missed-payment proxy: how many days balance < threshold
    low_balance_days = int((df["AccountBalance"] < 1000).sum())
    missed_payments = int(low_balance_days > 5)

    # Simple synthetic values where statement doesn’t give us info
    customer_age = 28
    hidden_debt_risk = 0.05        # baseline small risk
    num_credit_lines = 1
    foir_current = foir
    foir_new = foir + 0.05         # assume new EMI slightly increases FOIR
    freq_new_credit = 1            # dummy – could be improved

    # ---------- FINAL FEATURE DICT ----------
    features = {
        # EMI + cash flow (used by EMI & stability models)
        "income": float(income),
        "expense": float(expense),
        "net_savings": float(net_savings),
        "savings_rate": float(savings_rate),
        "savings_months": float(savings_months),
        "emi_amount": float(emi_amount),
        "foir": float(foir),
        "avg_balance": float(df["AccountBalance"].mean()),
        "min_balance": float(df["AccountBalance"].min()),
        "num_transactions": int(len(df)),
        "num_emi_txns": int(emi_mask.sum()),
        "customer_age": int(customer_age),

        # Stability-model extras
        "income_volatility": float(income_volatility),
        "missed_payments": int(missed_payments),
        "num_credit_lines": int(num_credit_lines),
        "hidden_debt_risk": float(hidden_debt_risk),
        "foir_current": float(foir_current),
        "foir_new": float(foir_new),

        # Hidden-debt-model features
        "bnpl_txn_count": int(bnpl_txn_count),
        "microloan_txn_count": int(microloan_txn_count),
        "bnpl_spend": float(bnpl_spend),
        "microloan_spend": float(microloan_spend),
        "hidden_emi_amount": float(hidden_emi_amount),
        "hidden_emi_to_income_ratio": float(hidden_emi_to_income_ratio),
        "wallet_credit_usage": float(wallet_credit_usage),
        "freq_new_credit": int(freq_new_credit),
        "high_risk_merchants": int(high_risk_merchants),
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
        "probability_high": float(probs[2]),
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
        "is_financially_stable": pred,
    }


# ===============================================================
# PREDICT HIDDEN DEBT
# ===============================================================
def predict_hidden_debt(features_dict):
    row = np.array([[features_dict[f] for f in FEATURES_HIDDEN]])
    prob = MODEL_HIDDEN.predict_proba(row)[0][1]

    return {
        "hidden_debt_risk_probability": float(round(prob, 4)),
        "high_hidden_debt_risk": bool(prob >= 0.5),
    }


# ===============================================================
# FULL RISK ANALYSIS (combines all 3 models)
# ===============================================================
def run_full_risk_analysis(features_dict: dict):
    """
    Runs all 3 models and combines them into a single risk signal
    that can be used by the loan officer UI.
    """

    # 1) Run individual models
    emi = predict_emi_stress(features_dict)
    stability = predict_stability(features_dict)
    hidden = predict_hidden_debt(features_dict)

    # 2) Convert outputs into numeric risk components in [0, 1]
    label_to_risk = {"LOW": 0.1, "MEDIUM": 0.5, "HIGH": 0.9}
    emi_risk = label_to_risk.get(emi["emi_stress_label"], 0.5)

    stability_risk = 1.0 - stability["financial_stability_probability"]
    hidden_risk = hidden["hidden_debt_risk_probability"]

    # 3) Weighted combination
    overall = 0.4 * emi_risk + 0.4 * stability_risk + 0.2 * hidden_risk
    overall = float(max(0.0, min(1.0, overall)))  # clamp to [0, 1]

    # 4) Bucket + recommendation
    if overall < 0.3:
        bucket = "LOW"
        recommendation = (
            "Customer looks low-risk: EMI burden and hidden debt are manageable. "
            "Likely safe to approve the requested loan with standard terms."
        )
    elif overall < 0.6:
        bucket = "MEDIUM"
        recommendation = (
            "Customer has moderate risk. Consider lower ticket size, shorter tenure, "
            "or ask for extra documentation / co-borrower."
        )
    else:
        bucket = "HIGH"
        recommendation = (
            "Customer is high-risk. Recommend manual review, stricter terms, or "
            "rejecting this loan unless strong compensating factors exist."
        )

    return {
        "emi_stress": emi,
        "stability": stability,
        "hidden_debt": hidden,
        "overall_risk": {
            "overall_risk_score": overall,
            "risk_bucket": bucket,
            "recommendation": recommendation,
            "components": {
                "emi_risk_component": float(round(emi_risk, 4)),
                "stability_risk_component": float(round(stability_risk, 4)),
                "hidden_debt_component": float(round(hidden_risk, 4)),
            },
        },
    }
