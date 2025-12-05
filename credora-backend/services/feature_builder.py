import pandas as pd
import numpy as np

def extract_features_from_csv(df: pd.DataFrame):
    """
    Takes the uploaded bank statement CSV and converts it into
    a SINGLE unified feature dictionary for all 3 ML models:
    - stability model
    - hidden debt model
    - emi stress model
    """

    # Normalize columns
    df.columns = df.columns.str.strip().str.lower()

    # Fix date fields
    if "transactiondate" in df.columns:
        df["transactiondate"] = pd.to_datetime(df["transactiondate"], errors="coerce")

    df = df.dropna(subset=["transactiondate"])

    # Fix amounts
    for col in ["transactionamount", "accountbalance"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(subset=["transactionamount", "accountbalance"], inplace=True)

    # Detect credit/debit
    if "transactiontype" in df.columns:
        df["transactiontype"] = df["transactiontype"].astype(str).str.lower()
        df["is_credit"] = df["transactiontype"].str.contains("credit").astype(int)
        df["is_debit"] = df["transactiontype"].str.contains("debit").astype(int)
    else:
        df["is_credit"] = (df["transactionamount"] > 0).astype(int)
        df["is_debit"] = (df["transactionamount"] < 0).astype(int)

    df["month"] = df["transactiondate"].dt.to_period("M")

    # ---- MONTHLY AGGREGATION ----
    monthly = df.groupby("month").agg(
        income=("transactionamount", lambda s: s[df.loc[s.index, "is_credit"] == 1].sum()),
        expense=("transactionamount", lambda s: abs(s[df.loc[s.index, "is_debit"] == 1].sum())),
        emi_amount=("transactionamount",
                    lambda s: abs(s[df.loc[s.index, "is_emi"]] if "is_emi" in df.columns else 0)),
        avg_balance=("accountbalance", "mean"),
        min_balance=("accountbalance", "min"),
        num_transactions=("transactionamount", "count")
    ).reset_index()

    if len(monthly) == 0:
        raise ValueError("CSV does not contain valid monthly data.")

    # Use last month as snapshot
    row = monthly.iloc[-1]

    # Derived features
    income = float(row["income"])
    expense = float(row["expense"])
    net_savings = income - expense
    savings_rate = net_savings / income if income > 0 else 0
    foir = row["emi_amount"] / income if income > 0 else 0

    # Return a unified dict
    return {
        # Stability features
        "income": income,
        "expense": expense,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "savings_months": (net_savings / expense) if expense > 0 else 0,
        "income_volatility": 0.1,  # placeholder
        "missed_payments": 0,      # placeholder
        "customer_age": 30,
        "num_credit_lines": 1,
        "hidden_debt_risk": 0.01,
        "foir_current": foir,
        "foir_new": foir,

        # Hidden debt features
        "bnpl_txn_count": 0,
        "microloan_txn_count": 0,
        "bnpl_spend": 0,
        "microloan_spend": 0,
        "hidden_emi_amount": float(row["emi_amount"]),
        "hidden_emi_to_income_ratio": foir,
        "wallet_credit_usage": 0,
        "freq_new_credit": 0,
        "high_risk_merchants": 0,

        # EMI features
        "emi_amount": float(row["emi_amount"]),
        "foir": foir,
        "avg_balance": float(row["avg_balance"]),
        "min_balance": float(row["min_balance"]),
        "num_emi_txns": 0,
        "num_transactions": int(row["num_transactions"]),
    }
