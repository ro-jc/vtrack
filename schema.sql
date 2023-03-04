DROP TABLE IF EXISTS login;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS user;


CREATE TABLE login (
userid INTEGER UNSIGNED UNIQUE PRIMARY KEY AUTO_INCREMENT,
email varchar(80),
password TEXT NOT NULL,
);


CREATE TABLE user (
userid INTEGER UNSIGNED UNIQUE PRIMARY KEY,
name varchar(50),
female BOOLEAN,
hostel_block char(1),
phone_number char(10) DEFAULT NULL,
FOREIGN KEY (userid) REFERENCES login (userid),
);


CREATE TABLE trips (
id INTEGER UNSIGNED UNIQUE PRIMARY KEY AUTO_INCREMENT,
trip_time TIMESTAMP,
user_1 INTEGER UNSIGNED UNIQUE NOT NULL,
user_2 INTEGER UNSIGNED UNIQUE DEFAULT NULL,
user_3 INTEGER UNSIGNED UNIQUE DEFAULT NULL,
user_4 INTEGER UNSIGNED UNIQUE DEFAULT NULL,
user_5 INTEGER UNSIGNED UNIQUE DEFAULT NULL,
user_6 INTEGER UNSIGNED UNIQUE DEFAULT NULL,
pickup_point varchar(100) NOT NULL,
drop_point varchar(100) NOT NULL,
resolved BOOLEAN DEFAULT FALSE,
vehicle TINYINT,
FOREIGN KEY (user_1) REFERENCES user (userid),
FOREIGN KEY (user_2) REFERENCES user (userid),
FOREIGN KEY (user_3) REFERENCES user (userid),
FOREIGN KEY (user_4) REFERENCES user (userid)
FOREIGN KEY (user_5) REFERENCES user (userid),
FOREIGN KEY (user_6) REFERENCES user (userid)
);