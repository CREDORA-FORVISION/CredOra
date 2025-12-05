import pandas as pd
import numpy as np

BNPL_KEYS = ["bnpl", "paylater", "zest", "slice", "simpl"]
MICRO_KEYS = ["kreditbee", "cash", "loan", "micro"]

def extract_base_features(df: pd.DataFrame):
    df["amount"] = df["amount"].astype(float)

    income = df[df["type"]=="credit"]["amount"].sum()
    expense = df[df["type"]=="debit"]["amount"].abs().sum()

    net_savings = income - expense
    savings_rate = net_savings / max(income, 1)

    avg_balance = df["balance"].mean()
    min_balance = df["balance"].min()

    num_txn = len(df)

    emi_txn = df[df["description"].str.contains("emi", case=False, na=False)]
    num_emi_txn = len(emi_txn)

    return {
        "income": income,
        "expense": expense,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "avg_balance": float(avg_balance),
        "min_balance": float(min_balance),
        "num_transactions": num_txn,
        "num_emi_txns": num_emi_txn,
    }

def build_emi_features(base, emi_amount, customer_age):
    foir = (base["expense"] + emi_amount) / max(base["income"], 1)

    return {
        **base,
        "emi_amount": emi_amount,
        "foir": foir,
        "customer_age": customer_age
    }

def build_stability_features(base, existing_emi, new_emi, customer_age):
    foir_current = existing_emi / max(base["income"], 1)
    foir_new = (existing_emi + new_emi) / max(base["income"], 1)

    return {
        **base,
        "total_emi_amount": existing_emi,
        "new_emi_amount": new_emi,
        "foir_current": foir_current,
        "foir_new": foir_new,
        "savings_months": base["net_savings"]/max(base["expense"],1),
        "income_volatility": 0.2, # simplify
        "customer_age": customer_age
    }

def build_hidden_debt_features(df: pd.DataFrame, base):
    desc = df["description"].astype(str).str.lower()

    bnpl_txn = desc.str.contains("|".join(BNPL_KEYS)).sum()
    micro_txn = desc.str.contains("|".join(MICRO_KEYS)).sum()

    return {
        "bnpl_txn_count": int(bnpl_txn),
        "microloan_txn_count": int(micro_txn),
        "hidden_debt_ratio": (bnpl_txn + micro_txn) / max(base["income"], 1)
    }
