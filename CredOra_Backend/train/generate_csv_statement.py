import argparse
import os
from sim_data_utils import simulate_user_statement

os.makedirs("../sample_statements", exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--user_id", type=int, default=1)
parser.add_argument("--months", type=int, default=6)
parser.add_argument("--risk", type=str, default="medium", choices=["low", "medium", "high", "random"])

args = parser.parse_args()

profile, df = simulate_user_statement(user_id=args.user_id, n_months=args.months, risk=args.risk)

filename = f"../sample_statements/user_{args.user_id}_{args.risk}_risk.csv"
df.to_csv(filename, index=False)
print(f"Generated CSV: {filename}")
print("Profile:", profile)
