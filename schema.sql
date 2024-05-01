CREATE TABLE User (
    user-ID INT PRIMARY KEY AUTO_INCREMENT,
    first-name VARCHAR(50) NOT NULL,
    last-name VARCHAR(50) NOT NULL,
    date-of-birth DATE,
    age INT,
    gender VARCHAR(10),
    email VARCHAR(100),
    password VARCHAR(100),
    phone-no VARCHAR(15) DEFAULT NULL,
    profile-pic VARCHAR(255) DEFAULT NULL,
    description TEXT DEFAULT NULL,
    achievements TEXT DEFAULT NULL
);

CREATE TABLE Admin (
    user-ID INT PRIMARY KEY,
    FOREIGN KEY (user-ID) REFERENCES User 
);

CREATE TABLE Trainer (
    user-ID INT PRIMARY KEY,
    specialization VARCHAR(255),
    certification VARCHAR(255),
    height INT
    weight INT
    FOREIGN KEY (user-ID) REFERENCES User
);


CREATE TABLE Trainee (
    user-ID INT PRIMARY KEY,
    fitness-goals VARCHAR(255), 
    height NUMERIC(3,2),
    weight NUMERIC(2,0),
    fat-percentage NUMERIC(3,2)
    FOREIGN KEY(user-ID) REFERENCES User
);

CREATE TABLE NutritionLog (
    log-ID INT PRIMARY KEY AUTO_INCREMENT,
    meal-items VARCHAR(255),
    calories-consumed INT
);

CREATE TABLE ExerciseLog (
    log-ID INT PRIMARY KEY AUTO_INCREMENT,
    duration NUMERIC(4,1) DEFAULT 0,
    exercise-list VARCHAR(255) DEFAULT NULL,
    notes VARCHAR(255) DEFAULT NULL,
    CONSTRAINT max_duration_check CHECK (duration <= 180.0)
);

CREATE TABLE NutritionPlan (
    plan-ID INT PRIMARY KEY AUTO_INCREMENT,
    trainee.user-ID INT,
    trainer.user-ID INT,
    plan-name VARCHAR(255),
    description VARCHAR(255),
    meal-items VARCHAR(255),
    FOREIGN KEY (trainee.user-ID) REFERENCES Trainee(user-ID),
    FOREIGN KEY (trainer.user-ID) REFERENCES Trainer(user-ID)
);

CREATE TABLE PremiumAccount (
    user-ID INT,
	premiumAcc-ID INT,
    start-date DATE,
    end-date DATE,
    payment-method VARCHAR(100),
    CONSTRAINT check-start-before-end CHECK (start-date < end-date),
    PRIMARY KEY (user-ID, premiumAcc-ID),
    FOREIGN KEY (user-ID) REFERENCES Users(user-ID)
);

CREATE TABLE Messages (
    sender-id INT,
    receiver-id INT,
    message VARCHAR(100),
    PRIMARY KEY (sender-id, receiver-id),
    FOREIGN KEY (sender-id) REFERENCES Users(user-id),
    FOREIGN KEY (receiver-id) REFERENCES Users(user-id)
);

CREATE TABLE ate (
    user-id INT,
    log-id INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    calories-taken INT,
    PRIMARY KEY (user-id, log-id),
    FOREIGN KEY (user-id) REFERENCES Users(user-id),
    FOREIGN KEY (log-id) REFERENCES NutritionLog(log-id)
);

CREATE TABLE done (
    user-ID INT,
    log-ID INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    calories-burned INT,
    PRIMARY KEY (user-ID, log-ID),
    FOREIGN KEY (user-ID) REFERENCES Users(user-id),
    FOREIGN KEY (log-ID) REFERENCES ExerciseLog(log-ID)
);

CREATE TABLE trains (
    trainee.user-ID INT,
    trainer.user-ID INT,
    start-date DATE,
    end-date DATE,
    recommendations VARCHAR(255) DEFAULT NULL,
    CONSTRAINT check-start-before-end CHECK (start-date < end-date)
    PRIMARY KEY (trainee.user-ID, trainer.user-ID),
    FOREIGN KEY (trainee.user-ID) REFERENCES Trainee(user-ID),
    FOREIGN KEY (trainer.user-ID) REFERENCES Trainer(user-ID)
);

