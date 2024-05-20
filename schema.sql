CREATE TABLE User (
    user_ID INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    age INT,
    gender VARCHAR(10),
    email VARCHAR(100),
    password VARCHAR(100),
    phone_no VARCHAR(15) DEFAULT NULL,
    profile_pic VARCHAR(255) DEFAULT NULL,
    description TEXT DEFAULT NULL,
    achievements TEXT DEFAULT NULL,
    isTrainer INT
);

CREATE TABLE Admin (
    user_ID INT PRIMARY KEY,
    FOREIGN KEY (user_ID) REFERENCES User(user_ID)
);

CREATE TABLE Trainer (
    user_ID INT PRIMARY KEY,
    specialization VARCHAR(255),
    certification VARCHAR(255),
    height INT,
    weight INT,
    FOREIGN KEY (user_ID) REFERENCES User(user_ID)
);

CREATE TABLE Trainee (
    user_ID INT PRIMARY KEY,
    height INT,
    weight INT,
    fat_percentage INT,
    FOREIGN KEY(user_ID) REFERENCES User(user_ID)
);

CREATE TABLE FitnessGoals (
    goal_ID INT PRIMARY KEY AUTO_INCREMENT,
    user_ID INT,
    goal_description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_ID) REFERENCES User(user_ID)
);

CREATE TABLE NutritionLog (
    log_ID INT PRIMARY KEY AUTO_INCREMENT,
    meal_items VARCHAR(255),
    calories_consumed INT
);

CREATE TABLE ExerciseLog (
    log_ID INT PRIMARY KEY AUTO_INCREMENT,
    duration NUMERIC(4,1) DEFAULT 0,
    exercise_list VARCHAR(255) DEFAULT NULL,
    notes VARCHAR(255) DEFAULT NULL,
    CONSTRAINT max_duration_check CHECK (duration <= 180.0)
);

CREATE TABLE NutritionPlan (
    plan_ID INT PRIMARY KEY AUTO_INCREMENT,
    trainee_user_ID INT,
    trainer_user_ID INT,
    plan_name VARCHAR(255),
    meal_items VARCHAR(255),
    description VARCHAR(255),
    FOREIGN KEY (trainee_user_ID) REFERENCES Trainee(user_ID),
    FOREIGN KEY (trainer_user_ID) REFERENCES Trainer(user_ID)
);

CREATE TABLE MealItem (
    meal_item_ID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    calories INT NOT NULL
);

CREATE TABLE PlanIncludesMealItem (
    plan_ID INT,
    meal_item_ID INT,
    quantity INT,
    PRIMARY KEY (plan_ID, meal_item_ID),
    FOREIGN KEY (plan_ID) REFERENCES NutritionPlan(plan_ID),
    FOREIGN KEY (meal_item_ID) REFERENCES MealItem(meal_item_ID)
);


CREATE TABLE PremiumAccount (
    user_ID INT,
    premiumAcc_ID INT,
    start_date DATE,
    end_date DATE,
    payment_method VARCHAR(100),
    CONSTRAINT check_start_before_end CHECK (start_date < end_date),
    PRIMARY KEY (user_ID, premiumAcc_ID),
    FOREIGN KEY (user_ID) REFERENCES User(user_ID)
);

CREATE TABLE Messages (
    sender_id INT,
    receiver_id INT,
    message VARCHAR(100),
    PRIMARY KEY (sender_id, receiver_id),
    FOREIGN KEY (sender_id) REFERENCES User(user_ID),
    FOREIGN KEY (receiver_id) REFERENCES User(user_ID)
);

CREATE TABLE ate (
    user_id INT,
    log_id INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    calories_taken INT,
    PRIMARY KEY (user_id, log_id),
    FOREIGN KEY (user_id) REFERENCES User(user_ID),
    FOREIGN KEY (log_id) REFERENCES NutritionLog(log_ID)
);

CREATE TABLE done (
    user_ID INT,
    log_ID INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    calories_burned INT,
    PRIMARY KEY (user_ID, log_ID),
    FOREIGN KEY (user_ID) REFERENCES User(user_ID),
    FOREIGN KEY (log_ID) REFERENCES ExerciseLog(log_ID)
);

CREATE TABLE trains (
    trainee_user_ID INT,
    trainer_user_ID INT,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date DATE,
    recommendations VARCHAR(255) DEFAULT NULL,
    CONSTRAINT check_start_before_end CHECK (start_date < end_date),
    PRIMARY KEY (trainee_user_ID, trainer_user_ID),
    FOREIGN KEY (trainee_user_ID) REFERENCES Trainee(user_ID),
    FOREIGN KEY (trainer_user_ID) REFERENCES Trainer(user_ID)
);

