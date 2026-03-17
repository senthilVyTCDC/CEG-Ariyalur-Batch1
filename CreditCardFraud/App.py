from flask import Flask, render_template, jsonify,request, redirect, url_for
from flask import Flask, render_template,jsonify, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

dbconnection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    password="revanth",
    database="creditcardfraud",
    port=3306
)

cursor = dbconnection.cursor(dictionary=True)


@app.route('/')
def home():
    return render_template("index.html")


# ===============================
# TRANSACTION API (POSTMAN)
# ===============================

@app.route('/transaction', methods=['GET'])
def transaction():

    cursor.execute("SELECT * FROM transaction_")
    records = cursor.fetchall()

    return jsonify(records)


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

    return jsonify({"message": "Transaction added successfully"})


@app.route('/transaction_update/<int:id>', methods=['PUT'])
def update_transaction(id):

    data = request.json

    cursor.execute("""
        UPDATE transaction_
        SET amount=%s, status=%s
        WHERE transaction_id=%s
    """, (
        data['amount'],
        data['status'],
        id
    ))

    dbconnection.commit()

    return jsonify({"message": "Transaction updated successfully"})


@app.route('/transaction_delete/<int:id>', methods=['DELETE'])
def delete_transaction(id):

    cursor.execute(
        "DELETE FROM transaction_ WHERE transaction_id=%s",
        (id,)
    )

    dbconnection.commit()

    return jsonify({"message": "Transaction deleted successfully"})


@app.route('/api/cards', methods=['GET'])
def get_cards():



# ===============================
# CARD TABLE
# ===============================

@app.route('/card', endpoint='card')
def Display_Card():

    cursor.execute("SELECT * FROM card")
    cards = cursor.fetchall()
    return jsonify(cards)

@app.route('/api/cards', methods=['POST'])
def add_card_api():
    data = request.json


@app.route('/card_add', methods=['GET', 'POST'])
def add_card():


    values = (
        data['user_id'],
        data['card_number'],
        data['card_type'],
        data['expiry_date']
    )

    cursor.execute(
        "INSERT INTO card (user_id, card_number, card_type, expiry_date) VALUES (%s, %s, %s, %s)",
        values
    )
    dbconnection.commit()


    return jsonify({"message": "Card added successfully"})

    cursor.execute(
            "INSERT INTO card (user_id, card_number, card_type, expiry_date) VALUES (%s,%s,%s,%s)",
            values
        )


@app.route('/api/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    data = request.json
    sql = """
    UPDATE card
    SET user_id=%s, card_number=%s, card_type=%s, expiry_date=%s
    WHERE card_id=%s
    """
    return redirect(url_for('card'))


    values = (
        data['user_id'],
        data['card_number'],
        data['card_type'],
        data['expiry_date'],
        card_id
    )


    cursor.execute(sql, values)
    dbconnection.commit()

    return jsonify({"message": "Card updated successfully"})


@app.route('/edit/<int:card_id>', methods=['GET', 'POST'])
def edit_card(card_id):

    if request.method == 'POST':

        sql = """
        UPDATE card
        SET user_id=%s, card_number=%s, card_type=%s, expiry_date=%s
        WHERE card_id=%s
        """

        values = (
            request.form['user_id'],
            request.form['card_number'],
            request.form['card_type'],
            request.form['expiry_date'],
            card_id
        )

        cursor.execute(sql, values)
        dbconnection.commit()

        return redirect(url_for('card'))

    cursor.execute("SELECT * FROM card WHERE card_id=%s", (card_id,))
    card = cursor.fetchone()

    return render_template('edit_card.html', card=card)


@app.route('/card_delete/<int:card_id>', methods=['POST'])
def delete_card(card_id):
    cursor.execute("DELETE FROM card WHERE card_id=%s", (card_id,))
    dbconnection.commit()
    
    return redirect(url_for('card'))


@app.route('/api/cards/<int:card_id>', methods=['DELETE'])
def delete_card_api(card_id):
    cursor.execute("DELETE FROM card WHERE card_id=%s", (card_id,))
    dbconnection.commit()
    
    return jsonify({"message": "Card deleted successfully"})


# ===============================
# USER TABLE
# ===============================


@app.route('/user', methods=['GET'])
def user():
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    return jsonify(users)


@app.route('/user_add', methods=['POST'])
def user_add():
    try:
        cursor.execute("""
        INSERT INTO user (user_id, name, email, phone)
        VALUES (%s,%s,%s,%s)
        """, (
            request.json['user_id'],
            request.json['name'],
            request.json['email'],
            request.json['phone']
        ))

        dbconnection.commit()

        return jsonify({"message": "User added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user_update/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        cursor.execute("""
        UPDATE user
        SET name=%s,email=%s,phone=%s
        WHERE user_id=%s
        """, (
            request.json['name'],
            request.json['email'],
            request.json['phone'],
            id
        ))

        dbconnection.commit()

        return jsonify({"message": "User updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user_delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        cursor.execute("DELETE FROM user WHERE user_id=%s", (id,))
        dbconnection.commit()

        return jsonify({"message": "User deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/merchant')
def merchant():
    return render_template("merchant.html")


if __name__ == "__main__":
    app.run(debug=True)