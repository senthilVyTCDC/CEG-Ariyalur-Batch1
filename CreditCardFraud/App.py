from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="revanth",
    database="CreditCardFraud"
)

cursor = db.cursor(dictionary=True)

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

    cursor.execute(
        "INSERT INTO user (user_id,name, email, phone) VALUES (%s, %s, %s)",
        (name, email, phone)
    )
    db.commit()
    return redirect(url_for('user'))

# DELETE
@app.route('/delete_user/<int:id>')
def delete_user(id):
    cursor.execute("DELETE FROM user WHERE userid=%s", (id,))
    db.commit()
    return redirect(url_for('user'))

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

if __name__ == "__main__":
    app.run(debug=True)