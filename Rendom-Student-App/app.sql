CREATE DATABASE random_wheel_db;

USE random_wheel_db;

CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
CREATE DATABASE groupdb;

USE groupdb;

CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE groups (
  id INT AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(50),
  members TEXT
);
CREATE DATABASE IF NOT EXISTS random_spinner_db;

USE random_spinner_db;

CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('text', 'image') NOT NULL,
    data TEXT
);