CREATE TABLE planned_for (
    plan_ID INT,
    user_ID INT,
    start_date DATE,
    end_date DATE,
    CONSTRAINT check_start_before_end CHECK (start_date < end_date),
    PRIMARY KEY (user_ID, plan_ID),
    FOREIGN KEY (user_ID) REFERENCES User(user_ID),
    FOREIGN KEY (plan_ID) REFERENCES NutritionPlan(plan_ID)
);

CREATE TABLE Exercise (
    exercise_ID INT PRIMARY KEY AUTO_INCREMENT,
    exercise_name VARCHAR(255) NOT NULL,
    description VARCHAR(255) DEFAULT NULL,
    target_muscles VARCHAR(255) DEFAULT NULL,
    difficulty_level INT CHECK(difficulty_level BETWEEN 1 AND 10),
    set_size INT,
    repeat_size INT
);

CREATE TABLE ExerciseRoutinePlan (
    routine_ID INT PRIMARY KEY AUTO_INCREMENT,
    trainee_user_ID INT,
    trainer_user_ID INT,
    routine_name VARCHAR(255),
    description VARCHAR(255),
    calories VARCHAR(50),
    intensity VARCHAR(255),
    duration VARCHAR(255),
    equipment VARCHAR(255),
    status VARCHAR(50),
    exercises_list VARCHAR(255),
    FOREIGN KEY (trainee_user_ID) REFERENCES Trainee(user_ID),
    FOREIGN KEY (trainer_user_ID) REFERENCES Trainer(user_ID)
);


CREATE TABLE PlansExercise (
    routine_ID INT,
    exercise_ID INT,
    quantity INT,
    PRIMARY KEY (routine_ID, exercise_ID),
    FOREIGN KEY (routine_ID) REFERENCES ExerciseRoutinePlan(routine_ID),
    FOREIGN KEY (exercise_ID) REFERENCES Exercise(exercise_ID)
);

CREATE TABLE Contains (
    log_ID INT,
    exercise_ID INT,
    PRIMARY KEY (log_ID, exercise_ID),
    FOREIGN KEY (log_ID) REFERENCES ExerciseLog(log_ID),
    FOREIGN KEY (exercise_ID) REFERENCES Exercise(exercise_ID)
);


CREATE TABLE Requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    user_ID INT,
    trainer_ID INT,
    note TEXT,
    type VARCHAR(50),
    FOREIGN KEY (user_ID) REFERENCES User(user_ID),
    FOREIGN KEY (trainer_ID) REFERENCES Trainer(user_ID)
);

CREATE TABLE CoachingRequests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    trainee_user_ID INT,
    trainer_user_ID INT,
    request_date DATE,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (trainee_user_ID) REFERENCES User(user_ID),
    FOREIGN KEY (trainer_user_ID) REFERENCES User(user_ID)
);

CREATE TABLE plans_nutrition(
    user_ID INT,
    plan_ID INT,
    PRIMARY KEY (user_ID, plan_ID),
    FOREIGN KEY (user_ID) REFERENCES Trainee(user_ID),
    FOREIGN KEY (plan_ID) REFERENCES NutritionPlan(plan_ID)
);

CREATE TABLE does (
    user_ID INT,
    routine_ID INT,
    exercise_ID INT,
    start_date DATE,
    end_date DATE,
    planned_calories INT,
    CONSTRAINT check_start_before_end CHECK (start_date < end_date),
    PRIMARY KEY (user_ID, routine_ID, exercise_ID),
    FOREIGN KEY (user_ID) REFERENCES Trainee(user_ID),
    FOREIGN KEY (routine_ID) REFERENCES ExerciseRoutinePlan(routine_ID),
    FOREIGN KEY (exercise_ID) REFERENCES Exercise(exercise_ID)
);

INSERT INTO User (first_name, last_name, date_of_birth, age, gender, email, password, phone_no, isTrainer)
VALUES 
('Melih', 'Guven', '2002-04-01', 22, 'Male', 'melihhguvenn@gmail.com', 'asd123', '05056542789',1),
('Kaan', 'Soyad', '2003-07-08', 20, 'Male', 'kaan@gmail.com', 'dsa321', '05050055513',1),
('Yagiz', 'Basarn', '2002-01-01', 22, 'Male', 'yagiz@gmail.com', 'yagiz', '05556557426',0),
('Bartu', 'Soyad', '2000-01-04', 24, 'Male', 'bartu@gmail.com', 'bartu123', '05357861234',0),
('ADMIN', '1',    '2024-05-05',   1, 'Female', 'admin@ft.com',    '123',       '1',       2);

