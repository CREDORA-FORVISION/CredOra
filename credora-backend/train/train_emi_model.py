import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import json

# Make sure models folder exists
os.makedirs("../models", exist_ok=True)

print("\n=== LOADING DATASET ===")
df = pd.read_csv("bank_transactions_data_2.csv")   # CSV must be in same folder

print("Columns in dataset:", df.columns.tolist())

# -------------------------------------------------------
# 1. Clean & Preprocess Transaction Data
# -------------------------------------------------------
df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], errors="coerce")
df = df.dropna(subset=["TransactionDate"])

# Convert numeric columns
for col in ["TransactionAmount", "AccountBalance"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["TransactionAmount", "AccountBalance"])

# Add credit/debit flags if missing
if "is_credit" not in df.columns:
    df["TransactionType"] = df["TransactionType"].astype(str).str.lower()
    df["is_credit"] = df["TransactionType"].str.contains("credit").astype(int)
    df["is_debit"] = df["TransactionType"].str.contains("debit").astype(int)

# -------------------------------------------------------
# 2. EMI Detection (3 repeating debits = EMI)
# -------------------------------------------------------
debits = df[df["is_debit"] == 1].copy()
debits["emi_candidate_count"] = debits.groupby(
    ["AccountID", "TransactionAmount"]
)["TransactionID"].transform("count")

debits["is_emi"] = (debits["emi_candidate_count"] >= 3).astype(int)

df = df.merge(
    debits[["TransactionID", "is_emi"]],
    on="TransactionID",
    how="left"
)
df["is_emi"] = df["is_emi"].fillna(0).astype(int)

print("Detected EMI transactions:", df["is_emi"].sum())

# -------------------------------------------------------
# 3. Monthly Aggregation (FIXED VERSION)
# -------------------------------------------------------
df["Month"] = df["TransactionDate"].dt.to_period("M")

def sum_credit(series):
    mask = df.loc[series.index, "is_credit"] == 1
    return series[mask].sum()

def sum_debit(series):
    mask = df.loc[series.index, "is_debit"] == 1
    return abs(series[mask]).sum()  # FIX

def sum_emi(series):
    mask = df.loc[series.index, "is_emi"] == 1
    return abs(series[mask]).sum()  # FIX

monthly = df.groupby(["AccountID", "Month"]).agg(
    income=("TransactionAmount", sum_credit),
    expense=("TransactionAmount", sum_debit),
    emi_amount=("TransactionAmount", sum_emi),
    num_emi_txns=("is_emi", "sum"),
    num_transactions=("TransactionID", "count"),
    avg_balance=("AccountBalance", "mean"),
    min_balance=("AccountBalance", "min"),
    customer_age=("CustomerAge", "mean"),
).reset_index()

# -------------------------------------------------------
# 4. Derived features (RESTORED BLOCK)
# -------------------------------------------------------
monthly["net_savings"] = monthly["income"] - monthly["expense"]

monthly["savings_rate"] = np.where(
    monthly["income"] > 0,
    monthly["net_savings"] / monthly["income"],
    0
)

monthly["foir"] = np.where(
    monthly["income"] > 0,
    monthly["emi_amount"] / monthly["income"],
    0
)

monthly.replace([np.inf, -np.inf], 0, inplace=True)
monthly.fillna(0, inplace=True)

# -------------------------------------------------------
# 5. EMI STRESS LABELING (Finally works)
# -------------------------------------------------------
def emi_stress_label(foir):
    if foir < 0.20:
        return 0  # low
    elif foir < 0.40:
        return 1  # medium
    else:
        return 2  # high

monthly["emi_stress_label"] = monthly["foir"].apply(emi_stress_label)

print("\nSample Labels:")
print(monthly[["AccountID", "foir", "emi_stress_label"]].head())

# -------------------------------------------------------
# 6. Feature Selection
# -------------------------------------------------------
FEATURES_EMI = [
    "income",
    "expense",
    "net_savings",
    "savings_rate",
    "emi_amount",
    "foir",
    "avg_balance",
    "min_balance",
    "num_transactions",
    "num_emi_txns",
    "customer_age"
]

X = monthly[FEATURES_EMI]
y = monthly["emi_stress_label"]

# -------------------------------------------------------
# 7. Train/Test split
# -------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

# -------------------------------------------------------
# 8. Train Model
# -------------------------------------------------------
clf = RandomForestClassifier(
    n_estimators=250,
    random_state=42,
    class_weight="balanced"
)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("\n=== EMI Stress Classification Report ===")
print(classification_report(y_test, y_pred))

print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

# -------------------------------------------------------
# 9. Save Model + Feature List
# -------------------------------------------------------
joblib.dump(clf, "../models/emi_stress_model.joblib")
print("Saved emi_stress_model.joblib")

with open("../models/emi_stress_features.json", "w") as f:
    json.dump(FEATURES_EMI, f)

print("Saved emi_stress_features.json")
print("\n=== DONE ===")
