import numpy as np
import pandas as pd
from datetime import datetime, timedelta

BNPL_MERCHANTS = [
    "ZestMoney", "Slice", "LazyPay", "Simpl",
    "Amazon PayLater", "Flipkart PayLater", "Jupiter PayLater"
]

MICROLOAN_MERCHANTS = [
    "KreditBee", "EarlySalary", "MoneyTap", "Dhani", "CASHe", "CashBean"
]

EXPENSE_MERCHANTS = [
    "Swiggy", "Zomato", "BigBazaar", "Reliance Trends",
    "Amazon", "Flipkart", "Fuel Station", "Electricity Board"
]


def simulate_user_profile(user_id, risk="medium"):
    if risk == "random":
        risk = np.random.choice(["low", "medium", "high"], p=[0.4, 0.4, 0.2])

    income = float(np.clip(np.random.normal(35000, 8000), 12000, 200000))
    age = int(np.random.randint(21, 60))
    has_emi = np.random.rand() < (0.3 if risk == "low" else 0.6)

    return {
        "user_id": user_id,
        "risk": risk,
        "base_income": income,
        "age": age,
        "has_emi": has_emi
    }


def simulate_month(profile, month_index, start_date, opening_balance):
    rows = []
    balance = opening_balance

    month_start = start_date + timedelta(days=30 * month_index)
    salary_day = np.random.randint(1, 5)
    salary_amt = float(np.clip(np.random.normal(profile["base_income"], profile["base_income"] * 0.1), 8000, 150000))

    for day in range(1, 31):
        date = month_start + timedelta(days=day - 1)

        # Salary
        if day == salary_day:
            balance += salary_amt
            rows.append([date, "Salary Credit", salary_amt, "credit", balance])

        # Expense patterns
        if profile["risk"] == "low":
            expense_count = np.random.poisson(2)
        elif profile["risk"] == "medium":
            expense_count = np.random.poisson(3)
        else:
            expense_count = np.random.poisson(4)

        for _ in range(expense_count):
            amt = float(max(100, np.random.exponential(900)))
            merchant = np.random.choice(EXPENSE_MERCHANTS)
            balance -= amt
            rows.append([date, merchant, -amt, "debit", balance])

        # EMI
        if profile["has_emi"] and day in [7, 15, 23]:
            emi_amt = float(np.random.uniform(2000, 9000))
            balance -= emi_amt
            rows.append([date, "Loan EMI HDFC", -emi_amt, "debit", balance])

        # BNPL transactions
        if profile["risk"] in ["medium", "high"] and np.random.rand() < 0.25:
            merchant = np.random.choice(BNPL_MERCHANTS)
            amt = float(np.random.uniform(500, 7000))
            balance -= amt
            rows.append([date, f"{merchant} Purchase", -amt, "debit", balance])

        # Microloan behaviour
        if profile["risk"] == "high" and np.random.rand() < 0.18:
            disb = float(np.random.uniform(3000, 15000))
            balance += disb
            rows.append([date, f"{np.random.choice(MICROLOAN_MERCHANTS)} Loan Disbursal", disb, "credit", balance])

            repay = disb * np.random.uniform(0.2, 0.6)
            balance -= repay
            rows.append([date, "Short-term Loan Repayment", -repay, "debit", balance])

    df = pd.DataFrame(rows, columns=["date", "description", "amount", "type", "balance"])
    return df, balance


def simulate_user_statement(user_id=1, n_months=6, risk="medium"):
    profile = simulate_user_profile(user_id, risk)
    balance = float(np.random.uniform(1000, 25000))
    start_date = datetime(2023, 1, 1)

    all_months = []
    for m in range(n_months):
        df_month, balance = simulate_month(profile, m, start_date, balance)
        df_month["month_index"] = m
        all_months.append(df_month)

    df_final = pd.concat(all_months, ignore_index=True)
    return profile, df_final
