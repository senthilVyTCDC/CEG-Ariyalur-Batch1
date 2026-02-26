from flask import Flask, render_template
import mysql.connector   # ✅ correct import

app = Flask(__name__)

# Database Connection
dbconnection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    port=3306,   # ✅ integer
    database='CreditCardFraud'
)

cursor = dbconnection.cursor(dictionary=True)

@app.route('/')
def HOME():
    return render_template('index.html')

@app.route('/card')
def Display_Card():
    cursor.execute("SELECT * FROM card")
    card = cursor.fetchall()
    return render_template('card.html', card=card)

if __name__ == '__main__':
    app.run(debug=True)