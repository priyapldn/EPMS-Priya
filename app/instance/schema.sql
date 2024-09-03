-- Create Employee Performance Management database, tables, keys and insert records
DROP DATABASE IF EXISTS epmstore;
CREATE DATABASE IF NOT EXISTS epmstore;
USE epmstore;

-- Create the employee table
CREATE TABLE employee (
    id INT PRIMARY KEY AUTO_INCREMENT,                  -- Unique identifier for each employee (auto-incremented)
    employee_id VARCHAR(10) UNIQUE NOT NULL , -- Employee ID, must be unique
    name VARCHAR(100) NOT NULL,             -- Employee's full name
    email VARCHAR(100) UNIQUE NOT NULL,     -- Employee's email, must be unique
    username VARCHAR(50) UNIQUE NOT NULL,   -- Username for login, must be unique
    password VARCHAR(255) NOT NULL,         -- Password (with validations for secure storage, see below)
    CHECK (LENGTH(password) >= 8),      -- Password must be at least 8 characters long
    CHECK (password LIKE '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$') -- Password must contain uppercase, lowercase, digit, and special character
);

-- Create the review table
CREATE TABLE review (
    id INT PRIMARY KEY AUTO_INCREMENT,                  -- Unique identifier for each review (auto-incremented)
    employee_id VARCHAR(10) NOT NULL,       -- Foreign key linking to the employee table    
    review_date DATE NOT NULL,              -- Date of the review
    reviewer_id INT NOT NULL,               -- Reviewer ID (could be another employee or an external reviewer)
    overall_performance_rating VARCHAR(50) CHECK (overall_performance_rating IN ('Excellent', 'Good', 'Satisfactory', 'Needs Improvement', 'Unsatisfactory')),                     -- Performance rating
    goals TEXT,                             -- Goals for the employee
    reviewer_comments TEXT,                 -- Comments from the reviewer
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)  -- Foreign key constraint
);