import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'melih123'
app.config['MYSQL_DB'] = 'fitnesstrackerdb'

mysql = MySQL(app)

@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User  WHERE email = %s AND password = %s', (email, password, ))
        user = cursor.fetchone()
        if user:              
            session['loggedin'] = True
            session['userid'] = user['user_ID']
            session['username'] = user['first_name']
            message = 'Logged in successfully!'
            return redirect(url_for('homepage'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('RegisterLogin/login.html', message = message)

@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'first_name' in request.form and 'email' in request.form and 'password' in request.form :
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        b_date = request.form['date']
        email = request.form['email']
        password = request.form['password']
        typeOfUser = request.form['typeOfUser'] #!!!!
        gender = request.form['genderOfUser']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different email!'
  
        elif not email or not password:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO User (first_name, last_name, date_of_birth, age, gender, email, password, phone_no) VALUES (% s, % s, % s, % s, % s, % s, % s, % s)', (first_name, last_name, b_date, 0, gender, email, password, 0))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('RegisterLogin/register.html', message = message)

#HOMEPAGE needs to be checked for trainer and trainee users

@app.route('/homepage')
def homepage():
    if 'loggedin' in session:
        userID = session['userid'] #cid = userID
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT first_name, last_name FROM User WHERE user_ID = %s", (userID,))
        fname_lname = cursor.fetchone()  # Fetch the first name and last name

        cursor.close()
        return render_template('TraineePages/homepg.html', fname_lname = fname_lname) #html yaz dataları çek
    return redirect(url_for('login'))


@app.route('/profile') # <aid> lazım
def profile():

    return render_template('TraineePages/profile.html')

@app.route('/add-pt') 
def add_pt():
    
    return render_template('TraineePages/add-pt.html')

@app.route('/add-goal')
def add_goal():

    return render_template('TraineePages/add-goal.html')

@app.route('/my-goals')
def my_goals():

    return render_template('TraineePages/my-goals.html')

@app.route('/workout-session')
def workout_session():

    return render_template('TraineePages/workoutses.html')

# USER'S SELECTED TRAINER PAGE
@app.route('/programs')#aid
def programs():

    return render_template('TraineePages/UsersTrainerPage/programs.html')

@app.route('/workout-program')#aid
def work_prog():

    return render_template('TraineePages/UsersTrainerPage/workoutprog.html')

@app.route('/nutr-program')#aid
def nutr_prog():

    return render_template('TraineePages/UsersTrainerPage/nutritionprog.html')

@app.route('/req-programs')#aid
def req_prog():

    return render_template('TraineePages/UsersTrainerPage/req-program.html')

@app.route('/settings')#aid
def settings():

    return render_template('TraineePages/settings.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)