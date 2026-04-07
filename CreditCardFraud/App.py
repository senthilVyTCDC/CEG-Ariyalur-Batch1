from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# ---------- DB CONNECTION ----------
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


# ================= USERS =================
@app.route('/users', methods=['GET'])
def get_users():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()

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
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= CARDS =================
@app.route('/cards', methods=['GET'])
def get_cards():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cards")
        return jsonify(cursor.fetchall())
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
            (card_id, user_id, card_limit, card_status, usage_frequency)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            data['card_id'], data['user_id'],
            data['card_limit'], data['card_status'],
            data['usage_frequency']
        ))

        db.commit()
        return jsonify({"message": "Card added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= TRANSACTIONS =================
@app.route('/transactions_', methods=['GET'])
def get_transactions():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions_")
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/transactions_', methods=['POST'])
def add_transaction():
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # 🔹 Previous transaction
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

            current_time = datetime.strptime(
                data['transaction_time'], "%Y-%m-%d %H:%M:%S"
            )

            gap = int((current_time - previous_time).total_seconds() / 60)
        else:
            previous_time = data['transaction_time']
            previous_location = data['location']
            gap = 0

        # 🔹 Average amount
        cursor.execute("""
            SELECT AVG(amount) AS avg_amt 
            FROM transactions_
            WHERE user_id=%s
        """, (data['user_id'],))

        result = cursor.fetchone()
        avg_amt = result['avg_amt'] if result['avg_amt'] else data['amount']

        # 🔹 Insert
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

        db.commit()

        return jsonify({
            "message": "Transaction added",
            "gap": gap
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= FRAUD =================
@app.route('/detect_fraud', methods=['GET'])
def detect_fraud():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

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
                "risk_score": risk,
                "status": status
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)