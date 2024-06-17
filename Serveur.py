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

        self.client_sockets = {}  # Dictionary to track client connections

        self.create_tables()  # Create SQLite database tables
        self.reset_connected_users()  # Reset connected users

    def create_tables(self):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS connected_users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE NOT NULL
                              )''')
            conn.commit()

    def reset_connected_users(self):
        # Clear all connected users on server start
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM connected_users')
            conn.commit()

    def start(self):
        # Start thread to print connected users every 20 seconds
        Thread(target=self.print_connected_users_periodically).start()

        # Start thread to send pings to clients every 10 seconds
        Thread(target=self.send_ping_to_clients).start()

        while True:
            client_socket, client_addr = self.server_socket.accept()
            secure_socket = self.context.wrap_socket(client_socket, server_side=True)
            self.client_sockets[client_addr] = secure_socket
            print(f'Connection established with {client_addr}')

            # Start a thread to handle the client
            Thread(target=self.handle_client, args=(secure_socket, client_addr)).start()

    def handle_client(self, secure_socket, client_addr):
        try:
            # Receive username from the client
            username = secure_socket.recv(1024).decode()
            if username:
                # Add user to the connected users database
                self.add_connected_user(username)

                # Send the list of connected users to all clients
                self.send_connected_users()

                # Wait for further messages or commands from the client
                while True:
                    data = secure_socket.recv(1024)
                    if not data:
                        break
                    message = data.decode()
                    if message.startswith('PING:'):
                        # Respond to ping
                        print(f'Message received from {username} : PING')
                        secure_socket.sendall(b'PONG:')
                    elif message.startswith('MSG:'):
                        print(f'Received from {username}: {message[4:]}')
                        # Echo back to client (or handle the message accordingly)
                        secure_socket.sendall(data)
        except Exception as e:
            print(f'Error with client {client_addr}: {e}')

        # Client disconnected
        self.remove_client(client_addr)
        self.send_connected_users()  # Update the list after disconnection
        print(f'Client {client_addr} disconnected')

    def add_connected_user(self, username):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO connected_users (username) VALUES (?)', (username,))
            conn.commit()

    def remove_client(self, client_addr):
        if client_addr in self.client_sockets:
            del self.client_sockets[client_addr]

        # Remove the disconnected user from the database
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM connected_users WHERE username = ?', (client_addr[0],))
            conn.commit()

    def get_connected_users(self):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username FROM connected_users')
            return [row[0] for row in cursor.fetchall()]

    def send_connected_users(self):
        connected_users_str = ','.join(self.get_connected_users())
        for client_addr, secure_socket in self.client_sockets.items():
            try:
                secure_socket.sendall(f'CONNECTED_USERS:{connected_users_str}'.encode())
            except Exception as e:
                print(f'Error sending connected users to {client_addr}: {e}')

    def print_connected_users_periodically(self):
        while True:
            connected_users = self.get_connected_users()
            print(f"Connected Users: {', '.join(connected_users)}")
            self.send_connected_users()  # Send the list of connected users
            time.sleep(20)

    def send_ping_to_clients(self):
        while True:
            # List of clients to remove
            clients_to_remove = []

            for client_addr, secure_socket in self.client_sockets.items():
                try:
                    secure_socket.sendall(b'PING:')
                    response = secure_socket.recv(1024)
                    if response.decode() != 'PONG:':
                        print(f'Client {client_addr} did not respond correctly to ping')
                        clients_to_remove.append(client_addr)
                except Exception as e:
                    print(f'Error sending ping to {client_addr}: {e}')
                    clients_to_remove.append(client_addr)

            # Remove clients that did not respond correctly to the ping
            for client_addr in clients_to_remove:
                self.remove_client(client_addr)

            time.sleep(10)

if __name__ == "__main__":
    server = ChatServer()
    server.start()
