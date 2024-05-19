import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors

app = Flask(__name__)

mysql = MySQL(app)
app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'melih123'
app.config['MYSQL_DB'] = 'fitnesstrackerdb'

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
        if user:              #denem
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

@app.route('/homepage', methods = ['GET', 'POST'])
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
            cursor.execute("SELECT * FROM trains WHERE trainee_user_ID = %s", (userID,))
            coach_check = cursor.fetchall()

            # burada user ın personal trainerları fetch edilmeli
            cursor.execute("SELECT u.first_name, u.last_name, u.gender, u.age, tr.trainer_user_ID FROM User u JOIN Trainer t ON u.user_ID = t.user_ID JOIN trains tr ON tr.trainer_user_ID = t.user_ID WHERE tr.trainee_user_ID = %s" , (userID,))
            trains = cursor.fetchall()

            if request.method == 'POST' and 'deleteTrainer' in request.form:
                trainerDeleted = request.form.get('deleteTrainer')
                cursor.execute("DELETE FROM trains WHERE trainer_user_ID = %s AND trainee_user_ID = %s", (trainerDeleted, userID,))
                mysql.connection.commit()
                return redirect(url_for('homepage'))

            # Query to get the last added coaching request names
            query_last_added = """
            SELECT U1.first_name AS trainee_first_name, U1.last_name AS trainee_last_name, 
                U2.first_name AS trainer_first_name, U2.last_name AS trainer_last_name 
            FROM CoachingRequests
            JOIN User U1 ON CoachingRequests.trainee_user_ID = U1.user_ID
            JOIN User U2 ON CoachingRequests.trainer_user_ID = U2.user_ID
            ORDER BY CoachingRequests.request_id DESC;
            """
            cursor.execute(query_last_added)
            last_added = cursor.fetchall()

            cursor.execute("INSERT IGNORE INTO Trainee (user_ID, height, weight, fat_percentage) VALUES (%s, %s, %s, %s)" , (userID,0,0,0,)) #diğer bilgileri profilde form olarak almalıyız
            mysql.connection.commit()
            return render_template('TraineePages/homepg.html', fname_lname = fname_lname, trains = trains, last_added = last_added, coach_check = coach_check)
        
        else:

            # MY TRAINEES
            cursor.execute("SELECT u.first_name, u.last_name, u.gender, u.age, u.user_ID, t.height, t.weight, t.fat_percentage FROM User u JOIN Trainee t ON u.user_ID = t.user_ID JOIN trains tr ON tr.trainee_user_ID = t.user_ID WHERE tr.trainer_user_ID = %s" , (userID,))
            trainees = cursor.fetchall()

            if request.method == 'POST' and ('delete' in request.form):
                trainee_user_ID = int(request.form.get('delete'))
                
                cursor.execute("DELETE FROM trains WHERE trainee_user_ID = %s AND trainer_user_ID = %s", (trainee_user_ID, userID,))
                mysql.connection.commit()
                return redirect(url_for('homepage'))

            # PROGRAM REQUEST
            cursor.execute("SELECT u.first_name, u.last_name, r.note, r.type, r.request_ID, r.user_ID FROM Requests r JOIN User u ON r.user_ID = u.user_ID WHERE r.trainer_ID = %s", (userID,))
            program_requests = cursor.fetchall()

            if request.method == 'POST' and ('acceptpr' in request.form or 'denypr' in request.form):
                # burada program requesti Requests den delete edilcek && type ına göre başka sayfalara yönlendirilcek
                trainee_user_ID = None
                request_id = None
                if 'acceptpr' in request.form:
                    # accept ettiği anda NutritionPlan a insert etcez.
                    accept_value = request.form['acceptpr']
                    request_id, trainee_user_ID, type = accept_value.split('|')
                    request_id = int(request_id)
                    trainee_user_ID = int(trainee_user_ID)

                    # delete from the Requests
                    cursor.execute("DELETE FROM Requests WHERE user_ID = %s AND trainer_ID = %s AND request_id = %s", (trainee_user_ID, userID, request_id))
                    mysql.connection.commit()
                    if type == 'Workout':
                        # Same for workout will be done (like below)
                        return redirect(url_for('workoutassign', trainee_user_ID = trainee_user_ID)) #yine planID verelim
                        
                    elif type == 'Nutrition':
                        #default bir plan oluşturuyoruz
                        cursor.execute("INSERT INTO NutritionPlan (trainee_user_ID, trainer_user_ID, plan_name, description) VALUES (%s, %s, %s, %s)", (trainee_user_ID, userID, "Plan", "description",))
                        mysql.connection.commit()
                        # plan_ID yi çekmemiz lazım                       
                        cursor.execute("SELECT plan_ID FROM NutritionPlan WHERE trainee_user_ID = %s AND trainer_user_ID = %s ORDER BY plan_ID DESC", (trainee_user_ID, userID,))
                        plan_ID = cursor.fetchone()[0]
                        session['plan_ID'] = plan_ID
                        
                        return redirect(url_for('mealassign'))
            
                elif 'denypr' in request.form:

                    deny_value = request.form['denypr']
                    request_id, trainee_user_ID, type = deny_value.split('|')
                    request_id = int(request_id)
                    trainee_user_ID = int(trainee_user_ID)

                    # delete from the Requests
                    cursor.execute("DELETE FROM Requests WHERE user_ID = %s AND trainer_ID = %s AND request_id = %s", (trainee_user_ID, userID, request_id))
                    mysql.connection.commit()
                    return redirect(url_for('homepage'))

                    
            #COACHING REQUEST
            # burada trainer a gelen istekler fetch edilmeli (trainee nin userID si de paslanmalı)
            cursor.execute("SELECT u.first_name, u.last_name, u.gender, u.age, t.height, t.weight, u.user_ID, t.fat_percentage FROM User u JOIN Trainee t ON u.user_ID = t.user_ID JOIN CoachingRequests CR ON CR.trainee_user_ID = t.user_ID WHERE CR.trainer_user_ID = %s", (userID,))
            requests = cursor.fetchall()

            # implement the delete logic from traines
            

            if request.method == 'POST' and ('accept' in request.form or 'deny' in request.form):
                trainee_user_ID = None
                if 'accept' in request.form:
                    trainee_user_ID = int(request.form.get('accept'))
                    # burada request silinip trainee ve trainer trains tablosuna eklenmeli
                    cursor.execute("DELETE FROM CoachingRequests WHERE trainee_user_ID = %s", (trainee_user_ID,))
                    mysql.connection.commit()

                    #control and adding
                    cursor.execute("SELECT COUNT(*) FROM trains WHERE trainee_user_ID = %s AND trainer_user_ID = %s", (trainee_user_ID, userID,))
                    count = cursor.fetchone()[0]
                    if count == 0:
                        cursor.execute("INSERT INTO trains (trainee_user_ID, trainer_user_ID) VALUES (%s, %s)", (trainee_user_ID, userID,))
                        mysql.connection.commit()
                        return redirect(url_for('homepage'))
                    

                elif 'deny' in request.form:
                    trainee_user_ID = int(request.form.get('deny'))
                    # burada sadece request silinmeli
                    cursor.execute("DELETE FROM CoachingRequests WHERE trainee_user_ID = %s AND trainer_user_ID = %s", (trainee_user_ID, userID,))
                    mysql.connection.commit()
                    return redirect(url_for('homepage'))

            return render_template('TrainerPages/trainerhomepg.html', fname_lname = fname_lname ,requests=requests, trainees = trainees, program_requests = program_requests)#html yaz dataları çek
        
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

        bmi = "Enter values to calculate BMI"
        bmitext = ""

        if trainer_info[0] == 0:

            cursor.execute("SELECT * FROM TrainerTraineeInfo WHERE trainee_ID = %s", (userID,))
            trainer_info = cursor.fetchall()

            cursor.execute("SELECT age, gender, height, weight, fat_percentage FROM User, Trainee WHERE User.user_ID=%s AND User.user_ID=Trainee.user_ID",(userID,))
            data = cursor.fetchall()

            cursor.execute("SELECT np.plan_ID, np.plan_name, np.description, u.first_name AS trainer_first_name, u.last_name AS trainer_last_name FROM NutritionPlan np JOIN User u ON np.trainer_user_ID = u.user_ID WHERE np.trainee_user_ID = %s", (userID,))
            nutrition_plans = cursor.fetchall()

            cursor.execute("SELECT erp.*, u.first_name, u.last_name FROM ExerciseRoutinePlan erp JOIN does d ON erp.routine_ID = d.routine_ID JOIN User u ON d.user_ID = u.user_ID WHERE d.user_ID = %s", (userID,))
            workout_plans = cursor.fetchall()

            height = data[0][2]
            weight = data[0][3]
            if height > 0 and weight > 0:
                bmi = weight / ((height/100) ** 2)
                if bmi < 18.4:
                    bmitext = "Underweight"
                elif bmi < 24.9:
                    bmitext = "Normal"
                elif bmi < 39.9:
                    bmitext = "Overweight"
                else:
                    bmitext = "Obese"

            if request.method == 'POST' and 'height' in request.form and 'weight' in request.form and 'fat' in request.form:
                height = request.form['height']
                weight = request.form['weight']
                fatp = request.form['fat']

                if height.isdigit():
                    height = int(height)
                else:
                    height = -1
                if weight.isdigit():
                    weight = int(weight)
                else:
                    weight = -1
                if fatp[0] == '%' and fatp[1:].isdigit():
                    height = int(height)
                    weight = int(weight)
                    fatp = int(fatp[1:])
                    
                else:
                    message = 'Please enter a valid fat percentage'
                    fatp = -1
    
                
                #burası doğru mu? -----------------DOĞRU-----------------
                #weight ve height de sınır var hata veriyor oraya farklı handle lazım
                if(height < 0 or height > 300):
                    message = 'Please enter a valid height(0-300)'
                    bmi= "cannot be calculated"
                elif(weight < 0 or weight > 300):
                    message = 'Please enter a valid weight(0-300)'
                    bmi= "cannot be calculated"
                elif(fatp < 0 or fatp > 100):
                    message = 'Please enter a valid fat percentage (%0-100)'
                    bmi= "cannot be calculated"
                else:
                    if height > 0 and weight > 0:
                        bmi = weight / ((height/100) ** 2)
                    else:
                        bmi = "cannot be calculated"

                    if bmi != "cannot be calculated":
                        if bmi < 18.4:
                            bmitext = "Underweight"
                        elif bmi < 24.9:
                            bmitext = "Normal"
                        elif bmi < 39.9:
                            bmitext = "Overweight"
                        else:
                            bmitext = "Obese"
                    cursor.execute("UPDATE Trainee SET height = %s, weight = %s, fat_percentage = %s WHERE Trainee.user_ID = %s",(height,weight,fatp,userID,))
                    mysql.connection.commit()

                    cursor.execute("SELECT age, gender, height, weight, fat_percentage FROM User, Trainee WHERE User.user_ID=%s AND User.user_ID=Trainee.user_ID",(userID,))
                    data = cursor.fetchall()

                    cursor.close()
            else:
                message = 'Please fill everything'

            return render_template('TraineePages/profile.html', fname_lname = fname_lname, data = data, message=message, trainer_info=trainer_info, bmi= "cannot be calculated" if bmi == "cannot be calculated" else ("Enter values to calculate BMI" if bmi == "Enter values to calculate BMI" else (str(round(bmi, 2)) + " (" + bmitext + ")")),nutrition_plans=nutrition_plans, workout_plans=workout_plans)
        
        else:
            cursor.execute("SELECT age, gender, height, weight, specialization, certification FROM User, Trainer WHERE User.user_ID=%s AND User.user_ID=Trainer.user_ID",(userID,))
            data = cursor.fetchall()

            if request.method == 'POST' and 'height' in request.form and 'weight' in request.form:
                height = request.form['height']
                weight = request.form['weight']

                if height.isdigit():
                    height = int(height)
                else:
                    height = -1
                if weight.isdigit():
                    weight = int(weight)
                else:
                    weight = -1

                #burası doğru mu? ------------DOĞRU------------------
                #weight ve height de sınır var hata veriyor oraya farklı handle lazım

                if(height < 0 or height > 300):
                    message = 'Please enter a valid height(0-300)'
                elif(weight < 0 or weight > 300):
                    message = 'Please enter a valid weight(0-300)'
                else:
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
                print("Request already exists.") # instead of this we can use some kind of pop uf window in frontend (idk how)
            else:
                cursor.execute("SELECT COUNT(*) FROM trains WHERE trainee_user_ID = %s", (trainee_user_ID,))
                count = cursor.fetchone()[0]
                if count == 0:
                    cursor.execute("INSERT INTO CoachingRequests (trainee_user_ID, trainer_user_ID, request_date, status) VALUES (%s, %s, %s, %s)", (trainee_user_ID, trainer_user_ID, request_date, status))
                    mysql.connection.commit()
                else:
                    print("You already have a trainer") # instead of this we can use some kind of pop uf window in frontend (idk how)

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
            return redirect(url_for('my_goals'))

        return render_template('TraineePages/add-goal.html')
    
    return redirect(url_for('login'))

