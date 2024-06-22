# database.py

import sqlite3
import hashlib

DATABASE_NAME = 'chat_app.db'

def create_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Création de la table 'users' si elle n'existe pas
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                    )''')

    # Création de la table 'connected_users' si elle n'existe pas
    cursor.execute('''CREATE TABLE IF NOT EXISTS connected_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE
                    )''')

    # Création de la table 'messages' si elle n'existe pas
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

    conn.commit()
    conn.close()

def add_user(username, password):
    with create_connection() as conn:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"User {username} already exists.")
            return False

def check_credentials(username, password):
    with create_connection() as conn:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        return cursor.fetchone() is not None

def get_users():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users')
        return cursor.fetchall()

def add_message(sender, recipient, message):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)', (sender, recipient, message))
        conn.commit()

def get_messages(sender, recipient):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT sender, message FROM messages WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)',
                       (sender, recipient, recipient, sender))
        return cursor.fetchall()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_connected_user(username):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO connected_users (username) VALUES (?)', (username,))
        conn.commit()

def get_connected_users():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM connected_users')
        return [row[0] for row in cursor.fetchall()]

def remove_connected_user(username):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM connected_users WHERE username = ?', (username,))
        conn.commit()

def reset_connected_users():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM connected_users')
        conn.commit()

# Ajout d'une fonction pour vérifier l'existence d'un utilisateur
def check_user_exists(username):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone() is not None