CREATE TABLE planned-for (
    plan-ID INT,
    user-ID INT,
    start-date DATE,
    end-date DATE,
    CONSTRAINT check-start-before-end CHECK (start-date < end-date),
    PRIMARY KEY (user-ID, plan-ID),
    FOREIGN KEY (plan-ID) REFERENCES NutritionPlan(plan-ID),
    FOREIGN KEY (user-ID) REFERENCES Users(user-ID)
);

CREATE TABLE does (
    user-ID INT,
    routine-ID INT,
    exercise-ID INT,
    start-date DATE,
    end-date DATE,
    planned-calories INT,
    CONSTRAINT check-start-before-end CHECK (start-date < end-date)
    PRIMARY KEY (user-ID, routine-ID, exercise-ID),
    FOREIGN KEY (user-ID) REFERENCES Trainee(user-ID),
    FOREIGN KEY (routine-ID) REFERENCES ExerciseRoutinePlan(routine-ID),
    FOREIGN KEY (exercise-ID) REFERENCES Exercise(exercise-ID)
);

CREATE TABLE Exercise (
    exercise-ID INT PRIMARY KEY AUTO_INCREMENT,
    exercise-name VARCHAR(255) NOT NULL,
    description VARCHAR(255) DEFAULT NULL,
    target-muscles VARCHAR(255) DEFAULT NULL,
    difficulty_level INT CHECK(difficulty_level BETWEEN 1 AND 10),
    set-size INT,
    repeat-size INT
);

CREATE TABLE ExerciseRoutinePlan (
    routine-ID INT AUTO_INCREMENT PRIMARY KEY,
    routine-name VARCHAR(255),
    description VARCHAR(255),
    calories VARCHAR(50),
    intensity VARCHAR(255),
    duration VARCHAR(255),
    equipment VARCHAR(255),
    status VARCHAR(50),
    exercises-list VARCHAR(255)
);

CREATE TABLE PlansExercise (
    routine-ID INT,
    exercise-ID INT,
    user-ID INT,
    PRIMARY KEY (routine-ID, exercise-ID, user-ID),
    FOREIGN KEY (routine-ID) REFERENCES ExerciseRoutinePlan(routine-ID),
    FOREIGN KEY (exercise-ID) REFERENCES Exercise(exercise-ID),
    FOREIGN KEY (user-ID) REFERENCES Users(user-ID)
);

CREATE TABLE Contains (
    log-ID INT,
    exercise-ID INT,
    PRIMARY KEY (log-ID, exercise_ID),
    FOREIGN KEY (log-ID) REFERENCES ExerciseLog(log-ID),
    FOREIGN KEY (exercise-ID) REFERENCES Exercise(exercise-ID)
);

CREATE TABLE includes (
    routine-ID INT,
    exercise-ID INT,
    PRIMARY KEY (routine-ID, exercise-ID),
    FOREIGN KEY (routine-ID) REFERENCES ExerciseRoutinePlan(routine-ID),
    FOREIGN KEY (exercise-ID) REFERENCES Exercise(exercise-ID)
);

CREATE TABLE Requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    user_ID INT,
    note TEXT,
    type VARCHAR(50),
    FOREIGN KEY (user_ID) REFERENCES User(user-ID)
);

CREATE TABLE plans-nutrition(
	user-ID INT,
	plan-ID INT,
    PRIMARY KEY (user-ID, exercise-ID),
	FOREIGN KEY (user-ID) REFERENCES Trainer,
    FOREIGN KEY (plan-ID) REFERENCES NutritionPlan
);

INSERT INTO User (first-name, last-name, date-of-birth, age, gender, email, password, phone-no)
VALUES 
('Melih', 'Guven', '2002-04-01', 22, 'Male', 'melihhguvenn@gmail.com', 'asd123', '05056542789'),
('Kaan', 'Soyad', '2003-07-08', 20, 'Male', 'kaan@gmail.com', 'dsa321', '05050055513'),
('Yağız', 'Soyad', '2002-01-01', 22, 'Male', 'yagiz@gmail.com', 'yagiz', '05556557426'),
('Bartu', 'Soyad', '2000-01-04', 24, 'Male', 'bartu@gmail.com', 'bartu123', '05357861234');

INSERT INTO Admin (user-ID)
VALUES 
(1);

