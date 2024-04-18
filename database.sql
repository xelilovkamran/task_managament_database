CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    password VARCHAR(255) NOT NULL UNIQUE
)


CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_id INT,
    task_name VARCHAR(255),
    description VARCHAR(255),
    due_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
)


CREATE TABLE IF NOT EXISTS categories (
	id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) NOT NULL UNIQUE
)

INSERT INTO categories (category) VALUES ('mandatory'), ('optional')