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

        self.client_sockets = {}  # Dictionnaire pour suivre les connexions des clients

        self.create_tables()  # Création des tables de la base de données SQLite
        self.reset_connected_users()  # Réinitialisation des utilisateurs connectés
    
    def create_private_room(self, room_name):
        if room_name not in self.chatrooms:
            self.chatrooms[room_name] = set()

    def join_private_room(self, room_name, username):
        if room_name in self.chatrooms:
            self.chatrooms[room_name].add(username)
            return True
        return False

    def leave_private_room(self, room_name, username):
        if room_name in self.chatrooms and username in self.chatrooms[room_name]:
            self.chatrooms[room_name].remove(username)


    def create_tables(self):
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS connected_users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE NOT NULL
                              )''')
            conn.commit()

    def reset_connected_users(self):
        # Effacer tous les utilisateurs connectés au démarrage du serveur
        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM connected_users')
            conn.commit()

    def start(self):
        # Démarrer le thread pour afficher les utilisateurs connectés toutes les 20 secondes
        Thread(target=self.print_connected_users_periodically).start()

        # Démarrer le thread pour envoyer des pings aux clients toutes les 10 secondes
        Thread(target=self.send_ping_to_clients).start()

        while True:
            client_socket, client_addr = self.server_socket.accept()
            secure_socket = self.context.wrap_socket(client_socket, server_side=True)
            self.client_sockets[client_addr] = secure_socket
            print(f'Connection established with {client_addr}')

            # Démarrer un thread pour gérer le client
            Thread(target=self.handle_client, args=(secure_socket, client_addr)).start()

    def handle_client(self, secure_socket, client_addr):
        try:
            # Recevoir le nom d'utilisateur du client
            username = secure_socket.recv(1024).decode()
            if username:
                # Ajouter l'utilisateur à la base de données des utilisateurs connectés
                self.add_connected_user(username)

                # Envoyer la liste des utilisateurs connectés à tous les clients
                self.send_connected_users()

                # Attendre les autres messages ou commandes du client si nécessaire
                while True:
                    data = secure_socket.recv(1024)
                    if not data:
                        break
                    print(f'Received from {username}: {data.decode()}')

                    # Exemple: Echo back to client
                    secure_socket.sendall(data)
        except Exception as e:
            print(f'Error with client {client_addr}: {e}')

        # Client disconnected
        self.remove_client(client_addr)
        self.send_connected_users()  # Mise à jour de la liste après déconnexion
        print(f'Client {client_addr} disconnected')

    def handle_client(self, secure_socket, client_addr):
        try:
            username = secure_socket.recv(1024).decode()
            if username:
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
                        # Commande spéciale pour les messages privés
                        self.handle_private_message(username, data)
                    else:
                        # Messages normaux dans les rooms privées
                        self.broadcast_to_private_room(username, data)
        except Exception as e:
            print(f'Error with client {client_addr}: {e}')

    def broadcast_to_private_room(self, sender, data):
        room_name, message = data.split(b':', 1)
        if room_name in self.chatrooms:
            for user in self.chatrooms[room_name]:
                if user in self.client_sockets and user != sender:
                    self.client_sockets[user].sendall(f"{sender}: {message.decode()}".encode())

        with sqlite3.connect('chat_app.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO connected_users (username) VALUES (?)', (username,))
            conn.commit()

    def remove_client(self, client_addr):
        if client_addr in self.client_sockets:
            del self.client_sockets[client_addr]

        # Supprimer l'utilisateur déconnecté de la base de données
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
                secure_socket.sendall(connected_users_str.encode())
            except Exception as e:
                print(f'Error sending connected users to {client_addr}: {e}')

    def print_connected_users_periodically(self):
        while True:
            connected_users = self.get_connected_users()
            print(f"Connected Users: {', '.join(connected_users)}")
            self.send_connected_users()  # Envoyer la liste des utilisateurs connectés
            time.sleep(20)

    def send_ping_to_clients(self):
        while True:
            # Liste des clients à supprimer
            clients_to_remove = []

            for client_addr, secure_socket in self.client_sockets.items():
                try:
                    secure_socket.sendall(b'ping')
                    response = secure_socket.recv(1024)
                    if response.decode() != 'pong':
                        print(f'Client {client_addr} did not respond correctly to ping')
                        clients_to_remove.append(client_addr)
                except Exception as e:
                    print(f'Error sending ping to {client_addr}: {e}')
                    clients_to_remove.append(client_addr)

            # Supprimer les clients qui n'ont pas répondu au ping correctement
            for client_addr in clients_to_remove:
                self.remove_client(client_addr)

            time.sleep(10)

if __name__ == "__main__":
    server = ChatServer()
    server.start()
