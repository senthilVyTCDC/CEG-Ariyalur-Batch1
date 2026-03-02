from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for  # ✅ correct import
import mysql.connector

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


# CREATE - Add New Card
@app.route('/add', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        user_id = request.form['user_id']
        card_number = request.form['card_number']
        card_type = request.form['card_type']
        expiry_date = request.form['expiry_date']

        sql = """
        INSERT INTO card (user_id, card_number, card_type, expiry_date)
        VALUES (%s, %s, %s, %s)
        """

        values = (user_id, card_number, card_type, expiry_date)

        cursor.execute(sql, values)
        dbconnection.commit()

        return redirect(url_for('Display_Card'))

    return render_template('add_card.html')


if __name__ == '__main__':
    app.run(debug=True)