INSERT INTO Trainer (user-ID, specialization, certification, height, weight)
VALUES 
(1, 'Strength Training', 'Certified Strength Coach', 180, 80),
(2, 'Corssfit Training', 'Certification of Professional Crossfit Coach', 190, 83);

INSERT INTO Trainee (user-ID, fitness-goals, height, weight, fat-percentage)
VALUES 
(3, 'Weight Loss', 1.65, 90, 24.5);
(4, 'Body Build', 1.90, 100, 14);

INSERT INTO NutritionLog (meal-items, calories-consumed)
VALUES 
('Chicken salad', 350),
('Meat Doner', 780);

INSERT INTO ExerciseLog (duration, exercise-list, notes)
VALUES 
(90.0, 'Running, Squats', 'Rested for 2 minutes'),
(15, 'Triceps Pull Down', 'Superset');

INSERT INTO NutritionPlan (trainee.user-ID, trainer.user-ID, plan-name, description, meal-items)
VALUES 
(3, 1, 'Weight Loss Basic', 'Basic plan for weight loss, low calory', 'Oatmeal, Salad, Chicken Breast'),
(4,2,'Body Building Standard Calory', 'Rice, Chicken Breast, Salad');

INSERT INTO PremiumAccount (user-ID, premiumAcc-ID, start-date, end-date, payment-method)
VALUES 
(3, 101, '2023-01-01', '2024-01-01', 'Credit Card'),
(4, 102, '2023-02-02', '2024-02-02', 'Credit Card');

INSERT INTO Messages (sender-id, receiver-id, message)
VALUES 
(1, 3, 'Can you update my last program, it is hard for me'),
(3,1, 'Please text me the part you are struggling'),
(4,2,'This meet we could not talk. Tell me how was your exercise');

INSERT INTO ate (user-id, log-id, calories-taken)
VALUES 
(2, 1, 350),
(1,2,840);

INSERT INTO done (user-ID, log-ID, calories-burned)
VALUES 
(2, 1, 400),
(1,2,700);

INSERT INTO trains (trainee.user-ID, trainer.user-ID, start-date, end-date, recommendations)
VALUES 
(3, 1, '2023-01-01', '2023-06-01', 'Your tend to lose weight easy'),
(4,2,'2023-02-02', '2023-10-02','Keep doing good!');

INSERT INTO planned-for (user-ID, plan-ID, start-date, end-date)
VALUES 
(3, 1, '2023-01-01', '2023-03-01'),
(4,2,'2023-02-02', '2023-03-02');

INSERT INTO ExerciseRoutinePlan (routine-name, description, calories, intensity, duration, equipment, status, exercises-list)
VALUES 
('Basic Strength', 'Routine for beginners', '500', 'Medium', '60 mins', 'Dumbbells', 'Active', 'Push-ups, Pull-ups'),
('Losing Weight', 'Routine for low fat prercentage', '600', 'Advanced', '90 mins', 'Dumbells and bars', 'Active', 'Barbell curl, Triceps Pushdown');

INSERT INTO Exercise (exercise-name, description, target-muscles, difficulty_level, set-size, repeat-size)
VALUES 
('Push-up', 'Standard push-ups', 'Chest, Shoulders, Triceps', 5, 3, 15),
('Pull-up', 'Standard', 'Shoulders, Chest, Back', 8, 3, 12);

INSERT INTO Requests (user_ID, note, type)
VALUES 
(2, 'Need a custom plan', 'Nutrition');

INSERT INTO plans-nutrition (user-ID, plan-ID)
VALUES 
(1, 1),
(2, 2);

INSERT INTO includes (routine-ID, exercise-ID)
VALUES 
(1, 1),
(1, 2),
(2, 1),
(2, 2);

INSERT INTO Contains (log-ID, exercise-ID)
VALUES 
(1, 1),
(2, 2);

INSERT INTO PlansExercise (routine-ID, exercise-ID, user-ID)
VALUES 
(1, 1, 3),
(1, 2, 4),
(2, 1, 3),
(2, 2, 4);

INSERT INTO does (user-ID, routine-ID, exercise-ID, start-date, end-date, planned-calories)
VALUES 
(3, 1, 1, '2023-01-01', '2023-06-01', 500),
(4, 2, 2, '2023-02-02', '2023-10-02', 700);