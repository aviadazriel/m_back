# neon
users_tbl = """CREATE TABLE users (
    id SERIAL PRIMARY KEY,                 -- Unique identifier for each user
    username VARCHAR(50) NOT NULL UNIQUE, -- Username, must be unique
    email VARCHAR(100) NOT NULL UNIQUE,   -- Email, must be unique
    phone VARCHAR(10) NOT NULL UNIQUE,   -- phone, must be unique
    password_hash VARCHAR(255) NOT NULL,  -- Hashed password for security
    first_name VARCHAR(50),               -- Optional first name
    last_name VARCHAR(50),                -- Optional last name
    profile_image_url TEXT,               -- URL to the user's profile image
    is_active BOOLEAN DEFAULT TRUE,       -- Indicates if the account is active
    is_admin BOOLEAN DEFAULT FALSE,       -- Indicates if the user is an admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for last update
);"""

insert_users_query = """INSERT INTO users (username, email,phone, password_hash, first_name, last_name, profile_image_url, is_active, is_admin)
VALUES
    ('johndoe', 'john.doe@example.com','0522257283', 'hashed_password_1', 'John', 'Doe', 'https://example.com/johndoe.jpg', TRUE, FALSE),
    ('janedoe', 'jane.doe@example.com','0522257284', 'hashed_password_2', 'Jane', 'Doe', 'https://example.com/janedoe.jpg', TRUE, TRUE);
"""
