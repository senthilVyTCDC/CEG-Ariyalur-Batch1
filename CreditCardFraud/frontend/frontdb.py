import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Fraud Detection System", layout="wide")

# ---------- SESSION ----------
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
        data = res.json()
        st.success(data.get("message", "Operation completed"))
    except:
        st.error("Something went wrong")

# ---------- HOME ----------
if st.session_state.page == "home":

    st.markdown("""
    <div style='text-align:center;'>
        <h1 style='color:#1f4e79;'>💳 Credit Card Fraud Detection System</h1>
        <p style='color:gray;'>Secure • Monitor • Detect Fraud</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Select Module")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👤 User Management", use_container_width=True):
            open_module("user")

        if st.button("💳 Card Management", use_container_width=True):
            open_module("card")

    with col2:
        if st.button("💰 Transaction Monitoring", use_container_width=True):
            open_module("transaction")

        if st.button("🏪 Merchant Analysis", use_container_width=True):
            open_module("merchant")

# ---------- MODULE ----------
elif st.session_state.page == "module":

    module = st.session_state.module
    st.title(f"📦 {module.upper()} MODULE")

    st.button("⬅ Back to Home", on_click=go_home)

    option = st.radio("Choose Operation", ["Create", "Read", "Update", "Delete"], horizontal=True)
    st.divider()

    # ================= USER =================
    if module == "user":

        if option == "Create":
            user_id = st.number_input("User ID")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

            if st.button("Submit"):
                res = requests.post(f"{BASE_URL}/user_add", json={
                    "user_id": int(user_id),
                    "name": name,
                    "email": email,
                    "phone": phone
                })
                show_message(res)

        elif option == "Read":
            if st.button("Load Users"):
                res = requests.get(f"{BASE_URL}/user")
                df = pd.DataFrame(res.json())

                st.dataframe(df, use_container_width=True)

                if not df.empty:
                    st.subheader("📊 User Distribution")
                    st.bar_chart(df['user_id'])

        elif option == "Update":
            user_id = st.number_input("User ID")
            name = st.text_input("New Name")
            email = st.text_input("New Email")
            phone = st.text_input("New Phone")

            if st.button("Update"):
                res = requests.put(f"{BASE_URL}/user_update/{int(user_id)}", json={
                    "name": name,
                    "email": email,
                    "phone": phone
                })
                show_message(res)

        elif option == "Delete":
            user_id = st.number_input("User ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/user_delete/{int(user_id)}")
                show_message(res)

    # ================= CARD =================
    elif module == "card":

        if option == "Create":
            user_id = st.number_input("User ID")
            card_number = st.text_input("Card Number")
            card_type = st.text_input("Card Type")
            expiry = st.text_input("Expiry Date")

            if st.button("Submit"):
                res = requests.post(f"{BASE_URL}/api/cards", json={
                    "user_id": int(user_id),
                    "card_number": card_number,
                    "card_type": card_type,
                    "expiry_date": expiry
                })
                show_message(res)

        elif option == "Read":
            if st.button("Load Cards"):
                res = requests.get(f"{BASE_URL}/api/cards")
                df = pd.DataFrame(res.json())

                st.dataframe(df, use_container_width=True)

                if not df.empty and 'card_type' in df.columns:
                    st.subheader("📊 Card Type Distribution")
                    st.bar_chart(df['card_type'].value_counts())

        elif option == "Update":
            card_id = st.number_input("Card ID")
            user_id = st.number_input("User ID")
            card_number = st.text_input("Card Number")
            card_type = st.text_input("Card Type")
            expiry = st.text_input("Expiry Date")

            if st.button("Update"):
                res = requests.put(f"{BASE_URL}/api/cards/{int(card_id)}", json={
                    "user_id": int(user_id),
                    "card_number": card_number,
                    "card_type": card_type,
                    "expiry_date": expiry
                })
                show_message(res)

        elif option == "Delete":
            card_id = st.number_input("Card ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/api/cards/{int(card_id)}")
                show_message(res)

    # ================= TRANSACTION =================
    elif module == "transaction":

        if option == "Create":
            user_id = st.number_input("User ID")
            card_id = st.number_input("Card ID")
            merchant_id = st.number_input("Merchant ID")
            amount = st.number_input("Amount")
            status = st.text_input("Status")

            if st.button("Submit"):
                res = requests.post(f"{BASE_URL}/transaction_add", json={
                    "user_id": int(user_id),
                    "card_id": int(card_id),
                    "merchant_id": int(merchant_id),
                    "amount": float(amount),
                    "status": status
                })
                show_message(res)

        elif option == "Read":
            if st.button("Load Transactions"):
                res = requests.get(f"{BASE_URL}/transaction")
                df = pd.DataFrame(res.json())

                st.dataframe(df, use_container_width=True)

                if not df.empty:
                    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

                    # KPI
                    st.metric("Total Transactions", len(df))
                    st.metric("Total Amount", int(df['amount'].sum()))

                    # Histogram
                    st.subheader("📊 Amount Distribution")
                    fig, ax = plt.subplots()
                    ax.hist(df['amount'])
                    st.pyplot(fig)

                    # Status Chart
                    if 'status' in df.columns:
                        st.subheader("📊 Status Distribution")
                        st.bar_chart(df['status'].value_counts())

        elif option == "Update":
            txn_id = st.number_input("Transaction ID")
            amount = st.number_input("Amount")
            status = st.text_input("Status")

            if st.button("Update"):
                res = requests.put(f"{BASE_URL}/transaction_update/{int(txn_id)}", json={
                    "amount": float(amount),
                    "status": status
                })
                show_message(res)

        elif option == "Delete":
            txn_id = st.number_input("Transaction ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/transaction_delete/{int(txn_id)}")
                show_message(res)

    # ================= MERCHANT =================
    elif module == "merchant":
        st.warning("⚠️ Merchant module not implemented in Flask yet")