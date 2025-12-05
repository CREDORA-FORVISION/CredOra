import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

N_ACCOUNTS = 300        # number of synthetic users
MONTHS = 6              # number of months to simulate
ROWS_PER_MONTH = 40     # total transactions per month

occupations = [
    "Engineer", "Teacher", "Student", "Doctor", "Sales",
    "Manager", "Designer", "Nurse", "Technician", "Analyst"
]

data = []
tid = 1

for acc in range(1, N_ACCOUNTS + 1):
    age = random.randint(21, 60)
    occupation = random.choice(occupations)

    # Base salary is different per user
    salary = random.randint(20000, 90000)

    # Generate EMI amount based on intended FOIR class → balanced labels
    stress_class = random.choice([0, 1, 2])   # LOW, MED, HIGH

    if stress_class == 0:         # LOW EMI stress → FOIR < 0.2
        emi_value = random.randint(1000, int(salary * 0.15))
    elif stress_class == 1:       # MEDIUM EMI stress → FOIR 0.2–0.4
        emi_value = random.randint(int(salary * 0.20), int(salary * 0.35))
    else:                         # HIGH EMI stress → FOIR > 0.4
        emi_value = random.randint(int(salary * 0.40), int(salary * 0.70))

    # Convert EMI value (positive) → transaction debit will be negative later
    emi_amount_positive = emi_value

    # Starting balance per user
    base_balance = random.randint(30000, 120000)

    for m in range(MONTHS):
        month_start = datetime(2024, 1, 1) + timedelta(days=30 * m)

        # ----------- Salary Credit -----------
        salary_credit = salary
        balance = base_balance + salary_credit

        data.append([
            tid,
            month_start + timedelta(days=1),
            salary_credit,
            "credit",
            balance,
            acc,
            age,
            occupation
        ])
        tid += 1

        # ----------- EMI Transactions (3 repeating → EMI detection) -----------
        for i in range(3):
            balance -= emi_amount_positive
            data.append([
                tid,
                month_start + timedelta(days=5 + i),
                -emi_amount_positive,     # debit entry
                "debit",
                balance,
                acc,
                age,
                occupation
            ])
            tid += 1

        # ----------- Additional Expenses -----------
        for i in range(ROWS_PER_MONTH - 4):
            amt = random.randint(200, 5000)
            balance -= amt

            data.append([
                tid,
                month_start + timedelta(days=random.randint(2, 28)),
                -amt,                     # expense debit
                "debit",
                balance,
                acc,
                age,
                occupation
            ])
            tid += 1

        base_balance = balance  # carry forward to next month

# ----------- Save CSV -----------
df = pd.DataFrame(data, columns=[
    "TransactionID",
    "TransactionDate",
    "TransactionAmount",
    "TransactionType",
    "AccountBalance",
    "AccountID",
    "CustomerAge",
    "CustomerOccupation"
])

df.to_csv("bank_transactions_data_2.csv", index=False)

print("\nGenerated CSV Successfully!")
print("Rows:", len(df))
print("Saved as: bank_transactions_data_2.csv")
