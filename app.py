import os
from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors

app = Flask(__name__)

#mysql = MySQL(app)

@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM customer WHERE name = % s AND cid = % s', (username, password, ))
        # user = cursor.fetchone()
        # if user:              
        #     session['loggedin'] = True
        #     session['userid'] = user['cid']
        #     session['username'] = user['name']
        #     message = 'Logged in successfully!'
        #     return redirect(url_for('main_page'))
        # else:
        #     message = 'Please enter correct email / password !'
    return render_template('RegisterLogin/login.html', message = message)

@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form :
        email = request.form['email']
        password = request.form['password']
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM customer WHERE name = % s', (username, ))
    #     account = cursor.fetchone()
    #     if account:
    #         message = 'Choose a different username!'
  
    #     elif not username or not password:
    #         message = 'Please fill out the form!'

    #     else:
    #         cursor.execute('INSERT INTO customer (cid, name) VALUES (% s, % s)', (password, username))
    #         mysql.connection.commit()
    #         message = 'User successfully created!'

    # elif request.method == 'POST':
    #     message = 'Please fill all the fields!'

    return render_template('RegisterLogin/register.html', message = message)

#HOMEPAGE needs to be checked for trainer and trainee users

@app.route('/homepage')
def homepage():
    #if 'loggedin' in session:
        #userID = session['userid'] #cid = userID
        #cursor = mysql.connection.cursor()
        #cursor.execute("SELECT * FROM account JOIN owns ON account.aid = owns.aid JOIN customer ON owns.cid = customer.cid WHERE customer.cid = %s",(userID,))
        # * = account.aid, account.branch, account.balance, account.openDate
        # data = cursor.fetchall()
        # cursor.execute("SELECT name FROM customer WHERE cid = %s", (userID,))
        # name = cursor.fetchone()  # Fetch the name
        # cursor.close()
        #return render_template('main.html', account = data, customer = name) #html yaz dataları çek
    #return redirect(url_for('login'))

    return render_template('Homepage/homepg.html')

@app.route('/profile') # <aid> lazım
def profile():

    return render_template('Homepage/profile.html')

@app.route('/add-pt') 
def add_pt():
    
    return render_template('Homepage/add-pt.html')

@app.route('/add-goals')
def add_goals():

    return render_template('Homepage/add-goals.html')

@app.route('/my-goals')
def my_goals():

    return render_template('Homepage/my-goals.html')

@app.route('/workout-session')
def workout_session():

    return render_template('Homepage/workoutses.html')

# USER'S SELECTED TRAINER PAGE
@app.route('/program-page')#aid
def programs():

    return render_template('UsersTrainerPage/programs.html')

@app.route('/workout-program')#aid
def work_prog():

    return render_template('UsersTrainerPage/workoutprog.html')

@app.route('/nutr-program')#aid
def nutr_prog():

    return render_template('UsersTrainerPage/nutritionprog.html')

@app.route('/req-programs')#aid
def req_prog():

    return render_template('UsersTrainerPage/req-program.html')


if __name__ == "__main__":
    app.run(debug=True)