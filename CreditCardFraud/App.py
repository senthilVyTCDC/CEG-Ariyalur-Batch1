from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import math

app = Flask(__name__)

# ---------- Database Connection ----------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rajesh",   # change if needed
        database="creditcardfraud",
        port=3306
    )

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- READ with Pagination ----------------
@app.route('/transaction')
def transaction():
    page = int(request.args.get('page', 1))
    per_page = 100   # show 100 records per page
    offset = (page - 1) * per_page

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get total count
    cursor.execute("SELECT COUNT(*) AS count FROM transaction_")
    total = cursor.fetchone()['count']

    # Get paginated records in ascending order (lowest transaction_id first)
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

# ---------------- ADD FORM PAGE ----------------
@app.route('/add_form')
def add_form():
    return render_template("add.html")

@app.route('/add', methods=['POST'])
def add():
    db = get_db()
    cursor = db.cursor()
    try:
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
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('transaction'))

# ---------------- UPDATE FORM PAGE ----------------
@app.route('/update_form')
def update_form():
    return render_template("update.html")

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    amount = request.form.get('amount')
    status = request.form.get('status')

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE transaction_
            SET amount=%s, status=%s
            WHERE transaction_id=%s
        """, (amount, status, id))
        db.commit()
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('transaction'))

# ---------------- DELETE FORM PAGE ----------------
@app.route('/delete_form')
def delete_form():
    return render_template("delete.html")

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM transaction_ WHERE transaction_id=%s", (id,))
        db.commit()
    finally:
        cursor.close()
        db.close()
    return redirect(url_for('transaction'))

if __name__ == "__main__":
    app.run(debug=True)