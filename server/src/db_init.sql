-- CREATE DATABASE IF NOT EXISTS Networkly;
-- GRANT ALL ON Networkly.* TO 'user'@'%';

-- USE Networkly;

-- DROP TABLE IF EXISTS USERS;

-- CREATE TABLE USERS(
--     id BIGINT(20) AUTO_INCREMENT,
--     username VARCHAR(25) NOT NULL,
--     email VARCHAR(50) NOT NULL,
--     firstname VARCHAR(50) NOT NULL,
--     lastname VARCHAR(100),
--     profile_description VARCHAR(250) ,
--     PRIMARY KEY (id)
-- );

-- INSERT INTO USERS(username, email, firstname, lastname, profile_description)
-- VALUES  ("david19", "david19@gmail.com", "david", "fernandez", "data scientist"),
--         ("isabel20", "isabel20@gmail.com", "isabel", "gomez", "product manager"),
--         ("sandra21", "sandra21@gmail.com", "sandra", "hernandez", "biologist");


-- DROP TABLE IF EXISTS DATASETS;

-- CREATE TABLE DATASETS(
--     dataset_id BIGINT(20) AUTO_INCREMENT,
--     dataset_hash CHAR(32) NOT NULL,
--     dataset_name VARCHAR(50), 
--     dataset_json JSON NOT NULL,
--     PRIMARY KEY (dataset_hash),
--     ON DELETE CASCADE
-- );

-- -- INSERT INTO DATASETS(dataset_hash, dataset_name, dataset_json)
-- -- VALUES  ("david19", "david19@gmail.com", "david", "fernandez", "data scientist"),
-- --         ("isabel20", "isabel20@gmail.com", "isabel", "gomez", "product manager"),
-- --         ("sandra21", "sandra21@gmail.com", "sandra", "hernandez", "biologist");


-- DROP TABLE IF EXISTS EXPERIMENTS;

-- CREATE TABLE EXPERIMENTS(
--     experiment_id BIGINT(20) AUTO_INCREMENT,
--     user_id BIGINT(20) NOT NULL,
--     creation_date DATETIME NOT NULL,
--     experiment_name VARCHAR(50), 
--     network_json JSON NOT NULL,
--     category VARCHAR(50) NOT NULL,
--     description VARCHAR(300),
--     metrics JSON,
--     dataset_name VARCHAR(50),
--     dataset_hash CHAR(32) NOT NULL, 
--     thumbnail BLOB,
--     PRIMARY KEY (experiment_id),
--     FOREIGN KEY (user_id) REFERENCES USERS(id),
--     FOREIGN KEY (dataset_hash) REFERENCES DATASETS(dataset_hash),
--     ON DELETE CASCADE
-- );