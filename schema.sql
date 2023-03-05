DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS user;


CREATE TABLE user (
userid INTEGER UNSIGNED UNIQUE PRIMARY KEY AUTO_INCREMENT,
email varchar(80) NOT NULL UNIQUE,
`password` TEXT NOT NULL,
`name` varchar(50) NOT NULL,
female BOOLEAN NOT NULL,
phone_number char(10) UNIQUE DEFAULT NULL
);


CREATE TABLE trips (
id INTEGER UNSIGNED UNIQUE PRIMARY KEY AUTO_INCREMENT,
trip_date DATE,
trip_time TIME,
pickup_point varchar(100) NOT NULL,
drop_point varchar(100) NOT NULL,
vehicle TINYINT,
num_people TINYINT,
gender_filter BOOLEAN,
user_1 INTEGER UNSIGNED NOT NULL,
user_2 INTEGER UNSIGNED DEFAULT NULL,
user_3 INTEGER UNSIGNED DEFAULT NULL,
user_4 INTEGER UNSIGNED DEFAULT NULL,
user_5 INTEGER UNSIGNED DEFAULT NULL,
user_6 INTEGER UNSIGNED DEFAULT NULL,
user_7 INTEGER UNSIGNED DEFAULT NULL,
user_8 INTEGER UNSIGNED DEFAULT NULL,
resolved BOOLEAN DEFAULT FALSE,
FOREIGN KEY (user_1) REFERENCES user (userid),
FOREIGN KEY (user_2) REFERENCES user (userid),
FOREIGN KEY (user_3) REFERENCES user (userid),
FOREIGN KEY (user_4) REFERENCES user (userid),
FOREIGN KEY (user_5) REFERENCES user (userid),
FOREIGN KEY (user_6) REFERENCES user (userid),
FOREIGN KEY (user_7) REFERENCES user (userid),
FOREIGN KEY (user_8) REFERENCES user (userid)
);


CREATE TABLE drivers (
    id INTEGER UNSIGNED UNIQUE PRIMARY KEY AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    phone_number char(10),
    vehicle_type varchar(10),
    vehicle_model varchar(30),
    registration_number varchar(10),
)