INSERT INTO Admin (user_ID)
VALUES 
(5);

INSERT INTO Trainer (user_ID, specialization, certification, height, weight)
VALUES 
(1, 'Strength Training', 'Certified Strength Coach', 180, 80),
(2, 'Corssfit Training', 'Certification of Professional Crossfit Coach', 190, 83);

INSERT INTO Trainee (user_ID, height, weight, fat_percentage)
VALUES 
(3, 1.65, 90, 24.5),
(4, 1.90, 50, 14.2);

INSERT INTO NutritionLog (meal_items, calories_consumed)
VALUES 
('Chicken salad', 350),
('Meat Doner', 780);

INSERT INTO ExerciseLog (duration, exercise_list, notes)
VALUES 
(90.0, 'Running, Squats', 'Rested for 2 minutes'),
(15, 'Triceps Pull Down', 'Superset');





INSERT INTO NutritionPlan (trainee_user_ID, trainer_user_ID, plan_name, description, meal_items)
VALUES 
(3, 1, 'Footballer Plan', 'Sportive plan for football players', ''),
(4,2,'Basketballer Plan', 'Sportive plan for basketball players', '');

INSERT INTO PremiumAccount (user_ID, premiumAcc_ID, start_date, end_date, payment_method)
VALUES 
(3, 101, '2023-01-01', '2024-01-01', 'Credit Card'),
(4, 102, '2023-02-02', '2024-02-02', 'Credit Card');

INSERT INTO Messages (sender_id, receiver_id, message)
VALUES 
(1, 3, 'Can you update my last program, it is hard for me'),
(3,1, 'Please text me the part you are struggling'),
(4,2,'This meet we could not talk. Tell me how was your exercise');

INSERT INTO ate (user_id, log_id, calories_taken)
VALUES 
(2, 1, 350),
(1,2,840);

INSERT INTO done (user_ID, log_ID, calories_burned)
VALUES 
(2, 1, 400),
(1,2,700);

INSERT INTO trains (trainee_user_ID, trainer_user_ID, start_date, end_date, recommendations)
VALUES 
(3, 1, '2023-01-01', '2023-06-01', 'Your tend to lose weight easy'),
(4,2,'2023-02-02', '2023-10-02','Keep doing good!');

INSERT INTO planned_for (user_ID, plan_ID, start_date, end_date)
VALUES 
(3, 1, '2023-01-01', '2023-03-01'),
(4,2,'2023-02-02', '2023-03-02');

INSERT INTO Exercise (exercise_ID, exercise_name, description, target_muscles, difficulty_level, set_size, repeat_size)
VALUES 
(1, 'Push-up', 'Standard push-ups', 'Chest, Shoulders, Triceps', 5, 3, 15),
(2, 'Pull-up', 'Standard', 'Shoulders, Chest, Back', 8, 3, 12),
(3, 'Squats', 'Standard squats', 'Quadriceps, Hamstrings, Glutes', 6, 3, 12),
(4, 'Deadlifts', 'Conventional deadlifts', 'Hamstrings, Glutes, Lower back', 9, 3, 10),
(5, 'Bench Press', 'Standard bench press', 'Chest, Shoulders, Triceps', 7, 3, 10),
(6, 'Dumbbell Rows', 'Standard dumbbell rows', 'Back, Biceps', 6, 3, 12),
(7, 'Plank', 'Standard plank exercise', 'Core', 4, 3, 60),
(8, 'Lunges', 'Standard lunges', 'Quadriceps, Hamstrings, Glutes', 7, 3, 12),
(9, 'Dumbbell Shoulder Press', 'Standard dumbbell shoulder press', 'Shoulders', 7, 3, 10);

INSERT INTO Requests (user_ID, note, type)
VALUES 
(2, 'Need a custom plan', 'Nutrition');

INSERT INTO plans_nutrition (user_ID, plan_ID)
VALUES 
(3, 1),
(4, 2);


INSERT INTO Contains (log_ID, exercise_ID)
VALUES 
(1, 1),
(2, 2);


