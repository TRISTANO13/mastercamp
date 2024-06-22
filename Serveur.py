import socket
import ssl
from threading import Thread
import sqlite3
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 8888

class ChatServer:
    def __init__(self):
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((SERVER_HOST, SERVER_PORT))
        self.server_socket.listen(5)
        print(f'Server is listening on {SERVER_HOST}:{SERVER_PORT}')

        self.client_sockets = {}
        self.usernames = {}
        self.chatrooms = {}

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
        Thread(target=self.print_connected_users_periodically).start()
        Thread(target=self.send_ping_to_clients).start()

        while True:
            client_socket, client_addr = self.server_socket.accept()
            secure_socket = self.context.wrap_socket(client_socket, server_side=True)
            self.client_sockets[client_addr] = secure_socket
            print(f'Connection established with {client_addr}')

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
                    if data.startswith(b'/join'):
                        room_name = data.split()[1].decode()
                        if self.join_private_room(room_name, username):
                            secure_socket.sendall(f"Joined room {room_name}".encode())
                        else:
                            secure_socket.sendall(f"Failed to join room {room_name}".encode())
                    elif data.startswith(b'/leave'):
                        room_name = data.split()[1].decode()
                        self.leave_private_room(room_name, username)
                        secure_socket.sendall(f"Left room {room_name}".encode())
                    elif data.startswith(b'/'):
                        self.handle_private_message(username, data)
                    else:
                        self.broadcast_to_private_room(username, data)
        except Exception as e:
            print(f'Error with client {client_addr}: {e}')

        self.remove_client(client_addr)
        self.send_connected_users()
        print(f'Client {client_addr} disconnected')

    def add_connected_user(self, username):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO connected_users (username) VALUES (?)', (username,))
            conn.commit()

    def send_connected_users(self):
        connected_users = self.get_connected_users()
        for secure_socket in self.client_sockets.values():
            secure_socket.sendall(f'Connected users: {connected_users}'.encode())

    def get_connected_users(self):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username FROM connected_users')
            users = [row[0] for row in cursor.fetchall()]
        return users

    def join_private_room(self, room_name, username):
        if room_name not in self.chatrooms:
            self.chatrooms[room_name] = set()
        self.chatrooms[room_name].add(username)
        return True

    def leave_private_room(self, room_name, username):
        if room_name in self.chatrooms:
            self.chatrooms[room_name].remove(username)
            if not self.chatrooms[room_name]:
                del self.chatrooms[room_name]

    def handle_private_message(self, username, data):
        parts = data.split()
        recipient = parts[0][1:].decode()
        message = b' '.join(parts[1:]).decode()

        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)',
                           (username, recipient, message))
            conn.commit()

        for secure_socket in self.client_sockets.values():
            secure_socket.sendall(f"{username} to {recipient}: {message}".encode())

    def broadcast_to_private_room(self, username, data):
        message = data.decode()
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)',
                           (username, 'all', message))
            conn.commit()

        for secure_socket in self.client_sockets.values():
            secure_socket.sendall(f"{username}: {message}".encode())

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

    def send_ping_to_clients(self):
        while True:
            time.sleep(10)
            for secure_socket in self.client_sockets.values():
                try:
                    secure_socket.sendall(b'/ping')
                except Exception as e:
                    print(f"Error sending ping: {e}")

    def print_connected_users_periodically(self):
        while True:
            connected_users = self.get_connected_users()
            print(f"Connected users: {connected_users}")
            time.sleep(10)

if __name__ == '__main__':
    server = ChatServer()
    server.start()
