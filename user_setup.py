import sqlite3
import bcrypt

conn = sqlite3.connect('chat_logs.db')
c = conn.cursor()

# Ajouter un nouvel utilisateur
def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, hashed))
    conn.commit()

# Utilisateur à ajouter
username = input("Enter new username: ")
password = input("Enter new password: ")
add_user(username, password)
print(f"User {username} added successfully")