INSERT INTO ExerciseRoutinePlan (routine_name, trainee_user_ID, trainer_user_ID, description, calories, intensity, duration, equipment, status, exercises_list)
VALUES 
('Weight Loss Routine', 3, 1, 'Routine for weight loss', '500', 'Intermediate', '60 mins', 'Dumbbells and resistance bands', 'Active', 'Squats, Lunges, Push-ups'),
('Muscle Building Routine', 3, 1, 'Routine for muscle building', '800', 'Advanced', '90 mins', 'Dumbbells and bars', 'Active', 'Barbell curl, Triceps Pushdown');

INSERT INTO MealItem (name, description, calories) VALUES
('Grilled Chicken Breast', 'A succulent piece of grilled chicken breast.', 165),
('Quinoa Salad', 'A healthy salad made with quinoa, vegetables, and a light vinaigrette.', 220),
('Oatmeal with Fruits', 'A bowl of oatmeal topped with fresh fruits.', 150),
('Protein Shake', 'A nutritious shake with protein powder, milk, and a banana.', 250),
('Vegetable Stir-fry', 'A mix of fresh vegetables stir-fried with a light soy sauce.', 180),
('Greek Yogurt with Honey', 'A serving of Greek yogurt drizzled with honey.', 120),
('Salmon Fillet', 'A perfectly cooked salmon fillet.', 200),
('Mixed Nuts', 'A small portion of assorted nuts.', 175),
('Smoothie Bowl', 'A bowl of blended fruits topped with granola and nuts.', 300),
('Egg White Omelette', 'An omelette made with egg whites and vegetables.', 100);

INSERT INTO PlanIncludesMealItem (plan_ID, meal_item_ID, quantity) VALUES
(1,3,1),
(1,4,1),
(1,1,1),
(2,6,1),
(2,7,1);

INSERT INTO PlansExercise (routine_ID, exercise_ID, quantity)
VALUES 
(1, 1, 1),
(1, 2, 1),
(2, 1, 1),
(2, 2, 1);

INSERT INTO does (user_ID, routine_ID, exercise_ID, start_date, end_date, planned_calories)
VALUES 
(3, 1, 1, '2023-01-01', '2023-06-01', 500),
(4, 2, 2, '2023-02-02', '2023-10-02', 700);

DELIMITER //

CREATE TRIGGER before_user_insert BEFORE INSERT ON User FOR EACH ROW
BEGIN
    SET NEW.age = YEAR(CURDATE()) - YEAR(NEW.date_of_birth);
END;
//

CREATE TRIGGER after_user_delete AFTER DELETE ON User FOR EACH ROW
BEGIN
    IF EXISTS (SELECT * FROM Trainer WHERE user_ID = OLD.user_ID) THEN
        DELETE FROM trains WHERE trainer_user_ID = OLD.user_ID;
        DELETE FROM NutritionPlan WHERE trainer_user_ID = OLD.user_ID;
        DELETE FROM ExerciseRoutinePlan WHERE trainer_user_ID = OLD.user_ID;
        DELETE FROM Trainer WHERE user_ID = OLD.user_ID;
    END IF;

    IF EXISTS (SELECT * FROM Trainee WHERE user_ID = OLD.user_ID) THEN
        DELETE FROM NutritionPlan WHERE trainee_user_ID = OLD.user_ID;
        DELETE FROM ExerciseRoutinePlan WHERE trainee_user_ID = OLD.user_ID;
        DELETE FROM trains WHERE trainee_user_ID = OLD.user_ID;
        DELETE FROM Trainee WHERE user_ID = OLD.user_ID;
    END IF;
END;
//

DELIMITER ;

CREATE VIEW TrainerTraineeInfo AS
SELECT
    t.user_ID AS trainer_ID,
    u1.first_name AS trainer_first_name,
    u1.last_name AS trainer_last_name,
    tn.user_ID AS trainee_ID,
    t.specialization AS trainer_specialization,
    u2.first_name AS trainee_first_name,
    u2.last_name AS trainee_last_name,
    tr.recommendations
FROM
    User u1
JOIN Trainer t ON u1.user_ID = t.user_ID
JOIN trains tr ON t.user_ID = tr.trainer_user_ID
JOIN Trainee tn ON tr.trainee_user_ID = tn.user_ID
JOIN User u2 ON tn.user_ID = u2.user_ID;

CREATE VIEW UserGoalsDetails AS
SELECT
    u.user_ID,
    u.first_name,
    u.last_name,
    fg.goal_description,
    fg.created_at
FROM
    User u
JOIN FitnessGoals fg ON u.user_ID = fg.user_ID;