@app.route('/my-goals')
def my_goals():
    if 'loggedin' in session:

        userID = session['userid'] #cid = userID
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM UserGoalsDetails WHERE user_ID = %s ", (userID,))
        goals_data = cursor.fetchall()

        return render_template('TraineePages/my-goals.html', goals_data=goals_data)
    
    return redirect(url_for('login'))

@app.route('/workout-session', methods=['GET', 'POST'])
def workout_session():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM ExerciseRoutinePlan WHERE 1=1"
        filters = []

        if request.method == 'POST' and 'filter' in request.form:
            intensity = request.form.get('intensity')
            duration = request.form.get('duration')
            equipment = request.form.get('equipment')

            if intensity:
                query += " AND intensity LIKE %s"
                filters.append(f"%{intensity}%")
            if duration:
                query += " AND duration LIKE %s"
                filters.append(f"%{duration}%")
            if equipment:
                query += " AND equipment LIKE %s"
                filters.append(f"%{equipment}%")

            cursor.execute(query, tuple(filters))
        elif request.method == 'POST' and 'reset' in request.form:
            query = "SELECT * FROM ExerciseRoutinePlan WHERE 1=1"
            cursor.execute(query)
        else:
            cursor.execute(query)

        exercise_plans = cursor.fetchall()
        return render_template('TraineePages/workoutses.html', exercise_plans=exercise_plans)
    return redirect(url_for('login'))

