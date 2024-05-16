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
    if request.method == 'POST' and 'first_name' in request.form and 'email' in request.form and 'password' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        b_date = request.form['date']
        email = request.form['email']
        password = request.form['password']
        typeOfUser = request.form['typeOfUser']
        gender = request.form['genderOfUser']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different email!'
        elif not email or not password:
            message = 'Please fill out the form!'
        else:
            date_object = datetime.strptime(b_date, "%Y-%m-%d")
            year_integer = date_object.year
            isTrainer = 1 if typeOfUser == "trainer" else 0
            cursor.execute('INSERT INTO User (first_name, last_name, date_of_birth, age, gender, email, password, phone_no, isTrainer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (first_name, last_name, b_date, 2024 - year_integer, gender, email, password, 0, isTrainer,))
            mysql.connection.commit()
            if isTrainer:
                cursor.execute('INSERT INTO Trainer (user_ID, specialization, certification, height, weight) VALUES (LAST_INSERT_ID(), %s, %s, %s, %s)', ('Not uploaded', 'Not uploaded', 0, 0,))
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

        if trainer_info[0] == 0:

            #şimdi burada eğer daha önce eklenmediyse trainee tablosuna o zaman eklenmeli
            #yoksa her homepg bastığımızda ekleyebilir sıkıntı - INSERT IGNORE ?

            # burada user ın personal trainerları fetch edilmeli
            cursor.execute("SELECT u.first_name, u.last_name, u.gender, u.age FROM User u JOIN Trainer t ON u.user_ID = t.user_ID JOIN trains tr ON tr.trainer_user_ID = t.user_ID WHERE tr.trainee_user_ID = %s" , (userID,))
            trains = cursor.fetchall()

            # bunu sonradan sil
            cursor.execute("SELECT U.first_name, U.last_name FROM CoachingRequests CR JOIN User U ON CR.trainer_user_ID = U.user_ID WHERE CR.trainee_user_ID = %s", (userID, ))
            trying = cursor.fetchone()

            cursor.execute("INSERT IGNORE INTO Trainee (user_ID, height, weight, fat_percentage) VALUES (%s, %s, %s, %s)" , (userID,0,0,0,)) #diğer bilgileri profilde form olarak almalıyız
            mysql.connection.commit()
            return render_template('TraineePages/homepg.html', fname_lname = fname_lname, trains = trains, trying = trying)
        else:
            return render_template('TrainerPages/trainerhomepg.html', fname_lname = fname_lname)#html yaz dataları çek
        
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

@app.route('/add-pt', methods =['GET', 'POST']) 
def add_pt():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM User U, Trainer T WHERE T.user_ID = U.user_ID") # User_ID iki kere geliyor onu fixleyelim
        data = cursor.fetchall()

        if request.method == 'POST':
            trainee_user_ID = session['userid']
            trainer_user_ID = request.form['trainer_user_ID']
            request_date = datetime.now().date()
            status = 'pending'

            # Check if the coaching request already exists
            cursor.execute("SELECT * FROM CoachingRequests WHERE trainee_user_ID = %s AND trainer_user_ID = %s", (trainee_user_ID, trainer_user_ID))
            existing_request = cursor.fetchone()
            if existing_request: 
                print("Already exists")
            else:
                cursor.execute("INSERT INTO CoachingRequests (trainee_user_ID, trainer_user_ID, request_date, status) VALUES (%s, %s, %s, %s)", (trainee_user_ID, trainer_user_ID, request_date, status))
                mysql.connection.commit()
        

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

# USER'S SELECTED TRAINER PAGE
@app.route('/programs')#aid
def programs():
    if 'loggedin' in session:
        return render_template('TraineePages/UsersTrainerPage/programs.html')
    return redirect(url_for('login'))

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