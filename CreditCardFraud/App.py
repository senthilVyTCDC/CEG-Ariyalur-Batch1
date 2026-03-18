from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

dbconnection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rajesh",
    database="creditcardfraud",
    port=3306
)

cursor = dbconnection.cursor(dictionary=True)


@app.route('/')
def home():
    return "API Running 🚀"



@app.route('/transaction', methods=['GET'])
def transaction():
    cursor.execute("SELECT * FROM transaction_")
    return jsonify(cursor.fetchall())


@app.route('/transaction_add', methods=['POST'])
def transaction_add():
    data = request.json

    cursor.execute("""
        INSERT INTO transaction_
        (user_id, card_id, merchant_id, amount, transaction_time, status)
        VALUES (%s,%s,%s,%s,NOW(),%s)
    """, (
        data['user_id'],
        data['card_id'],
        data['merchant_id'],
        data['amount'],
        data['status']
    ))

    dbconnection.commit()
    return jsonify({"message": "Transaction added"})


@app.route('/transaction_update/<int:id>', methods=['PUT'])
def update_transaction(id):
    data = request.json

    cursor.execute("""
        UPDATE transaction_
        SET amount=%s, status=%s
        WHERE transaction_id=%s
    """, (data['amount'], data['status'], id))

    dbconnection.commit()
    return jsonify({"message": "Transaction updated"})


@app.route('/transaction_delete/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    cursor.execute("DELETE FROM transaction_ WHERE transaction_id=%s", (id,))
    dbconnection.commit()
    return jsonify({"message": "Transaction deleted"})



@app.route('/api/cards', methods=['GET'])
def get_cards():
    cursor.execute("SELECT * FROM card")
    return jsonify(cursor.fetchall())


@app.route('/api/cards', methods=['POST'])
def add_card():
    data = request.json

    cursor.execute("""
        INSERT INTO card (user_id, card_number, card_type, expiry_date)
        VALUES (%s,%s,%s,%s)
    """, (
        data['user_id'],
        data['card_number'],
        data['card_type'],
        data['expiry_date']
    ))

    dbconnection.commit()
    return jsonify({"message": "Card added"})


@app.route('/api/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    data = request.json

    cursor.execute("""
        UPDATE card
        SET user_id=%s, card_number=%s, card_type=%s, expiry_date=%s
        WHERE card_id=%s
    """, (
        data['user_id'],
        data['card_number'],
        data['card_type'],
        data['expiry_date'],
        card_id
    ))

    dbconnection.commit()
    return jsonify({"message": "Card updated"})


@app.route('/api/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    cursor.execute("DELETE FROM card WHERE card_id=%s", (card_id,))
    dbconnection.commit()
    return jsonify({"message": "Card deleted"})



@app.route('/user', methods=['GET'])
def user():
    cursor.execute("SELECT * FROM user")
    return jsonify(cursor.fetchall())


@app.route('/user_add', methods=['POST'])
def user_add():
    data = request.json

    cursor.execute("""
        INSERT INTO user (user_id, name, email, phone)
        VALUES (%s,%s,%s,%s)
    """, (
        data['user_id'],
        data['name'],
        data['email'],
        data['phone']
    ))

    dbconnection.commit()
    return jsonify({"message": "User added"})


@app.route('/user_update/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json

    cursor.execute("""
        UPDATE user
        SET name=%s,email=%s,phone=%s
        WHERE user_id=%s
    """, (
        data['name'],
        data['email'],
        data['phone'],
        id
    ))

    dbconnection.commit()
    return jsonify({"message": "User updated"})


@app.route('/user_delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    cursor.execute("DELETE FROM user WHERE user_id=%s", (id,))
    dbconnection.commit()
    return jsonify({"message": "User deleted"})


if __name__ == "__main__":
    app.run(debug=True)