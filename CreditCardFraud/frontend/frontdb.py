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
        st.success(res.json().get("message"))
    except:
        st.error("Error")

# ---------------- HOME (UNCHANGED) ----------------
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
        if st.button("👤 User Management", width='stretch'):
            open_module("user")

        if st.button("💳 Card Management", width='stretch'):
            open_module("card")

    with col2:
        if st.button("💰 Transaction Monitoring", width='stretch'):
            open_module("transaction")

        if st.button("🏪 Merchant Analysis", width='stretch'):
            open_module("merchant")

# ---------------- MODULE ----------------
else:

    module = st.session_state.module
    st.title(f"📦 {module.upper()} MODULE")

    st.button("⬅ Back to Home", on_click=go_home)

    option = st.radio("Choose Operation", ["Create", "Read", "Update", "Delete"], horizontal=True)

    # USER
    if module == "user":

        if option == "Create":
            user_id = st.number_input("User ID")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            age = st.number_input("Age")
            gender = st.selectbox("Gender", ["Male", "Female"])
            bank = st.text_input("Bank Name")
            acc = st.selectbox("Account Type", ["Savings", "Business", "Employee"])

            if st.button("Submit"):
                show_message(requests.post(f"{BASE_URL}/user_add", json={
                    "user_id": int(user_id),
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "age": int(age),
                    "gender": gender,
                    "bank_name": bank,
                    "account_type": acc
                }))

        elif option == "Read":
            if st.button("Load Users"):
                df = pd.DataFrame(requests.get(f"{BASE_URL}/user").json())
                st.dataframe(df)

    # CARD
    elif module == "card":

        if option == "Read":
            if st.button("Load Cards"):
                df = pd.DataFrame(requests.get(f"{BASE_URL}/api/cards").json())
                st.dataframe(df)
                st.bar_chart(df["card_type"].value_counts())

    # TRANSACTION
    elif module == "transaction":

        if option == "Read":
            if st.button("Load Transactions"):
                df = pd.DataFrame(requests.get(f"{BASE_URL}/transaction").json())
                st.dataframe(df)

                if not df.empty:
                    st.bar_chart(df["status"].value_counts())
                    if "category" in df.columns:
                        st.bar_chart(df["category"].value_counts())

    # MERCHANT
    elif module == "merchant":
        st.warning("⚠️ Merchant module not implemented")
