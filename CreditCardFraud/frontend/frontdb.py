import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

# ================= SESSION =================
if "main_page" not in st.session_state:
    st.session_state.main_page = "HOME"

if "sub_page" not in st.session_state:
    st.session_state.sub_page = None

# ================= SIDEBAR =================
st.sidebar.title("📊 Dashboard")

st.session_state.main_page = st.sidebar.radio("Navigation", [
    "HOME",
    "KEY METRICS",
    "FILTERS",
    "ANALYTICS",
    "RECENT FRAUD ALERTS",
    "INSIGHTS"
])

# ================= API =================
def fetch_data(endpoint):
    try:
        res = requests.get(f"{BASE_URL}/{endpoint}")
        return pd.DataFrame(res.json())
    except:
        return pd.DataFrame()

def post_data(endpoint, payload):
    try:
        res = requests.post(f"{BASE_URL}/{endpoint}", json=payload)
        return res.json()
    except:
        return {"message": "Error"}

# ================= LOAD DATA =================
users_df = fetch_data("users")
cards_df = fetch_data("cards")
transactions_df = fetch_data("transactions")

# ================= SAFE FRAUD =================
if not transactions_df.empty:
    if "amount" in transactions_df.columns:
        transactions_df["is_fraud"] = transactions_df["amount"].apply(lambda x: 1 if x > 50000 else 0)
    else:
        transactions_df["is_fraud"] = 0

# ================= BACK BUTTON =================
if st.session_state.sub_page:
    if st.button("⬅ Back to Dashboard"):
        st.session_state.sub_page = None
        st.rerun()

# ================= HOME =================
if st.session_state.main_page == "HOME" and not st.session_state.sub_page:

    st.title("🏠 Home Dashboard")

    option = st.selectbox("Select Module", [
        "Users",
        "Cards",
        "Transactions"
    ])

    if st.button("Open Module"):
        st.session_state.sub_page = option
        st.rerun()

# ================= USERS =================
if st.session_state.sub_page == "Users":
    st.header("👤 Users")

    st.subheader("➕ Add User")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        user_id = st.number_input("User ID", step=1)

    with col2:
        avg_spend = st.number_input("Avg Monthly Spend")
        age = st.number_input("Age")
        acc_age_days = st.number_input("Account Age (Days)")
        acc_type = st.selectbox("Account Type", ["Savings", "Current"])

    if st.button("Add User"):
        if name and phone:
         payload = {
            "name": name,
            "phone_number": phone,
            "user_id": user_id,
            "avg_monthly_spend": avg_spend,
            "age": age,
            "acc_age_days": acc_age_days,
            "acc_type": acc_type
        }
        post_data("users", payload)
        st.success("✅ User Added Successfully")


    st.divider()
    st.dataframe(users_df)

# ================= CARDS =================
elif st.session_state.sub_page == "Cards":
    st.header("💳 Cards")

    st.subheader("➕ Add Card")

    col1, col2 = st.columns(2)

    with col1:
        user_id = st.number_input("User ID", step=1)
        card_id = st.number_input("Card ID", step=1)
        card_limit = st.number_input("Card Limit")

    with col2:
        card_status = st.selectbox("Card Status", ["Active", "Blocked"])
        usage_frequency = st.number_input("Usage Frequency")

    if st.button("Add Card"):
        if user_id and card_id:
         payload = {
            "user_id": user_id,
            "card_id": card_id,
            "card_limit": card_limit,
            "card_status": card_status,
            "usage_frequency": usage_frequency
        }
        post_data("cards", payload)
        st.success("✅ Card Added Successfully")
        st.rerun()



    st.divider()
    st.dataframe(cards_df)

# ================= TRANSACTIONS =================
elif st.session_state.sub_page == "Transactions":
    st.header("💰 Transactions")

    st.subheader("➕ Add Transaction")

    col1, col2, col3 = st.columns(3)

    with col1:
        transaction_id = st.number_input("Transaction ID", step=1)
        user_id = st.number_input("User ID", step=1)
        card_id = st.number_input("Card ID", step=1)
        amount = st.number_input("Amount")

    with col2:
        transaction_type = st.selectbox("Transaction Type", ["Online", "POS", "ATM"])
        device_type = st.selectbox("Device Type", ["Mobile", "Laptop", "ATM"])
        location = st.text_input("Location")

    with col3:
        merchant_id = st.number_input("Merchant ID", step=1)

    if st.button("Add Transaction"):
        if user_id and card_id and amount:
         payload = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "card_id": card_id,
            "amount": amount,
            "transaction_type": transaction_type,
            "device_type": device_type,
            "location": location,
            "merchant_id": merchant_id
        }
        post_data("transactions", payload)
        st.success("✅ Transaction Added Successfully")
        st.rerun()


    st.divider()
    st.dataframe(transactions_df)

# ================= KEY METRICS =================
elif st.session_state.main_page == "KEY METRICS":

    st.title("📌 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Users", len(users_df))
    col2.metric("Cards", len(cards_df))
    col3.metric("Transactions", len(transactions_df))
    col4.metric("Frauds", transactions_df["is_fraud"].sum())

# ================= FILTERS =================
elif st.session_state.main_page == "FILTERS":

    st.title("🔍 Filters")

    if not transactions_df.empty and "location" in transactions_df.columns and "device_type" in transactions_df.columns:

        location = st.selectbox("Location", transactions_df["location"].dropna().unique())
        device = st.selectbox("Device", transactions_df["device_type"].dropna().unique())

        filtered = transactions_df[
            (transactions_df["location"] == location) &
            (transactions_df["device_type"] == device)
        ]

        st.dataframe(filtered)

    else:
        st.warning("Required columns not available")

# ================= ANALYTICS =================
elif st.session_state.main_page == "ANALYTICS":

    st.title("📊 Analytics")

    if not transactions_df.empty:

        chart = st.selectbox("Select Chart", [
            "Fraud vs Normal",
            "Top Locations",
            "Device Usage"
        ])

        if chart == "Fraud vs Normal":
            fig = px.pie(transactions_df, names="is_fraud")
            st.plotly_chart(fig, use_container_width=True)

        elif chart == "Top Locations" and "location" in transactions_df.columns:
            loc = transactions_df["location"].value_counts().reset_index()
            loc.columns = ["location", "count"]
            fig = px.bar(loc, x="location", y="count")
            st.plotly_chart(fig, use_container_width=True)

        elif chart == "Device Usage" and "device_type" in transactions_df.columns:
            dev = transactions_df["device_type"].value_counts().reset_index()
            dev.columns = ["device", "count"]
            fig = px.bar(dev, x="device", y="count")
            st.plotly_chart(fig, use_container_width=True)

# ================= ALERTS =================
elif st.session_state.main_page == "RECENT FRAUD ALERTS":

    st.title("🚨 Recent Fraud Alerts")

    frauds = transactions_df[transactions_df["is_fraud"] == 1]

    if not frauds.empty:
        st.dataframe(frauds.head(10))
    else:
        st.success("No fraud transactions detected")

# ================= INSIGHTS =================
elif st.session_state.main_page == "INSIGHTS":

    st.title("💡 Insights")

    total = len(transactions_df)
    fraud = transactions_df["is_fraud"].sum()

    st.success(f"Total Transactions: {total}")
    st.error(f"Fraud Transactions: {fraud}")

    if fraud > 0:
        st.warning("⚠️ Fraud activity detected")
    else:
        st.info("System looks safe ✅")