import streamlit as st
import requests
import pandas as pd
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Fraud Detection System", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Users"

menu = st.sidebar.selectbox("Module", [
    "Users",
    "Cards",
    "Transactions",
    "Fraud Detection",
    "Fraud Alerts"
])

# ================= USERS =================
if menu == "Users":

    st.header("👤 Users")

    if st.button("Load Users"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/users").json())
        if not df.empty:
            st.dataframe(df)

            st.subheader("📊 Account Type Distribution")
            st.bar_chart(df["account_type"].value_counts())

            df["age_group"] = df["age"].apply(
                lambda x: "Below 25" if x < 25 else "25-50" if x <= 50 else "Above 50"
            )

            st.subheader("📊 Age Group Distribution")
            st.bar_chart(df["age_group"].value_counts())

    with st.expander("➕ Add User"):
        uid = st.number_input("User ID", key="u1")
        name = st.text_input("Name", key="u2")
        phone = st.text_input("Phone", key="u3")
        age = st.number_input("Age", key="u4")
        acc = st.selectbox("Account Type", ["savings","current","premium"], key="u5")
        days = st.number_input("Account Age Days", key="u6")

        if st.button("Add User"):
            requests.post(f"{BASE_URL}/users", json={
                "user_id": uid,
                "name": name,
                "phone": phone,
                "age": age,
                "account_type": acc,
                "account_age_days": days
            })
            st.success("User Added")

    with st.expander("✏️ Update User"):
        uid = st.number_input("User ID", key="u7")
        name = st.text_input("New Name", key="u8")
        phone = st.text_input("New Phone", key="u9")
        age = st.number_input("New Age", key="u10")
        acc = st.selectbox("Account Type", ["savings","current","premium"], key="u11")
        days = st.number_input("Account Age Days", key="u12")

        if st.button("Update User"):
            requests.put(f"{BASE_URL}/users/{int(uid)}", json={
                "name": name,
                "phone": phone,
                "age": age,
                "account_type": acc,
                "account_age_days": days
            })
            st.success("User Updated")

    with st.expander("🗑 Delete User"):
        uid = st.number_input("User ID", key="u13")
        if st.button("Delete User"):
            requests.delete(f"{BASE_URL}/users/{int(uid)}")
            st.success("User Deleted")

# ================= CARDS =================
elif menu == "Cards":

    st.header("💳 Cards")

    if st.button("Load Cards"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/cards").json())
        if not df.empty:
            st.dataframe(df)

            st.subheader("📊 Card Limit Distribution")
            st.bar_chart(df["card_limit"].value_counts())

    with st.expander("➕ Add Card"):
        cid = st.number_input("Card ID", key="c1")
        uid = st.number_input("User ID", key="c2")
        limit = st.selectbox("Limit", [50000,100000,150000,200000], key="c3")
        status = st.selectbox("Status", ["active","blocked"], key="c4")
        freq = st.number_input("Usage Frequency", key="c5")

        if st.button("Add Card"):
            requests.post(f"{BASE_URL}/cards", json={
                "card_id": cid,
                "user_id": uid,
                "card_limit": limit,
                "card_status": status,
                "usage_frequency": freq
            })
            st.success("Card Added")

    with st.expander("✏️ Update Card"):
        cid = st.number_input("Card ID", key="c6")
        limit = st.selectbox("Limit", [50000,100000,150000,200000], key="c7")
        status = st.selectbox("Status", ["active","blocked"], key="c8")
        freq = st.number_input("Usage Frequency", key="c9")

        if st.button("Update Card"):
            requests.put(f"{BASE_URL}/cards/{int(cid)}", json={
                "card_limit": limit,
                "card_status": status,
                "usage_frequency": freq
            })
            st.success("Card Updated")

    with st.expander("🗑 Delete Card"):
        cid = st.number_input("Card ID", key="c10")
        if st.button("Delete Card"):
            requests.delete(f"{BASE_URL}/cards/{int(cid)}")
            st.success("Card Deleted")

# ================= TRANSACTIONS =================
elif menu == "Transactions":

    st.header("💸 Transactions")

    if st.button("Load Transactions"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/transactions").json())
        if not df.empty:
            st.dataframe(df)

            st.subheader("📈 Transaction Amount Over Time")
            df["transaction_time"] = pd.to_datetime(df["transaction_time"])
            st.line_chart(df.set_index("transaction_time")["amount"])

            st.subheader("📊 Transaction Type Distribution")
            st.bar_chart(df["transaction_type"].value_counts())

            st.subheader("📊 Device Usage Distribution")
            st.bar_chart(df["device_type"].value_counts())

    with st.expander("➕ Add Transaction"):
        tid = st.number_input("Transaction ID", key="t1")
        uid = st.number_input("User ID", key="t2")
        cid = st.number_input("Card ID", key="t3")
        mid = st.number_input("Merchant ID", key="t4")
        amt = st.number_input("Amount", key="t5")
        time = st.text_input("Transaction Time (YYYY-MM-DD HH:MM:SS)",value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),key="t6")

        loc = st.selectbox("Location",
            ["Chennai","Delhi","Mumbai","Bangalore","Hyderabad"], key="t7")

        dev = st.selectbox("Device",
            ["mobile","ATM","POS"], key="t8")

        typ = st.selectbox("Type",
            ["online","withdrawal","swipe"], key="t9")

        freq = st.number_input("Transaction Frequency", min_value=1, value=1, key="t10")

        if st.button("Add Transaction"):
            res = requests.post(f"{BASE_URL}/transactions", json={
                "transaction_id": tid,
                "user_id": uid,
                "card_id": cid,
                "merchant_id": mid,
                "amount": amt,
                "transaction_time": time,
                "location": loc,
                "device_type": dev,
                "transaction_type": typ,
                "transaction_frequency": freq
            }).json()

            st.success(f"Fraud Probability: {res['fraud_probability']:.2f}")

# ================= FRAUD DETECTION =================
elif menu == "Fraud Detection":

    st.header("⚠️ Fraud Detection")

    if st.button("Run Detection"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/detect_fraud").json())
        if not df.empty:
            st.dataframe(df)

            st.subheader("📊 Fraud vs Normal")
            st.bar_chart(df["status"].value_counts())

# ================= FRAUD ALERTS =================
elif menu == "Fraud Alerts":

    st.header("🚨 Fraud Alerts")

    if st.button("Load Alerts"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/alerts").json())
        if not df.empty:
            st.dataframe(df)

            st.subheader("📊 Alert Distribution")
            st.bar_chart(df["alert_status"].value_counts())