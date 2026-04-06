import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"  # Change if needed

st.title("💳 Fraud Detection System")

menu = st.sidebar.selectbox("Module", [
    "Users",
    "Cards",
    "Transactions",
    "Fraud Detection"
])

# ================= USERS =================
if menu == "Users":

    st.subheader("👤 Users")

    if st.button("Load Users"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/users").json())
        st.dataframe(df)

        st.subheader("📊 Account Type Distribution")
        st.bar_chart(df["account_type"].value_counts())
        st.caption("Number of users in each account type")

        df["age_group"] = df["age"].apply(lambda x: "Below 25" if x < 25 else "25-50" if x <= 50 else "Above 50")
        st.subheader("📊 Age Group Distribution")
        st.bar_chart(df["age_group"].value_counts())
        st.caption("User distribution by age")

    with st.expander("➕ Add User"):
        uid = st.number_input("User ID", key="u1")
        name = st.text_input("Name", key="u2")
        phone = st.text_input("Phone", key="u3")
        age = st.number_input("Age", key="u4")
        acc = st.selectbox("Account Type", ["savings","current","premium"], key="u5")
        days = st.number_input("Account Age Days", key="u6")

        if st.button("Add"):
            requests.post(f"{BASE_URL}/users", json={
                "user_id": uid, "name": name, "phone": phone,
                "age": age, "account_type": acc, "account_age_days": days
            })
            st.success("Added")

    with st.expander("✏️ Update User"):
        uid = st.number_input("User ID", key="u7")
        name = st.text_input("New Name", key="u8")
        phone = st.text_input("New Phone", key="u9")
        age = st.number_input("New Age", key="u10")
        acc = st.selectbox("Account Type", ["savings","current","premium"], key="u11")
        days = st.number_input("Account Age Days", key="u12")

        if st.button("Update"):
            requests.put(f"{BASE_URL}/users/{int(uid)}", json={
                "name": name, "phone": phone,
                "age": age, "account_type": acc, "account_age_days": days
            })
            st.success("Updated")

    with st.expander("🗑 Delete User"):
        uid = st.number_input("User ID", key="u13")
        if st.button("Delete"):
            requests.delete(f"{BASE_URL}/users/{int(uid)}")
            st.success("Deleted")


# ================= CARDS =================
elif menu == "Cards":

    st.subheader("💳 Cards")

    if st.button("Load Cards"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/cards").json())
        st.dataframe(df)

        st.subheader("📊 Card Limit Distribution")
        st.bar_chart(df["card_limit"].value_counts())
        st.caption("Number of cards by limit")

    with st.expander("➕ Add Card"):
        cid = st.number_input("Card ID", key="c1")
        uid = st.number_input("User ID", key="c2")
        limit = st.selectbox("Limit",[50000,100000,150000,200000],key="c3")
        status = st.selectbox("Status",["active","blocked"],key="c4")
        freq = st.number_input("Usage Frequency",key="c5")

        if st.button("Add Card"):
            requests.post(f"{BASE_URL}/cards", json={
                "card_id":cid,"user_id":uid,"card_limit":limit,
                "card_status":status,"usage_frequency":freq
            })
            st.success("Added")

    with st.expander("✏️ Update Card"):
        cid = st.number_input("Card ID", key="c6")
        limit = st.selectbox("Limit",[50000,100000,150000,200000],key="c7")
        status = st.selectbox("Status",["active","blocked"],key="c8")
        freq = st.number_input("Usage Frequency",key="c9")

        if st.button("Update Card"):
            requests.put(f"{BASE_URL}/cards/{int(cid)}", json={
                "card_limit":limit,"card_status":status,"usage_frequency":freq
            })
            st.success("Updated")

    with st.expander("🗑 Delete Card"):
        cid = st.number_input("Card ID", key="c10")
        if st.button("Delete Card"):
            requests.delete(f"{BASE_URL}/cards/{int(cid)}")
            st.success("Deleted")


# ================= TRANSACTIONS =================
elif menu == "Transactions":

    st.subheader("💸 Transactions")

    if st.button("Load Transactions"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/transactions").json())
        st.dataframe(df)

        st.subheader("📈 Transaction Amount Over Time")
        df["transaction_time"] = pd.to_datetime(df["transaction_time"])
        st.line_chart(df.set_index("transaction_time")["amount"])
        st.caption("Shows spending pattern over time")

        st.subheader("📊 Transaction Type Distribution")
        st.bar_chart(df["transaction_type"].value_counts())
        st.caption("Online vs Swipe vs Withdrawal")

        st.subheader("📊 Device Usage Distribution")
        st.bar_chart(df["device_type"].value_counts())
        st.caption("Mobile vs ATM vs POS usage")

    with st.expander("➕ Add Transaction"):
        tid = st.number_input("Transaction ID", key="t1")
        uid = st.number_input("User ID", key="t2")
        cid = st.number_input("Card ID", key="t3")
        mid = st.number_input("Merchant ID", key="t4")
        amt = st.number_input("Amount", key="t5")
        time = st.text_input("Transaction Time", key="t6")
        loc = st.selectbox("Location",["Chennai","Delhi","Mumbai","Bangalore"],key="t7")
        dev = st.selectbox("Device",["mobile","ATM","POS"],key="t8")
        typ = st.selectbox("Type",["online","swipe","withdrawal"],key="t9")
        freq = st.number_input("Frequency",key="t10")

        if st.button("Add Transaction"):
            requests.post(f"{BASE_URL}/transactions", json={
                "transaction_id":tid,"user_id":uid,"card_id":cid,
                "merchant_id":mid,"amount":amt,"transaction_time":time,
                "location":loc,"device_type":dev,"transaction_type":typ,
                "transaction_frequency":freq
            })
            st.success("Added")

    with st.expander("✏️ Update Transaction"):
        tid = st.number_input("Transaction ID", key="t11")
        amt = st.number_input("Amount", key="t12")
        loc = st.selectbox("Location",["Chennai","Delhi"],key="t13")
        dev = st.selectbox("Device",["mobile","ATM","POS"],key="t14")
        typ = st.selectbox("Type",["online","swipe","withdrawal"],key="t15")
        freq = st.number_input("Frequency",key="t16")

        if st.button("Update Transaction"):
            requests.put(f"{BASE_URL}/transactions/{int(tid)}", json={
                "amount":amt,"location":loc,"device_type":dev,
                "transaction_type":typ,"transaction_frequency":freq
            })
            st.success("Updated")

    with st.expander("🗑 Delete Transaction"):
        tid = st.number_input("Transaction ID", key="t17")
        if st.button("Delete Transaction"):
            requests.delete(f"{BASE_URL}/transactions/{int(tid)}")
            st.success("Deleted")


# ================= FRAUD =================
elif menu == "Fraud Detection":

    if st.button("Run Fraud Detection"):
        df = pd.DataFrame(requests.get(f"{BASE_URL}/detect_fraud").json())

        st.dataframe(df)

        st.subheader("📊 Fraud vs Normal Transactions")
        st.bar_chart(df["status"].value_counts())
        st.caption("Shows fraud detection results")

st.set_page_config(page_title="Credit Card Fraud System", layout="wide")

st.title("💳 Credit Card Fraud Detection System - Frontend")

# ================= MODULE SELECTION =================
module = st.sidebar.selectbox(
    "Select Module",
    ["users", "cards", "transactions", "merchants"]
)

operation = st.sidebar.selectbox(
    "Operation",
    ["Create", "Read", "Update", "Delete"]
)

# ================= USERS =================
if module == "users":

    if operation == "Create":
        st.subheader("➕ Add User")
        user_id = st.number_input("User ID")
        name = st.text_input("Name")
        phone = st.number_input("Phone")
        age = st.number_input("Age")
        account_type = st.selectbox("Account Type", ["savings", "current", "premium"])
        account_age_days = st.number_input("Account Age (days)")
        avg_monthly_spend = st.number_input("Avg Monthly Spend")

        if st.button("Create User"):
            data = {
                "user_id": user_id,
                "name": name,
                "phone": phone,
                "age": age,
                "account_type": account_type,
                "account_age_days": account_age_days,
                "avg_monthly_spend": avg_monthly_spend
            }
            res = requests.post(f"{BASE_URL}/users", json=data)
            st.success(res.json())

    elif operation == "Read":
        st.subheader("📄 View Users")
        if st.button("Load Users"):
            res = requests.get(f"{BASE_URL}/users")
            df = pd.DataFrame(res.json())
            st.dataframe(df)

    elif operation == "Update":
        st.subheader("✏️ Update User")
        user_id = st.number_input("User ID to Update")
        name = st.text_input("New Name")
        phone = st.number_input("New Phone")
        age = st.number_input("New Age")
        account_type = st.selectbox("New Account Type", ["savings", "current", "premium"])
        account_age_days = st.number_input("New Account Age")
        avg_monthly_spend = st.number_input("New Avg Spend")

        if st.button("Update User"):
            data = {
                "name": name,
                "phone": phone,
                "age": age,
                "account_type": account_type,
                "account_age_days": account_age_days,
                "avg_monthly_spend": avg_monthly_spend
            }
            res = requests.put(f"{BASE_URL}/users/{user_id}", json=data)
            st.success(res.json())

    elif operation == "Delete":
        st.subheader("🗑 Delete User")
        user_id = st.number_input("User ID to Delete")
        if st.button("Delete User"):
            res = requests.delete(f"{BASE_URL}/users/{user_id}")
            st.success(res.json())

# ================= MERCHANTS =================
elif module == "merchants":

    if operation == "Create":
        st.subheader("➕ Add Merchant")
        merchant_id = st.number_input("Merchant ID")
        category = st.text_input("Category")
        location = st.text_input("Location")

        if st.button("Create Merchant"):
            data = {
                "merchant_id": merchant_id,
                "category": category,
                "location": location
            }
            res = requests.post(f"{BASE_URL}/merchants", json=data)
            st.success(res.json())

    elif operation == "Read":
        st.subheader("📄 View Merchants")
        if st.button("Load Merchants"):
            res = requests.get(f"{BASE_URL}/merchants")
            df = pd.DataFrame(res.json())
            st.dataframe(df)

    elif operation == "Update":
        st.subheader("✏️ Update Merchant")
        merchant_id = st.number_input("Merchant ID")
        category = st.text_input("New Category")
        location = st.text_input("New Location")

        if st.button("Update Merchant"):
            data = {"category": category, "location": location}
            res = requests.put(f"{BASE_URL}/merchants/{merchant_id}", json=data)
            st.success(res.json())

    elif operation == "Delete":
        st.subheader("🗑 Delete Merchant")
        merchant_id = st.number_input("Merchant ID")
        if st.button("Delete Merchant"):
            res = requests.delete(f"{BASE_URL}/merchants/{merchant_id}")
            st.success(res.json())

# ================= CARDS =================
elif module == "cards":

    if operation == "Create":
        st.subheader("➕ Add Card")
        card_id = st.number_input("Card ID")
        user_id = st.number_input("User ID")
        card_type = st.selectbox("Card Type", ["Visa", "MasterCard", "RuPay"])
        card_limit = st.number_input("Card Limit")
        card_status = st.text_input("Card Status")
        is_active = st.checkbox("Is Active")

        if st.button("Create Card"):
            data = {
                "card_id": card_id,
                "user_id": user_id,
                "card_type": card_type,
                "card_limit": card_limit,
                "card_status": card_status,
                "is_active": is_active
            }
            res = requests.post(f"{BASE_URL}/cards", json=data)
            st.success(res.json())

    elif operation == "Read":
        st.subheader("📄 View Cards")
        if st.button("Load Cards"):
            res = requests.get(f"{BASE_URL}/cards")
            df = pd.DataFrame(res.json())
            st.dataframe(df)

    elif operation == "Update":
        st.subheader("✏️ Update Card")
        card_id = st.number_input("Card ID")
        card_status = st.text_input("New Status")
        is_active = st.checkbox("Active")

        if st.button("Update Card"):
            data = {"card_status": card_status, "is_active": is_active}
            res = requests.put(f"{BASE_URL}/cards/{card_id}", json=data)
            st.success(res.json())

    elif operation == "Delete":
        st.subheader("🗑 Delete Card")
        card_id = st.number_input("Card ID")
        if st.button("Delete Card"):
            res = requests.delete(f"{BASE_URL}/cards/{card_id}")
            st.success(res.json())

# ================= TRANSACTIONS =================
elif module == "transactions":

    if operation == "Create":
        st.subheader("➕ Add Transaction")
        transaction_id = st.number_input("Transaction ID")
        user_id = st.number_input("User ID")
        card_id = st.number_input("Card ID")
        merchant_id = st.number_input("Merchant ID")
        amount = st.number_input("Amount")
        device_type = st.selectbox("Device", ["mobile", "web", "atm"])
        transaction_type = st.selectbox("Type", ["online", "offline"])
        is_international = st.checkbox("International")
        is_fraud = st.checkbox("Fraud")

        if st.button("Create Transaction"):
            data = {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "card_id": card_id,
                "merchant_id": merchant_id,
                "amount": amount,
                "device_type": device_type,
                "transaction_type": transaction_type,
                "is_international": is_international,
                "is_fraud": is_fraud
            }
            res = requests.post(f"{BASE_URL}/transactions_", json=data)
            st.success(res.json())

    elif operation == "Read":
        st.subheader("📄 View Transactions")
        if st.button("Load Transactions"):
            res = requests.get(f"{BASE_URL}/transactions_")
            df = pd.DataFrame(res.json())
            st.dataframe(df)

    elif operation == "Update":
        st.subheader("✏️ Update Transaction")
        transaction_id = st.number_input("Transaction ID")
        amount = st.number_input("New Amount")
        is_fraud = st.checkbox("Fraud")

        if st.button("Update Transaction"):
            data = {"amount": amount, "is_fraud": is_fraud}
            res = requests.put(f"{BASE_URL}/transactions_/{transaction_id}", json=data)
            st.success(res.json())

    elif operation == "Delete":
        st.subheader("🗑 Delete Transaction")
        transaction_id = st.number_input("Transaction ID")
        if st.button("Delete Transaction"):
            res = requests.delete(f"{BASE_URL}/transactions_/{transaction_id}")
            st.success(res.json())

st.sidebar.markdown("---")
st.sidebar.info("Make sure your Flask API is running 🚀")
