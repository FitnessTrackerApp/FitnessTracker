from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)
