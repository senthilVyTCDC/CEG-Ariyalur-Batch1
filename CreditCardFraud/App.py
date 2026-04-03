from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# ---------- DB CONNECTION ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",   # change if needed
    database="creditcardfraud"
)

cursor = db.cursor(dictionary=True)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return "API Running 🚀"


# =========================================================
# 🔹 USER MODULE
# =========================================================
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM user")
    return jsonify(cursor.fetchall())


@app.route('/users', methods=['POST'])
def add_user():
    data = request.json

    cursor.execute("""
        INSERT INTO user (user_id, name, email, phone, age, gender, bank_name, account_type)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data['user_id'],
        data['name'],
        data['email'],
        data['phone'],
        data['age'],
        data['gender'],
        data['bank_name'],
        data['account_type']
    ))

    db.commit()
    return jsonify({"message": "User added"})


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json

    cursor.execute("""
        UPDATE user
        SET name=%s, email=%s, phone=%s
        WHERE user_id=%s
    """, (data['name'], data['email'], data['phone'], id))

    db.commit()
    return jsonify({"message": "User updated"})


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    cursor.execute("DELETE FROM user WHERE user_id=%s", (id,))
    db.commit()
    return jsonify({"message": "User deleted"})


# =========================================================
# 🔹 CARD MODULE
# =========================================================
@app.route('/cards', methods=['GET'])
def get_cards():
    cursor.execute("SELECT * FROM card")
    return jsonify(cursor.fetchall())


@app.route('/cards', methods=['POST'])
def add_card():
    data = request.json

    cursor.execute("""
        INSERT INTO card
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


@app.route('/cards/<int:id>', methods=['PUT'])
def update_card(id):
    data = request.json

    cursor.execute("""
        UPDATE card
        SET user_id=%s,
            card_number=%s,
            expiry_date=%s,
            card_limit=%s,
            last_used=%s
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


@app.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    cursor.execute("DELETE FROM card WHERE card_id=%s", (id,))
    db.commit()
    return jsonify({"message": "Card deleted"})


# =========================================================
# 🔹 TRANSACTION MODULE
# =========================================================
@app.route('/transactions', methods=['GET'])
def get_transactions():
    cursor.execute("SELECT * FROM transaction_")
    return jsonify(cursor.fetchall())


@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json

    cursor.execute("""
        INSERT INTO transaction_
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


@app.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    data = request.json

    cursor.execute("""
        UPDATE transaction_
        SET amount=%s,
            location=%s,
            category=%s,
            transaction_type=%s
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


@app.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    cursor.execute("DELETE FROM transaction_ WHERE transaction_id=%s", (id,))
    db.commit()
    return jsonify({"message": "Transaction deleted"})


# =========================================================
# 🔹 FRAUD MODULE
# =========================================================
@app.route('/fraud_prediction', methods=['GET'])
def fraud_prediction():
    cursor.execute("SELECT * FROM fraud_prediction")
    return jsonify(cursor.fetchall())


@app.route('/fraud_alert', methods=['GET'])
def fraud_alert():
    cursor.execute("SELECT * FROM fraud_alert")
    return jsonify(cursor.fetchall())


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)