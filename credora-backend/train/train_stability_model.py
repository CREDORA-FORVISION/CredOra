import os
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
import joblib
from sim_data_utils import simulate_user_statement

os.makedirs("../models", exist_ok=True)

np.random.seed(42)
N_USERS = 2500

rows = []

# -----------------------------------------------------------
# Generate user features
# -----------------------------------------------------------
for uid in range(N_USERS):
    profile, df = simulate_user_statement(uid, n_months=6)

    income = df[
        df["description"].str.contains("salary", case=False, na=False)
        & (df["type"] == "credit")
    ]["amount"].sum()
    income = float(max(5000, income / 6))

    expense = float(df[df["type"] == "debit"]["amount"].abs().sum() / 6)

    net_savings = income - expense
    savings_rate = net_savings / max(income, 1)
    savings_months = net_savings / max(expense, 1)

    emi_txn = df[
        df["description"].str.contains("EMI", case=False, na=False)
        & (df["type"] == "debit")
    ]
    total_emi_amount = float(emi_txn["amount"].abs().sum() / 6)

    new_emi = float(np.random.uniform(1500, 7000))

    foir_current = total_emi_amount / max(income, 1)
    foir_new = (total_emi_amount + new_emi) / max(income, 1)

    monthly_sals = []
    for m in sorted(df["month_index"].unique()):
        sm = df[
            (df["month_index"] == m)
            & df["description"].str.contains("salary", case=False, na=False)
            & (df["type"] == "credit")
        ]["amount"].sum()
        monthly_sals.append(sm)

    income_volatility = (
        float(np.std(monthly_sals)) / max(np.mean(monthly_sals), 1)
        if monthly_sals else 0.2
    )

    low_balance_days = (df["balance"] < 1000).sum()
    missed_payments = int(low_balance_days > 5)

    num_credit_lines = int(
        df["description"].str.contains("Loan", case=False, na=False).any()
    ) + int(len(emi_txn) > 0)

    desc = df["description"].str.lower()
    bnpl_mask = desc.str.contains("paylater|zest|slice|simpl", na=False)
    micro_mask = desc.str.contains(
        "kreditbee|earlysalary|moneytap|dhani|cashbean", na=False
    )

    hidden_debt_risk = (bnpl_mask.sum() + micro_mask.sum()) / max(len(df), 1)

    age = profile["age"]

    rows.append(
        {
            "income": income,
            "expense": expense,
            "net_savings": net_savings,
            "savings_rate": savings_rate,
            "savings_months": savings_months,
            "income_volatility": income_volatility,
            "missed_payments": missed_payments,
            "customer_age": age,
            "num_credit_lines": num_credit_lines,
            "hidden_debt_risk": hidden_debt_risk,
            "foir_current": foir_current,
            "foir_new": foir_new,
        }
    )


# -----------------------------------------------------------
# Convert & clean
# -----------------------------------------------------------
df_feat = pd.DataFrame(rows)
df_feat = df_feat.replace([np.inf, -np.inf], np.nan).dropna()


# -----------------------------------------------------------
# **AUTO-GENERATED BALANCED LABELING**
# -----------------------------------------------------------
df_feat["risk_score"] = (
    df_feat["foir_new"] * 0.5
    + df_feat["hidden_debt_risk"] * 0.3
    + df_feat["missed_payments"] * 0.2
)

df_feat = df_feat.sort_values("risk_score")

# Top 35% = stable
cutoff = int(len(df_feat) * 0.35)
df_feat["stable"] = 0
df_feat.iloc[:cutoff, df_feat.columns.get_loc("stable")] = 1

print("\nLabel Distribution:")
print(df_feat["stable"].value_counts(), "\n")


# -----------------------------------------------------------
# Train model
# -----------------------------------------------------------
FEATURES_STAB = [
    "income",
    "expense",
    "net_savings",
    "savings_rate",
    "savings_months",
    "income_volatility",
    "missed_payments",
    "customer_age",
    "num_credit_lines",
    "hidden_debt_risk",
    "foir_current",
    "foir_new",
]

X = df_feat[FEATURES_STAB]
y = df_feat["stable"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.07,
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

joblib.dump(model, "../models/stability_model.joblib")
print("Saved stability_model.joblib")

import json
with open("../models/stability_features.json", "w") as f:
    json.dump(FEATURES_STAB, f)
print("Saved stability_features.json")