@app.route('/programs', methods=['GET', 'POST'])  # Updated to handle POST for form submission
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
        userID = session['userid'] #cid = userID
        cursor = mysql.connection.cursor()

        # Fetch all nutrition plans for the logged-in user
        cursor.execute("SELECT plan_ID, plan_name FROM NutritionPlan WHERE trainee_user_ID = %s", (userID,))
        plans = cursor.fetchall()

        # Create a dictionary to store the meals for each plan
        plans_with_meals = {}
        for plan in plans:
            plan_id, plan_name = plan
            cursor.execute("SELECT M.name, M.calories, P.quantity FROM PlanIncludesMealItem P JOIN MealItem M ON P.meal_item_ID = M.meal_item_ID WHERE P.plan_ID = %s", (plan_id,))
            meals = cursor.fetchall()
            plans_with_meals[plan_name] = meals

        return render_template('TraineePages/UsersTrainerPage/nutritionprog.html', plans_with_meals=plans_with_meals)
    return redirect(url_for('login'))

@app.route('/req-programs', methods=['GET', 'POST'])#aid
def req_prog():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        user_id = session['userid']  # The ID of the logged-in user (trainee)
            
        cursor.execute(" SELECT trainer_user_ID FROM trains WHERE trainee_user_ID = %s", (user_id,))
        trainer_id = cursor.fetchone()

        cursor.execute("SELECT first_name, last_name FROM User WHERE user_ID = %s", (trainer_id,))
        names = cursor.fetchone()

        if request.method == 'POST':

            workoutrequest = request.form.get('workout_request')
            nutritionrequest = request.form.get('nutrition_request')

            # Check and insert workout and nutrition requests
            if workoutrequest != None:
                cursor.execute("INSERT INTO Requests (user_ID, trainer_ID, note, type) VALUES (%s, %s, %s, %s)", (user_id, trainer_id, workoutrequest, 'Workout',))
                mysql.connection.commit()
            elif nutritionrequest != None:
                cursor.execute("INSERT INTO Requests (user_ID, trainer_ID, note, type) VALUES (%s, %s, %s, %s)", (user_id, trainer_id, nutritionrequest, 'Nutrition',))
                mysql.connection.commit()

        return render_template('TraineePages/UsersTrainerPage/req-program.html', names = names)

    return redirect(url_for('login'))

