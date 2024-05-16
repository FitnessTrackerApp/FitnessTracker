import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
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
            if typeOfUser == "trainee":
                checker = 0
                date_object = datetime.strptime(b_date, "%Y-%m-%d")
                year_integer = date_object.year
                cursor.execute('INSERT INTO User (first_name, last_name, date_of_birth, age, gender, email, password, phone_no, isTrainer) VALUES (% s, % s, % s, % s, % s, % s, % s, % s, %s)', (first_name, last_name, b_date, 2024 - year_integer, gender, email, password, 0, checker,))
            else:
                checker = 1
                date_object = datetime.strptime(b_date, "%Y-%m-%d")
                year_integer = date_object.year
                cursor.execute('INSERT INTO User (first_name, last_name, date_of_birth, age, gender, email, password, phone_no, isTrainer) VALUES (% s, % s, % s, % s, % s, % s, % s, % s, %s)', (first_name, last_name, b_date, 2024- 0, year_integer, email, password, 0, checker,))

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

        cursor.execute("SELECT isTrainer FROM User WHERE user_ID = %s", (userID,))
        trainer_info = cursor.fetchone()

        #cursor.close()

        if trainer_info['isTrainer'] == 0:

            #şimdi burada eğer daha önce eklenmediyse trainee tablosuna o zaman eklenmeli
            #yoksa her homepg bastığımızda ekleyebilir sıkıntı - INSERT IGNORE ?

            cursor.execute("INSERT IGNORE INTO Trainee (user_ID, height, weight, fat_percentage) VALUES (%s, %s, %s, %s)" , (userID,0,0,0,)) #diğer bilgileri profilde form olarak almalıyız
            return render_template('TraineePages/homepg.html', fname_lname = fname_lname)
        elif trainer_info['isTrainer'] == 1:
            # Fetch requests made to this trainer
            cursor.execute("""
                SELECT r.request_id, r.user_ID, r.note, r.type, u.first_name, u.last_name 
                FROM Requests r
                JOIN User u ON r.user_ID = u.user_ID
                WHERE r.trainer_ID = %s
            """, (userID,))
            requests = cursor.fetchall()

            return render_template('TrainerPages/trainerhomepg.html', fname_lname=fname_lname, requests=requests)
    return redirect(url_for('login'))


@app.route('/profile', methods =['GET', 'POST']) # <aid> lazım
def profile():
    if 'loggedin' in session:
        userID = session['userid'] #cid = userID
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT first_name, last_name FROM User WHERE user_ID = %s", (userID,))
        fname_lname = cursor.fetchone()  # Fetch the first name and last name

        cursor.execute("SELECT isTrainer FROM User WHERE user_ID = %s", (userID,))
        trainer_info = cursor.fetchone()

        message = ''

        if trainer_info[0] == 0:

            cursor.execute("SELECT age, gender, height, weight, fat_percentage FROM User, Trainee WHERE User.user_ID=%s AND User.user_ID=Trainee.user_ID",(userID,))
            data = cursor.fetchall()

            if request.method == 'POST' and 'height' in request.form and 'weight' in request.form and 'fat' in request.form:
                height = request.form['height']
                weight = request.form['weight']
                fatp = request.form['fat']

                #burası doğru mu?
                #weight ve height de sınır var hata veriyor oraya farklı handle lazım

                cursor.execute("UPDATE Trainee SET height = %s, weight = %s, fat_percentage = %s WHERE Trainee.user_ID = %s",(height,weight,fatp,userID,))
                mysql.connection.commit()

                cursor.execute("SELECT age, gender, height, weight, fat_percentage FROM User, Trainee WHERE User.user_ID=%s AND User.user_ID=Trainee.user_ID",(userID,))
                data = cursor.fetchall()

                cursor.close()
            else:
                message = 'Please fill everything'

            return render_template('TraineePages/profile.html', fname_lname = fname_lname, data = data, message=message)
        
        else:
            cursor.execute("SELECT age, gender, height, weight, specialization, certification FROM User, Trainer WHERE User.user_ID=%s AND User.user_ID=Trainer.user_ID",(userID,))
            data = cursor.fetchall()

            if request.method == 'POST' and 'height' in request.form and 'weight' in request.form:
                height = request.form['height']
                weight = request.form['weight']

                #burası doğru mu?
                #weight ve height de sınır var hata veriyor oraya farklı handle lazım

                cursor.execute("UPDATE Trainer SET height = %s, weight = %s WHERE Trainer.user_ID = %s",(height,weight,userID,))
                mysql.connection.commit()

                cursor.execute("SELECT age, gender, height, weight, specialization, certification FROM User, Trainer WHERE User.user_ID=%s AND User.user_ID=Trainer.user_ID",(userID,))
                data = cursor.fetchall()

                cursor.close()
            else:
                message = 'Please fill everything'
            return render_template('TrainerPages/trainerprofile.html', fname_lname = fname_lname, data=data, message = message)#html yaz dataları çek
            
    return redirect(url_for('login'))

