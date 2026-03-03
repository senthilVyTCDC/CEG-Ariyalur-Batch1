from flask import Flask, render_template
from mysql.connector import *

app = Flask(__name__)

dbconnection = connect(
    host='localhost',
    user='root',
    password='root@123',
    port='3306',
    database='fsdintern',
)
cursor = dbconnection.cursor(dictionary=True)

@app.route('/Home')
def Display_Student():
    cursor.execute("SELECT * FROM student")
    users = cursor.fetchall()   
    return render_template('indexdb.html', users=users)
    # return jsonify(users)


@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/user')
def User():
    return render_template('user.html')

@app.route('/card')
def Card():
    return render_template('card.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

if __name__ == '__main__':
    app.run(debug=True)