from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rajesh",
    database="creditcardfraud",
    port=3306
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

if __name__ == '__main__':
    app.run(debug=True)