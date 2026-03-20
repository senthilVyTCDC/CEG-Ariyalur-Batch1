import streamlit as st
import requests

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

if st.session_state.page == "home":

    st.markdown("""
    <div style='text-align:center; margin-bottom:10px'>
        <h1 style='color:#1f4e79;'>💳 Credit Card Detalis</h1>
        <p style='color:gray;'>Secure • Monitor • Detect</p>
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

elif st.session_state.page == "module":

    module = st.session_state.module
    st.title(f"📦 {module.upper()} DETAILS")

    st.button("⬅ Back to Home", on_click=go_home)

    option = st.radio("Choose Operation", ["Create", "Read", "Update", "Delete"], horizontal=True)

    st.divider()

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
                st.success(res.json())

        elif option == "Read":
            if st.button("Load Users"):
                res = requests.get(f"{BASE_URL}/user")
                st.dataframe(res.json(), width='stretch')

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
                st.success(res.json())

        elif option == "Delete":
            user_id = st.number_input("User ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/user_delete/{int(user_id)}")
                st.success(res.json())

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
                st.success(res.json())

        elif option == "Read":
            if st.button("Load Cards"):
                res = requests.get(f"{BASE_URL}/api/cards")
                st.dataframe(res.json(), width='stretch')

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
                st.success(res.json())

        elif option == "Delete":
            card_id = st.number_input("Card ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/api/cards/{int(card_id)}")
                st.success(res.json())

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
                    "amount": amount,
                    "status": status
                })
                st.success(res.json())

        elif option == "Read":
            if st.button("Load Transactions"):
                res = requests.get(f"{BASE_URL}/transaction")
                st.dataframe(res.json(), width='stretch')

        elif option == "Update":
            txn_id = st.number_input("Transaction ID")
            amount = st.number_input("Amount")
            status = st.text_input("Status")

            if st.button("Update"):
                res = requests.put(f"{BASE_URL}/transaction_update/{int(txn_id)}", json={
                    "amount": amount,
                    "status": status
                })
                st.success(res.json())

        elif option == "Delete":
            txn_id = st.number_input("Transaction ID")

            if st.button("Delete"):
                res = requests.delete(f"{BASE_URL}/transaction_delete/{int(txn_id)}")
                st.success(res.json())

    elif module == "merchant":
        st.warning("⚠️ Merchant module not implemented in Flask yet")