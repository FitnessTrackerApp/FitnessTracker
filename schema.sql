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