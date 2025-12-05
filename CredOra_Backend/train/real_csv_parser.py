import pandas as pd
import re

def detect_bank_format(df):
    cols = [c.lower() for c in df.columns]

    if "narration" in cols and "debit" in cols and "credit" in cols:
        return "HDFC"

    if "value date" in cols and "description" in cols:
        return "SBI"

    if "transaction remarks" in cols:
        return "ICICI"

    if "particulars" in cols:
        return "AXIS"

    return "GENERIC"


def parse_to_standard_format(df):
    bank = detect_bank_format(df)

    df = df.copy()

    # HDFC Format
    if bank == "HDFC":
        df["amount"] = df["credit"].fillna(0) - df["debit"].fillna(0)
        df["type"] = df["amount"].apply(lambda x: "credit" if x > 0 else "debit")

        return df.rename(columns={
            "date": "date",
            "narration": "description",
            "balance": "balance"
        })[["date", "description", "amount", "type", "balance"]]

    # SBI Format
    elif bank == "SBI":
        df["amount"] = df["credit"].fillna(0) - df["debit"].fillna(0)
        df["type"] = df["amount"].apply(lambda x: "credit" if x > 0 else "debit")

        return df.rename(columns={
            "txn date": "date",
            "description": "description",
            "balance": "balance"
        })[["date", "description", "amount", "type", "balance"]]

    # ICICI Format
    elif bank == "ICICI":
        df["type"] = df["amount"].apply(lambda x: "credit" if x > 0 else "debit")
        return df.rename(columns={
            "date": "date",
            "transaction remarks": "description"
        })[["date", "description", "amount", "type", "balance"]]

    # Axis Format
    elif bank == "AXIS":
        df["type"] = df["amount"].apply(lambda x: "credit" if x > 0 else "debit")
        return df.rename(columns={"particulars": "description"})[
            ["date", "description", "amount", "type", "balance"]
        ]

    # Generic
    else:
        df["type"] = df["amount"].apply(lambda x: "credit" if x > 0 else "debit")
        return df[["date", "description", "amount", "type", "balance"]]
