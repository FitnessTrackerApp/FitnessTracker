from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/traineehomepage')
def traineehomepage():
    return render_template('traineehomepage.html')

@app.route('/traineeprofile')
def traineeprofile():
    return render_template('traineeprofile.html')


if __name__ == '__main__':
    app.run(debug=True)
