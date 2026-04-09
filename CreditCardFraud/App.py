from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
import pickle

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

app = Flask(__name__)

# ---------------- DB CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="soni",
    database="creditcardfraud"
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return "Fraud Detection API Running ✅"

# ================= USERS =================
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    return jsonify(cursor.fetchall())

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    cursor.execute("""
        INSERT INTO users 
        (user_id, name, phone, age, account_type, account_age_days, avg_monthly_spend)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        data['user_id'], data['name'], data['phone'], data['age'],
        data['account_type'], data['account_age_days'], 0
    ))
    db.commit()
    return jsonify({"message": "User added"})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    cursor.execute("""
        UPDATE users SET 
        name=%s, phone=%s, age=%s,
        account_type=%s, account_age_days=%s
        WHERE user_id=%s
    """, (
        data['name'], data['phone'], data['age'],
        data['account_type'], data['account_age_days'], id
    ))
    db.commit()
    return jsonify({"message": "User updated"})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    cursor.execute("DELETE FROM users WHERE user_id=%s", (id,))
    db.commit()
    return jsonify({"message": "User deleted"})

# ================= CARDS =================
@app.route('/cards', methods=['GET'])
def get_cards():
    cursor.execute("SELECT * FROM cards")
    return jsonify(cursor.fetchall())

@app.route('/cards', methods=['POST'])
def add_card():
    data = request.json
    cursor.execute("""
        INSERT INTO cards 
        (card_id, user_id, card_limit, card_status, usage_frequency)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        data['card_id'], data['user_id'], data['card_limit'],
        data['card_status'], data['usage_frequency']
    ))
    db.commit()
    return jsonify({"message": "Card added"})

@app.route('/cards/<int:id>', methods=['PUT'])
def update_card(id):
    data = request.json
    cursor.execute("""
        UPDATE cards SET 
        card_limit=%s, card_status=%s, usage_frequency=%s
        WHERE card_id=%s
    """, (
        data['card_limit'], data['card_status'],
        data['usage_frequency'], id
    ))
    db.commit()
    return jsonify({"message": "Card updated"})

@app.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    cursor.execute("DELETE FROM cards WHERE card_id=%s", (id,))
    db.commit()
    return jsonify({"message": "Card deleted"})

