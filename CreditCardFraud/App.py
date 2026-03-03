from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def Home():
    return render_template('card.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

if __name__ == '__main__':
    app.run(debug=True)