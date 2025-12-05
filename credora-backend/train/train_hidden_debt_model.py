import os
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
import joblib
from sim_data_utils import simulate_user_statement

os.makedirs("../models", exist_ok=True)

np.random.seed(123)
N_USERS = 2000

rows = []

# -----------------------------------------------------------
# Generate synthetic hidden-debt features
# -----------------------------------------------------------
for uid in range(N_USERS):
    profile, df = simulate_user_statement(uid, n_months=6)

    # Income (needed for scaling)
    income = df[
        df["description"].str.contains("salary", case=False, na=False)
        & (df["type"] == "credit")
    ]["amount"].sum()
    income = float(max(5000, income / 6))

    desc = df["description"].astype(str).str.lower()

    # BNPL & Microloan patterns
    bnpl_mask = desc.str.contains("paylater|zest|slice|simpl|bnpl", na=False)
    micro_mask = desc.str.contains("kreditbee|earlysalary|moneytap|dhani|cashbean", na=False)

    bnpl_txn_count = int(bnpl_mask.sum())
    microloan_txn_count = int(micro_mask.sum())

    bnpl_spend = float(df.loc[bnpl_mask & (df["type"] == "debit"), "amount"].abs().sum())
    microloan_spend = float(
        df.loc[micro_mask & (df["type"] == "debit"), "amount"].abs().sum()
    )

    hidden_emi_amount = (bnpl_spend + microloan_spend) / 6.0
    hidden_emi_to_income_ratio = hidden_emi_amount / max(income, 1)

    # Wallet/UPI spending patterns
    wallet_credit_usage = float(
        df[df["description"].str.contains("wallet|paytm|phonepe|gpay", case=False, na=False)]["amount"]
        .abs()
        .sum()
    )

    # New credit frequency = number of loan disbursal messages
    freq_new_credit = int(df["description"].str.contains("Loan Disbursal", case=False, na=False).sum())

    high_risk_merchants = bnpl_txn_count + microloan_txn_count

    rows.append(
        {
            "bnpl_txn_count": bnpl_txn_count,
            "microloan_txn_count": microloan_txn_count,
            "bnpl_spend": bnpl_spend,
            "microloan_spend": microloan_spend,
            "hidden_emi_amount": hidden_emi_amount,
            "hidden_emi_to_income_ratio": hidden_emi_to_income_ratio,
            "wallet_credit_usage": wallet_credit_usage,
            "freq_new_credit": freq_new_credit,
            "high_risk_merchants": high_risk_merchants,
        }
    )

# -----------------------------------------------------------
# Convert to DataFrame
# -----------------------------------------------------------
df_feat = pd.DataFrame(rows)
df_feat = df_feat.replace([np.inf, -np.inf], np.nan).dropna()

# -----------------------------------------------------------
# AUTO-GENERATED BALANCED LABEL (like stability model)
# -----------------------------------------------------------
df_feat["risk_score"] = (
    df_feat["hidden_emi_to_income_ratio"] * 0.5
    + df_feat["bnpl_txn_count"] * 0.2
    + df_feat["microloan_txn_count"] * 0.2
    + df_feat["freq_new_credit"] * 0.1
)

df_feat = df_feat.sort_values("risk_score", ascending=False)

# Top 30% are high hidden debt risk
cutoff = int(len(df_feat) * 0.30)

df_feat["hidden_risk"] = 0
df_feat.iloc[:cutoff, df_feat.columns.get_loc("hidden_risk")] = 1

print("\nLabel Distribution:")
print(df_feat["hidden_risk"].value_counts(), "\n")

# -----------------------------------------------------------
# Prepare features
# -----------------------------------------------------------
FEATURES_HIDDEN = [
    "bnpl_txn_count",
    "microloan_txn_count",
    "bnpl_spend",
    "microloan_spend",
    "hidden_emi_amount",
    "hidden_emi_to_income_ratio",
    "wallet_credit_usage",
    "freq_new_credit",
    "high_risk_merchants",
]

X = df_feat[FEATURES_HIDDEN]
y = df_feat["hidden_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------------------------------------
# Train XGBoost
# -----------------------------------------------------------
model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="binary:logistic",
    eval_metric="logloss",
)

model.fit(X_train, y_train)

probs = model.predict_proba(X_test)[:, 1]
preds = (probs > 0.5).astype(int)

print("AUC:", roc_auc_score(y_test, probs))
print("ACC:", accuracy_score(y_test, preds))

joblib.dump(model, "../models/hidden_debt_model.joblib")
print("Saved hidden_debt_model.joblib")

# Save features
import json
with open("../models/hidden_features.json", "w") as f:
    json.dump(FEATURES_HIDDEN, f)
print("Saved hidden_features.json")
