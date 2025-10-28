CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) DEFAULT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO users (username, email, full_name, hashed_password, is_active)
VALUES
('Adithya', 'eadithya123@gmail.com', 'EdupugantiAdithya', 'Adi', 1),
('Harsha', 'Harsha123@gmail.com', 'HarshaGopal', 'Harsh', 1),
('Siddharth', 'Siddharth890@gmail.com', 'SiddharthReddy', 'siddh', 1),
('Rajesh', 'Rajesh456@gmail.com', 'RajeshMenon', 'Raj', 1)
ON DUPLICATE KEY UPDATE username=username;