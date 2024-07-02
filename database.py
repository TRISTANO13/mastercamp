# database.py
import sqlite3
import bcrypt 

def initialize_db():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de l'initialisation de la base de données: {e}")
    finally:
        conn.close()

def register_user_db(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password.decode('utf-8')))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as e:
        print(f"Erreur lors de l'enregistrement de l'utilisateur: {e}")
        return False
    finally:
        conn.close()

def verify_user_db(username, password):
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username=?", (username,))
            result = c.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                return True
    except sqlite3.Error as e:
        print(f"Erreur de base de données: {e}")
    except Exception as e:
        print(f"Erreur: {e}")
    return False

def verify_user_available(username):
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username=?", (username,))
            result = c.fetchone()
            if result:
                return True
            return False
    except sqlite3.Error as e:
        print(f"Erreur de base de données: {e}")
        return False

initialize_db()