@app.route('/add-pt') 
def add_pt():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM User U, Trainer T WHERE T.user_ID = U.user_ID") # User_ID iki kere geliyor onu fixleyelim
        data = cursor.fetchall()

        return render_template('TraineePages/add-pt.html', trainers=data)
    
    return redirect(url_for('login'))

@app.route('/add-goal',  methods =['GET', 'POST'])
def add_goal():
    if 'loggedin' in session:
        userID = session['userid'] #cid = userID
        cursor = mysql.connection.cursor()

        if request.method == 'POST':
            text_goal = request.form.get('goal')
            #print(text_goal)
            #değişecek burası
            cursor.execute("INSERT INTO FitnessGoals (user_ID, goal_description) VALUES (%s, %s)", (userID, text_goal,))

            mysql.connection.commit()

        return render_template('TraineePages/add-goal.html')
    
    return redirect(url_for('login'))

@app.route('/my-goals')
def my_goals():
    if 'loggedin' in session:

        userID = session['userid'] #cid = userID
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT goal_description, created_at FROM FitnessGoals WHERE user_ID = %s ", (userID,))
        goals_data = cursor.fetchall()

        return render_template('TraineePages/my-goals.html', goals_data=goals_data)
    
    return redirect(url_for('login'))

@app.route('/workout-session')
def workout_session():
    if 'loggedin' in session:
        return render_template('TraineePages/workoutses.html')
    return redirect(url_for('login'))

@app.route('/programs', methods=['GET', 'POST'])  # Updated to handle POST for form submission
def programs():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = session['user_id']  # The ID of the logged-in user (trainee)
        trainer_id = request.form.get('trainer_id')  # You need to get this from the form or context
        workout_request = request.form.get('workout_request')
        nutrition_request = request.form.get('nutrition_request')

        cursor = mysql.connection.cursor()

        # Check and insert workout and nutrition requests
        if workout_request:
            cursor.execute(
                'INSERT INTO Requests (user_ID, trainer_ID, note, type) VALUES (%s, %s, %s, %s)',
                (user_id, trainer_id, workout_request, 'Workout')
            )

        if nutrition_request:
            cursor.execute(
                'INSERT INTO Requests (user_ID, trainer_ID, note, type) VALUES (%s, %s, %s, %s)',
                (user_id, trainer_id, nutrition_request, 'Nutrition')
            )

        cursor.close()

        return redirect(url_for('some_success_page'))  # Redirect to a success page

    return render_template('TraineePages/UsersTrainerPage/programs.html')


@app.route('/workout-program')#aid
def work_prog():
    if 'loggedin' in session:
        return render_template('TraineePages/UsersTrainerPage/workoutprog.html')
    return redirect(url_for('login'))

@app.route('/nutr-program')#aid
def nutr_prog():
    if 'loggedin' in session:
        return render_template('TraineePages/UsersTrainerPage/nutritionprog.html')
    return redirect(url_for('login'))

@app.route('/req-programs')#aid
def req_prog():
    if 'loggedin' in session:
        return render_template('TraineePages/UsersTrainerPage/req-program.html')
    return redirect(url_for('login'))

@app.route('/settings')#aid
def settings():
    if 'loggedin' in session:
        return render_template('TraineePages/settings.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    #flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)