# ================= TRANSACTIONS =================
@app.route('/transactions', methods=['GET'])
def get_transactions():
    cursor.execute("SELECT * FROM transactions_")
    return jsonify(cursor.fetchall())

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json

    if not data.get('transaction_time'):
        return jsonify({"error": "Transaction time is required"}), 400

    current_time = datetime.strptime(data['transaction_time'], "%Y-%m-%d %H:%M:%S")

    # -------- GET PREVIOUS --------
    cursor.execute("""
        SELECT transaction_time, location 
        FROM transactions_
        WHERE user_id=%s
        ORDER BY transaction_time DESC
        LIMIT 1
    """, (data['user_id'],))

    prev = cursor.fetchone()

    if prev:
        previous_time = prev['transaction_time']
        previous_location = prev['location']

        if isinstance(previous_time, str):
            previous_time = datetime.strptime(previous_time, "%Y-%m-%d %H:%M:%S")
        gap = int((current_time - previous_time).total_seconds() / 60)
    else:
        previous_time = current_time
        previous_location = data['location']
        gap = 0

    # -------- USER AVG --------
    cursor.execute("""
        SELECT AVG(amount) AS avg_amt 
        FROM transactions_
        WHERE user_id=%s
    """, (data['user_id'],))

    result = cursor.fetchone()
    avg_amt = float(result['avg_amt']) if result['avg_amt'] else float(data['amount'])

    # -------- FIXED FREQUENCY --------
    freq = data.get("transaction_frequency", 1)

    # -------- ML --------
    input_data = [[
        data["amount"],
        freq,
        gap,
        avg_amt,
        current_time.hour
    ]]

    prob = model.predict_proba(input_data)[0][1]
    prob = float(prob)

    # -------- INSERT --------
    cursor.execute("""
        INSERT INTO transactions_ (
            transaction_id, user_id, card_id, merchant_id, amount,
            transaction_time, previous_transaction_time,
            location, previous_location,
            device_type, transaction_type,
            transaction_frequency, last_transaction_gap,
            user_avg_transaction_amount
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data['transaction_id'], data['user_id'], data['card_id'],
        data['merchant_id'], data['amount'], current_time,
        previous_time, data['location'], previous_location,
        data['device_type'], data['transaction_type'],
        freq, gap, avg_amt
    ))

    # -------- UPDATE USER --------
    cursor.execute("""
        UPDATE users SET avg_monthly_spend=%s WHERE user_id=%s
    """, (avg_amt, data['user_id']))

    # -------- ALERT --------
    if prob > 0.7:
        cursor.execute("""
            INSERT INTO fraud_alert 
            (transaction_id, fraud_probability, alert_status)
            VALUES (%s,%s,%s)
        """, (data['transaction_id'], prob, "HIGH"))

    db.commit()

    return jsonify({
        "message": "Transaction added",
        "fraud_probability": float(prob)
    })

@app.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    data = request.json
    cursor.execute("""
        UPDATE transactions_ SET
        amount=%s, location=%s, device_type=%s,
        transaction_type=%s, transaction_frequency=%s
        WHERE transaction_id=%s
    """, (
        data['amount'], data['location'], data['device_type'],
        data['transaction_type'], data['transaction_frequency'], id
    ))
    db.commit()
    return jsonify({"message": "Transaction updated"})

@app.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    cursor.execute("DELETE FROM transactions_ WHERE transaction_id=%s", (id,))
    db.commit()
    return jsonify({"message": "Transaction deleted"})

# ================= RULE-BASED FRAUD =================
@app.route('/detect_fraud', methods=['GET'])
def detect_fraud():

    cursor.execute("""
        SELECT t.*, c.card_limit
        FROM transactions_ t
        JOIN cards c ON t.card_id = c.card_id
    """)

    data = cursor.fetchall()
    results = []

    for row in data:
        risk = 0
        amount = float(row['amount'])
        limit = float(row['card_limit'])
        gap = int(row['last_transaction_gap'])
        freq = int(row['transaction_frequency'])
        hour = int(str(row['transaction_time'])[11:13])

        if amount > 0.8 * limit:
            risk += 1
        if row['location'] != row['previous_location'] and gap < 60:
            risk += 2
        if hour < 4 and amount > 0.6 * limit:
            risk += 2
        if freq > 10 and gap < 30:
            risk += 2
        if amount > 3 * float(row['user_avg_transaction_amount']):
            risk += 1

        status = "Fraud" if risk >= 3 else "Normal"

        results.append({
            "transaction_id": row['transaction_id'],
            "amount": amount,
            "risk_score": risk,
            "status": status
        })

    return jsonify(results)

# ================= ML FRAUD =================
@app.route('/predict_fraud', methods=['POST'])
def predict_fraud():
    data = request.json

    dt = datetime.strptime(data["transaction_time"], "%Y-%m-%d %H:%M:%S")

    input_data = [[
        data["amount"],
        data["transaction_frequency"],
        data["last_transaction_gap"],
        data["user_avg_transaction_amount"],
        dt.hour
    ]]

    prob = model.predict_proba(input_data)[0][1]
    status = "Fraud" if prob > 0.7 else "Normal"

    return jsonify({
        "fraud_probability": float(prob),
        "status": status
    })

# ================= ALERTS =================
@app.route('/alerts', methods=['GET'])
def get_alerts():
    cursor.execute("SELECT * FROM fraud_alert")
    return jsonify(cursor.fetchall())



# ================= MERCHANTS =================

@app.route('/merchants', methods=['GET'])
def get_merchants():
    cursor.execute("SELECT * FROM merchants")
    return jsonify(cursor.fetchall())

@app.route('/merchants', methods=['POST'])
def add_merchant():
    data = request.json
    cursor.execute(
        "INSERT INTO merchants (merchant_id, category, location) VALUES (%s,%s,%s)",
        (data['merchant_id'], data['category'], data['location'])
    )
    db.commit()
    return jsonify({"message": "Merchant added"})

@app.route('/merchants/<int:id>', methods=['PUT'])
def update_merchant(id):
    data = request.json
    cursor.execute(
        "UPDATE merchants SET category=%s, location=%s WHERE merchant_id=%s",
        (data['category'], data['location'], id)
    )
    db.commit()
    return jsonify({"message": "Updated"})

@app.route('/merchants/<int:id>', methods=['DELETE'])
def delete_merchant(id):
    cursor.execute("DELETE FROM merchants WHERE merchant_id=%s", (id,))
    db.commit()
    return jsonify({"message": "Deleted"})

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


