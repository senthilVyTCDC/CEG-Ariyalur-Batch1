from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import math

app = Flask(__name__)

<<<<<<< HEAD
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="revanth",
    database="CreditCardFraud"
=======
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rajesh",
        database="creditcardfraud",
        port=3306
    )

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/transaction')
def transaction():
    page = int(request.args.get('page', 1))
    per_page = 100
    offset = (page - 1) * per_page

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS count FROM transaction_")
    total = cursor.fetchone()['count']

    cursor.execute("""
        SELECT * FROM transaction_
        ORDER BY transaction_id ASC
        LIMIT %s OFFSET %s
    """, (per_page, offset))

    records = cursor.fetchall()

    cursor.close()
    db.close()

    total_pages = math.ceil(total / per_page)

    return render_template(
        "transaction.html",
        records=records,
        page=page,
        total_pages=total_pages
    )

@app.route('/transaction_add_form')
def transaction_add_form():
    return render_template("transaction_add.html")

@app.route('/transaction_add', methods=['POST'])
def add_transaction():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO transaction_
        (user_id, card_id, merchant_id, amount, transaction_time, status)
        VALUES (%s, %s, %s, %s, NOW(), %s)
    """, (
        request.form['user_id'],
        request.form['card_id'],
        request.form['merchant_id'],
        request.form['amount'],
        request.form['status']
    ))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('transaction'))

@app.route('/transaction_update/<int:id>', methods=['POST'])
def update_transaction(id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE transaction_
        SET amount=%s, status=%s
        WHERE transaction_id=%s
    """, (
        request.form['amount'],
        request.form['status'],
        id
    ))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('transaction'))

@app.route('/transaction_delete/<int:id>', methods=['POST'])
def delete_transaction(id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM transaction_ WHERE transaction_id=%s", (id,))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('transaction'))

dbconnection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    port=3306,
    database='CreditCardFraud'
>>>>>>> 5425bdd466abb6653976fcfbfe443e03648138a1
)

cursor = db.cursor(dictionary=True)

<<<<<<< HEAD
@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/transaction')
def transaction():
    cursor.execute("SELECT * FROM transaction_")
    data = cursor.fetchall()
    return render_template("transaction.html", records=data)

@app.route('/user')
def user():
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    return render_template("user.html", records=data)

# CREATE
@app.route('/add_user', methods=['POST'])
def add_user():
    user_id = request.form['user_id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
=======
@app.route('/card')
def Display_Card():
    cursor.execute("SELECT * FROM card")
    card = cursor.fetchall()
    return render_template('card.html', card=card)

@app.route('/card_add', methods=['GET', 'POST'])
def add_card():

    if request.method == 'POST':
>>>>>>> 5425bdd466abb6653976fcfbfe443e03648138a1

    cursor.execute(
        "INSERT INTO user (user_id,name, email, phone) VALUES (%s, %s, %s)",
        (name, email, phone)
    )
    db.commit()
    return redirect(url_for('user'))

<<<<<<< HEAD
# DELETE
@app.route('/delete_user/<int:id>')
def delete_user(id):
    cursor.execute("DELETE FROM user WHERE userid=%s", (id,))
    db.commit()
    return redirect(url_for('user'))
=======
        values = (
            request.form['user_id'],
            request.form['card_number'],
            request.form['card_type'],
            request.form['expiry_date']
        )
>>>>>>> 5425bdd466abb6653976fcfbfe443e03648138a1

# UPDATE
@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    cursor.execute("""
        UPDATE user
        SET name=%s, email=%s, phone=%s
        WHERE userid=%s
    """, (name, email, phone, id))

    db.commit()
    return redirect(url_for('user'))

<<<<<<< HEAD
=======
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

>>>>>>> 5425bdd466abb6653976fcfbfe443e03648138a1
if __name__ == "__main__":
    app.run(debug=True)