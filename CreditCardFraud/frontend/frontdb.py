import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000/"

st.title("Credit Card Fraud System")

menu = st.sidebar.selectbox("Select Module", ["User", "Card", "Transaction"])

#users
if menu == "User":
    st.header("👤 User Operations")

    option = st.selectbox("Choose Operation", ["Create", "Get", "Update", "Delete"])

    if option == "Create":
        name = st.text_input("Name")
        email = st.text_input("Email")

        if st.button("Create User"):
            res = requests.post(f"{BASE_URL}/users", json={
                "name": name,
                "email": email
            })
            st.write(res.json())

    elif option == "Get":
        user_id = st.text_input("User ID")

        if st.button("Get User"):
            res = requests.get(f"{BASE_URL}/users/{user_id}")
            st.write(res.json())

    elif option == "Update":
        user_id = st.text_input("User ID")
        name = st.text_input("New Name")
        email = st.text_input("New Email")

        if st.button("Update User"):
            res = requests.put(f"{BASE_URL}/users/{user_id}", json={
                "name": name,
                "email": email
            })
            st.write(res.json())

    elif option == "Delete":
        user_id = st.text_input("User ID")

        if st.button("Delete User"):
            res = requests.delete(f"{BASE_URL}/users/{user_id}")
            st.write(res.json())


#  CARD 
elif menu == "Card":
    st.header("Card Operations")

    option = st.selectbox("Choose Operation", ["Create", "Get", "Update", "Delete"])

    if option == "Create":
        card_number = st.text_input("Card Number")
        card_type = st.text_input("Card Type")
        expiry = st.text_input("Expiry Date")
        user_id = st.text_input("User ID")

        if st.button("Create Card"):
            res = requests.post(f"{BASE_URL}/cards", json={
                "card_number": card_number,
                "card_type": card_type,
                "expiry_date": expiry,
                "user_id": user_id
            })
            st.write(res.json())

    elif option == "Get":
        card_id = st.text_input("Card ID")

        if st.button("Get Card"):
            res = requests.get(f"{BASE_URL}/cards/{card_id}")
            st.write(res.json())

    elif option == "Update":
        card_id = st.text_input("Card ID")
        card_number = st.text_input("New Card Number")
        card_type = st.text_input("New Card Type")

        if st.button("Update Card"):
            res = requests.put(f"{BASE_URL}/cards/{card_id}", json={
                "card_number": card_number,
                "card_type": card_type
            })
            st.write(res.json())

    elif option == "Delete":
        card_id = st.text_input("Card ID")

        if st.button("Delete Card"):
            res = requests.delete(f"{BASE_URL}/cards/{card_id}")
            st.write(res.json())


# TRANSACTION
elif menu == "Transaction":
    st.header("Transaction Operations")

    option = st.selectbox("Choose Operation", ["Create", "Get", "Delete"])

    if option == "Create":
        card_id = st.text_input("Card ID")
        amount = st.text_input("Amount")
        location = st.text_input("Location")

        if st.button("Create Transaction"):
            res = requests.post(f"{BASE_URL}/transactions", json={
                "card_id": card_id,
                "amount": amount,
                "location": location
            })
            st.write(res.json())

    elif option == "Get":
        txn_id = st.text_input("Transaction ID")

        if st.button("Get Transaction"):
            res = requests.get(f"{BASE_URL}/transactions/{txn_id}")
            st.write(res.json())

    elif option == "Delete":
        txn_id = st.text_input("Transaction ID")

        if st.button("Delete Transaction"):
            res = requests.delete(f"{BASE_URL}/transactions/{txn_id}")
            st.write(res.json())