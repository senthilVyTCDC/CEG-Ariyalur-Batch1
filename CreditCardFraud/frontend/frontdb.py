import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Fraud Detection System", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

if "module" not in st.session_state:
    st.session_state.module = None

def go_home():
    st.session_state.page = "home"
    st.session_state.module = None

def open_module(name):
    st.session_state.page = "module"
    st.session_state.module = name

def show_message(res):
    try:
        st.success(res.json().get("message", "Success"))
    except:
        st.error("Error occurred")

# ---------------- HOME ----------------
if st.session_state.page == "home":

    st.title("💳 Credit Card Fraud Detection System")
    st.write("Secure • Monitor • Detect Fraud")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👤 User"):
            open_module("user")
        if st.button("💳 Card"):
            open_module("card")

    with col2:
        if st.button("💰 Transaction"):
            open_module("transaction")
        if st.button("🚨 Fraud Monitor"):
            open_module("fraud")

# ---------------- MODULE ----------------
elif st.session_state.page == "module":

    module = st.session_state.module
    st.title(f"{module.upper()} MODULE")

    st.button("⬅ Back", on_click=go_home)

    option = st.radio("Operation", ["Create", "Read", "Update", "Delete"], horizontal=True)
    st.divider()

    # ================= USER =================
    if module == "user":

        if option == "Create":
            user_id = st.number_input("User ID")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

            if st.button("Submit"):
                res = requests.post(f"{BASE_URL}/users", json={
                    "user_id": int(user_id),
                    "name": name,
                    "email": email,
                    "phone": phone
                })
                show_message(res)

        elif option == "Read":
            if st.button("Load"):
                df = pd.DataFrame(requests.get(f"{BASE_URL}/users").json())
                st.dataframe(df, use_container_width=True)

                if not df.empty:
                    st.metric("Total Users", len(df))

        elif option == "Update":
            user_id = st.number_input("User ID")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

            if st.button("Update"):
                res = requests.put(f"{BASE_URL}/users/{int(user_id)}", json={
                    "name": name,
                    "email": email,
                    "phone": phone
                })
                show_message(res)

        elif option == "Delete":
            user_id = st.number_input("User ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/users/{int(user_id)}")
                show_message(res)

    # ================= CARD =================
    elif module == "card":

        if option == "Create":
            card_id = st.number_input("Card ID")
            user_id = st.number_input("User ID")
            card_number = st.text_input("Card Number")
            expiry = st.text_input("Expiry Date")
            limit = st.number_input("Card Limit")
            last_used = st.text_input("Last Used (YYYY-MM-DD HH:MM:SS)")

            if st.button("Submit"):
                res = requests.post(f"{BASE_URL}/cards", json={
                    "card_id": int(card_id),
                    "user_id": int(user_id),
                    "card_number": card_number,
                    "expiry_date": expiry,
                    "card_limit": float(limit),
                    "last_used": last_used
                })
                show_message(res)

        elif option == "Read":
            if st.button("Load"):
                df = pd.DataFrame(requests.get(f"{BASE_URL}/cards").json())
                st.dataframe(df, use_container_width=True)

                if not df.empty:
                    st.subheader("📊 Card Limit Distribution")
                    st.bar_chart(df["card_limit"])

        elif option == "Update":
            card_id = st.number_input("Card ID")
            user_id = st.number_input("User ID")
            card_number = st.text_input("Card Number")
            expiry = st.text_input("Expiry Date")
            limit = st.number_input("Card Limit")
            last_used = st.text_input("Last Used")

            if st.button("Update"):
                res = requests.put(f"{BASE_URL}/cards/{int(card_id)}", json={
                    "user_id": int(user_id),
                    "card_number": card_number,
                    "expiry_date": expiry,
                    "card_limit": float(limit),
                    "last_used": last_used
                })
                show_message(res)

        elif option == "Delete":
            card_id = st.number_input("Card ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/cards/{int(card_id)}")
                show_message(res)

    # ================= TRANSACTION =================
    elif module == "transaction":

        if option == "Create":
            txn_id = st.number_input("Transaction ID")
            user_id = st.number_input("User ID")
            card_id = st.number_input("Card ID")
            merchant_id = st.number_input("Merchant ID")
            amount = st.number_input("Amount")
            datetime = st.text_input("Datetime (YYYY-MM-DD HH:MM:SS)")
            location = st.text_input("Location")
            category = st.text_input("Category")
            txn_type = st.text_input("Type (online/offline)")

            if st.button("Submit"):
                res = requests.post(f"{BASE_URL}/transactions", json={
                    "transaction_id": int(txn_id),
                    "user_id": int(user_id),
                    "card_id": int(card_id),
                    "merchant_id": int(merchant_id),
                    "amount": float(amount),
                    "transaction_datetime": datetime,
                    "location": location,
                    "category": category,
                    "transaction_type": txn_type
                })
                show_message(res)

        elif option == "Read":
            if st.button("Load"):
                df = pd.DataFrame(requests.get(f"{BASE_URL}/transactions").json())
                st.dataframe(df, use_container_width=True)

                if not df.empty:
                    df["amount"] = pd.to_numeric(df["amount"], errors='coerce')

                    st.metric("Total Transactions", len(df))
                    st.metric("Total Amount", int(df["amount"].sum()))

                    if "transaction_datetime" in df.columns:
                        df["transaction_datetime"] = pd.to_datetime(df["transaction_datetime"])
                        df = df.sort_values("transaction_datetime")
                        st.line_chart(df.set_index("transaction_datetime")["amount"])

                    if "category" in df.columns:
                        st.bar_chart(df["category"].value_counts())

        elif option == "Update":
            txn_id = st.number_input("Transaction ID")
            amount = st.number_input("Amount")
            location = st.text_input("Location")
            category = st.text_input("Category")
            txn_type = st.text_input("Type")

            if st.button("Update"):
                res = requests.put(f"{BASE_URL}/transactions/{int(txn_id)}", json={
                    "amount": float(amount),
                    "location": location,
                    "category": category,
                    "transaction_type": txn_type
                })
                show_message(res)

        elif option == "Delete":
            txn_id = st.number_input("Transaction ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/transactions/{int(txn_id)}")
                show_message(res)

    # ================= FRAUD =================
    elif module == "fraud":

        st.subheader("🚨 Fraud Detection")

        if st.button("Load Predictions"):
            df = pd.DataFrame(requests.get(f"{BASE_URL}/fraud_prediction").json())
            st.dataframe(df, use_container_width=True)

        if st.button("Load Alerts"):
            df = pd.DataFrame(requests.get(f"{BASE_URL}/fraud_alert").json())
            st.dataframe(df, use_container_width=True)