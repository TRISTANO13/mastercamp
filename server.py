import socket
import ssl
from threading import Thread
import sqlite3
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 8888

class ChatServer:
    def __init__(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2  # Assurez-vous que la version minimale est TLS 1.2
        self.context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((SERVER_HOST, SERVER_PORT))
        self.server_socket.listen(5)
        print(f'Server is listening on {SERVER_HOST}:{SERVER_PORT}')

        self.client_sockets = {}
        self.usernames = {}

        self.create_tables()
        self.reset_connected_users()

    def create_tables(self):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS connected_users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE NOT NULL
                              )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                sender TEXT NOT NULL,
                                recipient TEXT NOT NULL,
                                message TEXT NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                              )''')
            conn.commit()

    def reset_connected_users(self):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM connected_users')
            conn.commit()

    def start(self):
        while True:
            client_socket, client_addr = self.server_socket.accept()
            secure_socket = self.context.wrap_socket(client_socket, server_side=True)
            self.client_sockets[client_addr] = secure_socket
            Thread(target=self.handle_client, args=(secure_socket, client_addr)).start()

    def handle_client(self, secure_socket, client_addr):
        try:
            username = secure_socket.recv(1024).decode()
            if username:
                self.usernames[client_addr] = username
                self.add_connected_user(username)
                self.send_connected_users()

                while True:
                    data = secure_socket.recv(1024)
                    if not data:
                        break
                    self.handle_message(data.decode(), client_addr)
        except Exception as e:
            print(f"Error handling client {client_addr}: {e}")

        self.remove_client(client_addr)
        self.send_connected_users()

    def handle_message(self, message, client_addr):
        if message.startswith('/get_users'):
            print(f"Received /get_users from {self.usernames[client_addr]}")
            self.send_connected_users_to_client(client_addr)
        else:
            parts = message.split(':', 1)
            if len(parts) == 2:
                sender = parts[0].strip()
                content = parts[1].strip()
                self.broadcast_message(f"{sender}: {content}", sender)

    def send_connected_users_to_client(self, client_addr):
        users = self.get_connected_users()
        try:
            print(f"Sending connected users to {self.usernames[client_addr]}: {users}")
            self.client_sockets[client_addr].sendall(f"{','.join(users)}".encode())
        except Exception as e:
            print(f"Error sending users to client {client_addr}: {e}")

    def broadcast_message(self, message, sender):
        for addr, socket in self.client_sockets.items():
            if self.usernames.get(addr) != sender:
                try:
                    socket.sendall(message.encode())
                except Exception as e:
                    print(f"Error sending message to {addr}: {e}")

    def add_connected_user(self, username):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO connected_users (username) VALUES (?)', (username,))
            conn.commit()

    def send_connected_users(self):
        users = self.get_connected_users()
        for addr, socket in self.client_sockets.items():
            try:
                socket.sendall(f"/users:{','.join(users)}".encode())
            except Exception as e:
                print(f"Error sending connected users: {e}")

    def get_connected_users(self):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username FROM connected_users')
            users = [row[0] for row in cursor.fetchall()]
        return users

    def remove_client(self, client_addr):
        username = self.usernames.pop(client_addr, None)
        if username:
            self.remove_connected_user(username)
        self.client_sockets.pop(client_addr, None)

    def remove_connected_user(self, username):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM connected_users WHERE username = ?', (username,))
            conn.commit()

if __name__ == '__main__':
    server = ChatServer()
    server.start()
