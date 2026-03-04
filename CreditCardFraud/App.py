from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import math

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

@app.route('/card')
def Display_Card():
    cursor.execute("SELECT * FROM card")
    card = cursor.fetchall()
    return render_template('card.html', card=card)

@app.route('/card_add', methods=['GET', 'POST'])
def add_card():

    if request.method == 'POST':

        values = (
            request.form['user_id'],
            request.form['card_number'],
            request.form['card_type'],
            request.form['expiry_date']
        )

        cursor.execute(
            "INSERT INTO card (user_id, card_number, card_type, expiry_date) VALUES (%s, %s, %s, %s)",
            values
        )

        dbconnection.commit()

        return redirect(url_for('Display_Card'))

    return render_template('add_card.html')

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

        return redirect(url_for('Display_Card'))

    cursor.execute("SELECT * FROM card WHERE card_id=%s", (card_id,))
    card = cursor.fetchone()

    return render_template('edit_card.html', card=card)

@app.route('/card_delete/<int:card_id>', methods=['POST'])
def delete_card(card_id):

    cursor.execute("DELETE FROM card WHERE card_id=%s", (card_id,))
    dbconnection.commit()

    return redirect(url_for('Display_Card'))

@app.route('/user')
def user():
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    return render_template("user.html", records=data)



@app.route('/merchant')
def merchant():
    return render_template("merchant.html")

if __name__ == "__main__":
    app.run(debug=True)