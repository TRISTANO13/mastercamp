import socket
import ssl
import sqlite3
import bcrypt
from datetime import datetime

# Configuration du serveur SSL/TLS
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Connexion à la base de données
conn = sqlite3.connect('chat_logs.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs (timestamp TEXT, user TEXT, message TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')

# Fonction de journalisation
def log_event(user, message):
    c.execute("INSERT INTO logs (timestamp, user, message) VALUES (?,?,?)",
              (datetime.now(), user, message))
    conn.commit()

# Fonction d'authentification des utilisateurs
def authenticate(username, password):
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()
    if stored_password and bcrypt.checkpw(password.encode(), stored_password[0]):
        return True
    return False

# Fonction de traitement des clients
def handle_client(connstream):
    try:
        data = connstream.recv(1024).decode()
        username, password = data.split(':')
        if authenticate(username, password):
            connstream.send("AUTH_SUCCESS".encode())
            while True:
                message = connstream.recv(1024).decode()
                if not message:
                    break
                log_event(username, message)
                connstream.send(f"Received: {message}".encode())
        else:
            connstream.send("AUTH_FAIL".encode())
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()

# Configuration du socket du serveur
bindsocket = socket.socket()
bindsocket.bind(('localhost', 10023))
bindsocket.listen(5)

print("Server started and listening...")

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    handle_client(connstream)
