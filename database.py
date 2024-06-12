import sqlite3
from hashlib import sha256

DATABASE_NAME = 'chat_app.db'

def create_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL
                          )''')
        conn.commit()

def add_user(username, password):
    with create_connection() as conn:
        cursor = conn.cursor()
        hashed_password = sha256(password.encode()).hexdigest()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()

def authenticate_user(username, password):
    with create_connection() as conn:
        cursor = conn.cursor()
        hashed_password = sha256(password.encode()).hexdigest()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        return cursor.fetchone() is not None

def get_users():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users')
        return cursor.fetchall()

def print_users():
    users = get_users()
    print("Registered Users:")
    for user in users:
        print(f"Username: {user[0]}")
# Create the tables initially

def delete_user(username):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        
create_tables()
