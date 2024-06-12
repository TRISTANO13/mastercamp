import sqlite3
import bcrypt

# Connexion à la base de données
conn = sqlite3.connect('chat_logs.db')
c = conn.cursor()

# Créer la table users si elle n'existe pas
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

# Fonction pour ajouter un nouvel utilisateur
def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, hashed))
    conn.commit()

# Ajouter un utilisateur
username = input("Enter new username: ")
password = input("Enter new password: ")
add_user(username, password)
print(f"User {username} added successfully")
