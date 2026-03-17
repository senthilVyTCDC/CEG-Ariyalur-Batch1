from flask import Flask, render_template, jsonify,request, redirect, url_for
import mysql.connector
import math

app = Flask(__name__)

dbconnection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="creditcardfraud",
    port=3306
)

cursor = dbconnection.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/transaction')
def transaction():

    page = int(request.args.get('page', 1))
    per_page = 100
    offset = (page - 1) * per_page

    cursor.execute("SELECT COUNT(*) AS count FROM transaction_")
    total = cursor.fetchone()['count']

    cursor.execute("""
        SELECT * FROM transaction_
        ORDER BY transaction_id ASC
        LIMIT %s OFFSET %s
    """, (per_page, offset))

    records = cursor.fetchall()

    total_pages = math.ceil(total / per_page)

    return render_template(
        "transaction.html",
        records=records,
        page=page,
        total_pages=total_pages
    )

@app.route('/transaction_add', methods=['GET', 'POST'])
def transaction_add():

    if request.method == 'POST':

        cursor.execute("""
            INSERT INTO transaction_
            (user_id, card_id, merchant_id, amount, transaction_time, status)
            VALUES (%s,%s,%s,%s,NOW(),%s)
        """, (
            request.form['user_id'],
            request.form['card_id'],
            request.form['merchant_id'],
            request.form['amount'],
            request.form['status']
        ))

        dbconnection.commit()

        return redirect(url_for('transaction'))

    return render_template("transaction_add.html")

@app.route('/transaction_update', methods=['GET'])
def transaction_update():
    return render_template("transaction_update.html")

@app.route('/transaction_update/<int:id>', methods=['POST'])
def update_transaction(id):

    cursor.execute("""
        UPDATE transaction_
        SET amount=%s, status=%s
        WHERE transaction_id=%s
    """, (
        request.form['amount'],
        request.form['status'],
        id
    ))

    dbconnection.commit()

    return redirect(url_for('transaction'))

@app.route('/transaction_delete', methods=['GET'])
def transaction_delete():
    return render_template("transaction_delete.html")

@app.route('/transaction_delete/<int:id>', methods=['POST'])
def delete_transaction(id):

    cursor.execute(
        "DELETE FROM transaction_ WHERE transaction_id=%s",
        (id,)
    )

    dbconnection.commit()

    return redirect(url_for('transaction'))

@app.route('/api/cards', methods=['GET'])
def get_cards():
    cursor.execute("SELECT * FROM card")
    cards = cursor.fetchall()
    return jsonify(cards)

@app.route('/api/cards', methods=['POST'])
def add_card_api():
    data = request.json

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

@app.route('/api/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    data = request.json

    sql = """
    UPDATE card
    SET user_id=%s, card_number=%s, card_type=%s, expiry_date=%s
    WHERE card_id=%s
    """

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

@app.route('/api/cards/<int:card_id>', methods=['DELETE'])
def delete_card_api(card_id):
    cursor.execute("DELETE FROM card WHERE card_id=%s", (card_id,))
    dbconnection.commit()

    return jsonify({"message": "Card deleted successfully"})

@app.route('/user')
def user():
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    return render_template("user.html", users=users)


@app.route('/user_add', methods=['GET','POST'])
def user_add():

    if request.method == 'POST':

        cursor.execute("""
        INSERT INTO user (user_id, name, email, phone)
        VALUES (%s,%s,%s,%s)
        """,(
            request.form['user_id'],
            request.form['name'],
            request.form['email'],
            request.form['phone']
        ))

        dbconnection.commit()

        return redirect(url_for('user'))

    return render_template("user_add.html")


@app.route('/user_update', methods=['GET'])
def user_update():
    return render_template("user_update.html")


@app.route('/user_update/<int:id>', methods=['POST'])
def update_user(id):

    cursor.execute("""
    UPDATE user
    SET name=%s,email=%s,phone=%s
    WHERE user_id=%s
    """,(
        request.form['name'],
        request.form['email'],
        request.form['phone'],
        id
    ))

    dbconnection.commit()

    return redirect(url_for('user'))


@app.route('/user_delete', methods=['GET'])
def user_delete():
    return render_template("user_delete.html")


@app.route('/user_delete/<int:id>', methods=['POST'])
def delete_user(id):

    cursor.execute("DELETE FROM user WHERE user_id=%s",(id,))
    dbconnection.commit()

    return redirect(url_for('user'))

@app.route('/merchant')
def merchant():
    return render_template("merchant.html")

if __name__ == "__main__":
    app.run(debug=True)