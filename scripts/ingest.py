import pandas as pd
import sqlalchemy
import redis
import pickle
import os

DB_URL = "mysql+pymysql://mlops_user:mlops_pass@127.0.0.1:3306/creditcard_db"
XLS_PATH = os.path.expanduser("~/mlops/data/default of credit card clients.xls")

# --- Read XLS (ETL - Extract) ---
print("Reading dataset...")
df = pd.read_excel(XLS_PATH, header=1)
print(f"Shape: {df.shape}")

# --- Transform ---
df.rename(columns={"default payment next month": "default_payment"}, inplace=True)
df.columns = df.columns.str.strip()

# --- Load into MariaDB flat table ---
print("Connecting to MariaDB...")
engine = sqlalchemy.create_engine(DB_URL)
df.to_sql("credit_card_default", con=engine, if_exists="replace", index=False)
print(f"Flat table loaded: {len(df)} rows")

# --- Load Star Schema ---
print("Loading Star Schema tables...")

dim_client = df[["ID", "SEX", "EDUCATION", "MARRIAGE", "AGE"]].copy()
dim_client.rename(columns={"ID": "client_id"}, inplace=True)
dim_client.to_sql("dim_client", con=engine, if_exists="replace", index=False)

dim_repayment = df[["ID", "PAY_0", "PAY_AMT1", "PAY_AMT2"]].copy()
dim_repayment.rename(columns={"ID": "repayment_id"}, inplace=True)
dim_repayment.to_sql("dim_repayment", con=engine, if_exists="replace", index=False)

fact = df[["ID", "ID", "LIMIT_BAL", "BILL_AMT1", "default_payment"]].copy()
fact.columns = ["client_id", "repayment_id", "LIMIT_BAL", "BILL_AMT1", "default_payment"]
fact.to_sql("fact_credit_default", con=engine, if_exists="replace", index=False)

print("Star schema populated.")

# --- Cache to Redis ---
print("Caching data to Redis...")
r = redis.Redis(host="127.0.0.1", port=6379)
r.set("raw_data", pickle.dumps(df))
print("Data cached to Redis successfully.")
print("Ingestion complete.")