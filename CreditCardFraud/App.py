from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

<<<<<<< HEAD
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rajesh",
    database="creditcardfraud"
)

cursor = db.cursor(dictionary=True)

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
=======
# ---------- DB CONNECTION FUNCTION ----------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="creditcardfraud"
    )

# ---------- HOME ----------
@app.route('/')
def home():
    return jsonify({"message": "API Running 🚀"})


# =========================================================
# 🔹 TRANSACTION MODULE
# =========================================================
@app.route('/transactions_', methods=['GET'])
def get_transactions():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions_")
        data = cursor.fetchall()
        return jsonify(data if data else [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
>>>>>>> 18ee112 (updated db)


@app.route('/transactions_', methods=['POST'])
def add_transaction():
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

<<<<<<< HEAD
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
        current_time = datetime.strptime(data['transaction_time'], "%Y-%m-%d %H:%M:%S")
        gap = int((current_time - previous_time).total_seconds() / 60)
    else:
        previous_time = data['transaction_time']
        previous_location = data['location']
        gap = 0

    cursor.execute("""
        SELECT AVG(amount) AS avg_amt 
        FROM transactions_
        WHERE user_id=%s
    """, (data['user_id'],))

    result = cursor.fetchone()
    avg_amt = result['avg_amt'] if result['avg_amt'] else data['amount']

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
        data['merchant_id'], data['amount'], data['transaction_time'],
        previous_time, data['location'], previous_location,
        data['device_type'], data['transaction_type'],
        data['transaction_frequency'], gap, avg_amt
    ))

    cursor.execute("""
        UPDATE users SET avg_monthly_spend=%s WHERE user_id=%s
    """, (avg_amt, data['user_id']))

    db.commit()
    return jsonify({"message": "Transaction added"})
=======
        cursor.execute("""
            INSERT INTO transactions_
            (transaction_id, user_id, card_id, merchant_id, amount,
             transaction_datetime, location, category, transaction_type)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data['transaction_id'],
            data['user_id'],
            data['card_id'],
            data['merchant_id'],
            data['amount'],
            data['transaction_datetime'],
            data['location'],
            data['category'],
            data['transaction_type']
        ))

        db.commit()
        return jsonify({"message": "Transaction added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
>>>>>>> 18ee112 (updated db)


@app.route('/transactions_/<int:id>', methods=['PUT'])
def update_transaction(id):
<<<<<<< HEAD
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
=======
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE transactions_
            SET amount=%s, location=%s, category=%s, transaction_type=%s
            WHERE transaction_id=%s
        """, (
            data['amount'],
            data['location'],
            data['category'],
            data['transaction_type'],
            id
        ))

        db.commit()
        return jsonify({"message": "Transaction updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
>>>>>>> 18ee112 (updated db)


@app.route('/transactions_/<int:id>', methods=['DELETE'])
def delete_transaction(id):
<<<<<<< HEAD
    cursor.execute("DELETE FROM transactions_ WHERE transaction_id=%s", (id,))
    db.commit()
    return jsonify({"message": "Transaction deleted"})


# ================= FRAUD =================
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


=======
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("DELETE FROM transactions_ WHERE transaction_id=%s", (id,))
        db.commit()
        return jsonify({"message": "Transaction deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================================================
# 🔹 CARD MODULE
# =========================================================
@app.route('/cards', methods=['GET'])
def get_cards():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cards")
        data = cursor.fetchall()
        return jsonify(data if data else [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/cards', methods=['POST'])
def add_card():
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO cards
            (card_id, user_id, card_number, expiry_date, card_limit, last_used)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            data['card_id'],
            data['user_id'],
            data['card_number'],
            data['expiry_date'],
            data['card_limit'],
            data['last_used']
        ))

        db.commit()
        return jsonify({"message": "Card added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/cards/<int:id>', methods=['PUT'])
def update_card(id):
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE cards
            SET user_id=%s, card_number=%s, expiry_date=%s,
                card_limit=%s, last_used=%s
            WHERE card_id=%s
        """, (
            data['user_id'],
            data['card_number'],
            data['expiry_date'],
            data['card_limit'],
            data['last_used'],
            id
        ))

        db.commit()
        return jsonify({"message": "Card updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("DELETE FROM cards WHERE card_id=%s", (id,))
        db.commit()
        return jsonify({"message": "Card deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================================================
# 🔹 USER MODULE
# =========================================================
@app.route('/users', methods=['GET'])
def get_users():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        return jsonify(data if data else [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO users (user_id, name, email, phone)
            VALUES (%s,%s,%s,%s)
        """, (
            data['user_id'],
            data['name'],
            data['email'],
            data['phone']
        ))

        db.commit()
        return jsonify({"message": "User added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE user
            SET name=%s, email=%s, phone=%s
            WHERE user_id=%s
        """, (
            data['name'],
            data['email'],
            data['phone'],
            id
        ))

        db.commit()
        return jsonify({"message": "User updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("DELETE FROM users WHERE user_id=%s", (id,))
        db.commit()
        return jsonify({"message": "User deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================================================
# 🔹 MERCHANT
# =========================================================
@app.route('/merchant', methods=['GET'])
def get_merchant():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM merchant")
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================================================
# 🔹 FRAUD (OPTIONAL)
# =========================================================
@app.route('/fraud_prediction', methods=['GET'])
def fraud_prediction():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fraud_prediction")
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================================================
>>>>>>> 18ee112 (updated db)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)