@app.route('/correspondingtraineelog/<int:trainee_id>')
def correspondingtraineelog(trainee_id):
    if 'loggedin' in session:
        trainer_id = session['userid']  # Assuming the logged-in user is the trainer
        cursor = mysql.connection.cursor()

        # Query to fetch workout plans specific to the logged-in trainer and the selected trainee
        cursor.execute("SELECT erp.*, u.first_name, u.last_name FROM ExerciseRoutinePlan erp JOIN does d ON erp.routine_ID = d.routine_ID JOIN User u ON d.user_ID = u.user_ID WHERE d.user_ID = %s", (trainee_id,))
        workout_logs = cursor.fetchall()
        
        # Query to fetch nutrition plans specific to the logged-in trainer and the selected trainee
        cursor.execute("SELECT np.*, u.first_name, u.last_name FROM NutritionPlan np JOIN User u ON np.trainee_user_ID = u.user_ID WHERE np.trainee_user_ID = %s AND np.trainer_user_ID = %s", (trainee_id, trainer_id))
        nutrition_logs = cursor.fetchall()

        return render_template('TrainerPages/correspondingtraineelog.html', workout_logs=workout_logs, nutrition_logs=nutrition_logs)
    return redirect(url_for('login'))

@app.route('/mealassign/<int:trainee_user_ID>')
def mealassign(trainee_user_ID):
    if 'loggedin' in session:
        # Here there will be  'add' buttons for each meal which has value as meal_item_ID (MealItem table). 
        # When the accept the meal request it should already create a (NutritionPlan) with plan name to be defined later. 
        # When we tap to add Button it will insert to the PlanIncludesMealItem table (we can insert the same meal for multiple times if we want to by keeping the quantity (if - else statement)). 
        # Finally when we write the name of the program and tap 'Done' it will update the plan_name.
        plan_ID = session['plan_ID']
        cursor = mysql.connection.cursor()
        #user_id = session['userid'] # this is trainerID

        #cursor.execute("SELECT * FROM NutritionPlan WHERE plan_ID = %s", (plan_ID,))
        #trainee_user_ID = cursor.fetchone()[1]

        if request.method == 'POST':
            if 'addmeal' in request.form:
                # Eğer meal item plande hiç yoksa ekle, varsa quantity i arttır.
                meal_item_ID = request.form.get('addmeal') #butondan çekecez
                cursor.execute("SELECT COUNT(*) FROM PlanIncludesMealItem WHERE plan_ID = %s AND meal_item_ID = %s", (plan_ID, meal_item_ID,))
                count_of_meal = cursor.fetchone()[0]
                if count_of_meal == 0:
                    cursor.execute("INSERT INTO PlanIncludesMealItem (plan_ID, meal_item_ID, quantity) VALUES (%s, %s, %s)", (plan_ID, meal_item_ID, count_of_meal,))
                    mysql.connection.commit()
                else:
                    cursor.execute("UPDATE PlanIncludesMealItem SET quantity = %s WHERE plan_ID = %s", (count_of_meal + 1, plan_ID,))
                    mysql.connection.commit()
                # we can do return redirect here
                return redirect(url_for('mealassign'))
            
            if 'removemeal' in request.form:
                meal_item_ID = request.form.get('removemeal') #butondan çekecez
                cursor.execute("DELETE FROM PlanIncludesMealItem WHERE plan_ID = %s AND meal_item_ID = %s ",(plan_ID, meal_item_ID,))
                mysql.connection.commit()
                return redirect(url_for('mealassign'))

                
            if 'done' in request.form:
                plan_name = request.form.get('plan_name') #butondan çekecez
                cursor.execute("UPDATE NutritionPlan SET plan_name = %s WHERE plan_ID = %s", (plan_name, plan_ID))
                mysql.connection.commit()
                return redirect(url_for('homepage'))
            
        
        # Burada databasedeki bütün mealları çekmemiz lazım 
        cursor.execute("SELECT * FROM MealItem")
        meal_items = cursor.fetchall()

        # Burada mevcut plana eklediğimiz mealları çekmek lazım
        cursor.execute("SELECT P.meal_item_ID, P.quantity, M.name FROM PlanIncludesMealItem P, MealItem M WHERE P.plan_ID = %s AND P.meal_item_ID = M.meal_item_ID", (plan_ID,))
        current_meal_items = cursor.fetchall()

        return render_template('TrainerPages/mealassign.html', meal_items = meal_items, current_meal_items = current_meal_items, )
    return redirect(url_for('login'))

# URL den user id çekilmeli
@app.route('/workoutassign/<int:trainee_user_ID>')
def workoutassign(trainee_user_ID):
    if 'loggedin' in session:
        return render_template('TrainerPages/workoutassign.html', trainee_user_ID = trainee_user_ID)
    return redirect(url_for('login'))


@app.route('/personal-workout-program')#aid
def personal_work_prog():
    if 'loggedin' in session:
        return render_template('TraineePages/personalworkoutprogram.html')
    return redirect(url_for('login'))

@app.route('/personal-diet-program')#aid
def personal_diet_prog():
    if 'loggedin' in session:
        return render_template('TraineePages/personaldietprogram.html')
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