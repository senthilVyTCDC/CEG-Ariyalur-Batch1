import pandas as pd
import xgboost as xgb
import pickle
import mysql.connector

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="soni",
    password="1234",
    database="creditcardfraud"
)

# Load data
df = pd.read_sql("SELECT * FROM transactions_", db)

# ---------------- FEATURE ENGINEERING ----------------
df["hour"] = pd.to_datetime(df["transaction_time"]).dt.hour

# ---------------- CREATE LABEL ----------------
df["fraud"] = (
    (df["amount"] > df["user_avg_transaction_amount"] * 3) |
    (df["last_transaction_gap"] < 60)
).astype(int)

# ---------------- FEATURES ----------------
X = df[[
    "amount",
    "transaction_frequency",
    "last_transaction_gap",
    "user_avg_transaction_amount",
    "hour"
]]

y = df["fraud"]

# ---------------- TRAIN MODEL ----------------
model = xgb.XGBClassifier()
model.fit(X, y)

# ---------------- SAVE MODEL ----------------
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained and saved successfully")