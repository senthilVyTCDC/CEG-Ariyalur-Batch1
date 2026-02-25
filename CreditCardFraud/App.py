from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="revanth",  # change this
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
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    print(data)   # 👈 ADD THIS LINE (important)
    return render_template("user.html", records=data)

if __name__ == "__main__":
    app.run(debug=True)