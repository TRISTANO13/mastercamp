import socket
import ssl
import json
import threading
from database import verify_user_db, verify_user_available, register_user_db

class SSLServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket = None
        self.server_loggedUsers = []
        self.rooms = {}

    def server_send(self, client_socket, message):
        try:
            client_socket.sendall(message.encode("UTF-8"))
            print(f"[OUT] : {message}")
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def server_send_json(self, client_socket, json_message):
        try:
            client_socket.sendall(json.dumps(json_message).encode("UTF-8"))
            print(f"[OUT-J] : {json_message}")
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def handle_client(self, client_socket, addr):
        print(f"[CONNECT] {addr}")
        secure_socket = client_socket
        try:
            while True:
                data = secure_socket.recv(1000000000)
                if not data:
                    break
                self.handle_received_data(secure_socket, data)
                print(f"[IN] {addr} : {data.decode('utf-8')}")
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            secure_socket.close()

    def server_receive(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

    def handle_login(self, client_socket, data):
        username = data["username"]
        password = data["password"]

        if username and password:
            if verify_user_db(username, password):
                accept_login_obj = {
                    "action": "accept_login",
                    "message": "Connexion réussie.",
                    "username": username
                }
                self.do_loggin_user(username, client_socket)
                self.server_send_json(client_socket, accept_login_obj)
            else:
                reject_login_obj = {
                    "action": "reject_login",
                    "message": "Utilisateur ou mot de passe incorrect."
                }
                self.server_send_json(client_socket, reject_login_obj)
        else:
            reject_login_obj = {
                "action": "reject_login",
                "message": "Utilisateur ou mot de passe manquant."
            }
            self.server_send_json(client_socket, reject_login_obj)

    def handle_register(self, client_socket, data):
        username = data["username"]
        password = data["password"]

        if username and password:
            if not verify_user_available(username, password):
                accept_register_obj = {
                    "action": "accept_register",
                    "message": "Votre compte a bien été créé.",
                    "username": username
                }
                register_user_db(username, password)
                self.server_send_json(client_socket, accept_register_obj)
            else:
                reject_register_obj = {
                    "action": "reject_register",
                    "message": "Utilisateur déjà existant."
                }
                self.server_send_json(client_socket, reject_register_obj)
        else:
            reject_register_obj = {
                "action": "reject_register",
                "message": "Utilisateur ou mot de passe manquant."
            }
            self.server_send_json(client_socket, reject_register_obj)

    def handle_room(self, client_socket, data):
        From = data["From"]
        To = data["to"]
        Name = data["name"]

        if From and To and Name:
            if Name not in self.rooms:
                self.rooms[Name] = []
            if From not in self.rooms[Name]:
                self.rooms[Name].append(From)
            if To not in self.rooms[Name]:
                self.rooms[Name].append(To)

            accept_room_obj = {
                "action": "accept_room",
                "message": "Room créée.",
                "From": From,
                "To": To,
                "Name": Name
            }
            self.server_send_json(client_socket, accept_room_obj)
        else:
            reject_room_obj = {
                "action": "reject_room",
                "message": "Informations de la salle manquantes."
            }
            self.server_send_json(client_socket, reject_room_obj)

    def handle_message(self, client_socket, data):
        From = data["From"]
        To = data["to"]
        Name = data["name"]
        Message = data["message"]

        if From and To and Name and Message:
            if Name in self.rooms and From in self.rooms[Name]:
                accept_message_obj = {
                    "action": "accept_message",
                    "message": f"{From} : {Message}",
                    "From": From,
                    "To": To,
                    "Id": Name,
                    "confirmation": "Message reçu"
                }
                for user in self.server_loggedUsers:
                    if user['username'] in self.rooms[Name]:
                        self.server_send_json(user['socket'], accept_message_obj)
            else:
                reject_message_obj = {
                    "action": "reject_message",
                    "message": "Vous n'êtes pas dans cette salle."
                }
                self.server_send_json(client_socket, reject_message_obj)
        else:
            reject_message_obj = {
                "action": "reject_message",
                "message": "Utilisateur ou message manquant."
            }
            self.server_send_json(client_socket, reject_message_obj)

    def handle_received_data(self, client_socket, data):
        decoded_data = data.decode('utf-8')
        dejsonified_data = None
        try:
            dejsonified_data = json.loads(decoded_data)
            if dejsonified_data and dejsonified_data.get('action') == "login":
                self.handle_login(client_socket, dejsonified_data)
            if dejsonified_data and dejsonified_data.get('action') == "register":
                self.handle_register(client_socket, dejsonified_data)
            if dejsonified_data and dejsonified_data.get('action') == "get_logged_users":
                loggedUsers_json = {
                    "action": "get_logged_users",
                    "value": self.get_logged_users(client_socket)
                }
                self.server_send_json(client_socket, loggedUsers_json)
            if dejsonified_data and dejsonified_data.get('action') == "deconnexion":
                username = dejsonified_data["username"]
                self.do_logout_user(username)
                DecoUser_json = {
                    "action": "close_window",
                }
                self.server_send_json(client_socket, DecoUser_json)
            if dejsonified_data and dejsonified_data.get('action') == "create_room":
                self.handle_room(client_socket, dejsonified_data)
            if dejsonified_data and dejsonified_data.get('action') == "room_message":
                self.handle_message(client_socket, dejsonified_data)
            if dejsonified_data and dejsonified_data.get('action') == "send_file":
                self.handle_file_transfer(client_socket, dejsonified_data)
        except:
            print("Réponse non JSON reçue.")

    def do_loggin_user(self, username, client_socket):
        self.server_loggedUsers.append({"username": username, "socket": client_socket})

    def get_logged_users(self, client_socket):
        loggedInUsers = []
        for users in self.server_loggedUsers:
            if 'username' in users:
                loggedInUsers.append(users['username'])
        return loggedInUsers

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print("Le serveur est en attente de connexions...")
            receive_thread = threading.Thread(target=self.server_receive, args=())
            receive_thread.start()
        except Exception as e:
            print("Erreur lors du lancement du server. : \n", e)

    def do_logout_user(self, username):
        try:
            for user in self.server_loggedUsers:
                if user.get('username') == username:
                    self.server_loggedUsers.remove(user)
                    print(f"{username} déconnecté.")
                    break
        except Exception as e:
            print(f"Erreur lors de la déconnexion de {username}: {e}")

    def handle_file_transfer(self, client_socket, data):
        From = data["From"]
        To = data["to"]
        Name = data["name"]
        filename = data["filename"]
        file_data = data["file_data"]

        if From and To and Name and filename and file_data:
            if Name in self.rooms and From in self.rooms[Name]:
                file_transfer_obj = {
                    "action": "accept_file",
                    "From": From,
                    "to": To,
                    "name": Name,
                    "filename": filename,
                    "file_data": file_data,
                    "Id": Name
                }
                print("bardella")
                for user in self.server_loggedUsers:
                    if user['username'] in self.rooms[Name]:
                        self.server_send_json(user['socket'], file_transfer_obj)
            else:
                reject_file_obj = {
                    "action": "reject_file",
                    "message": "Vous n'êtes pas dans cette salle."
                }
                self.server_send_json(client_socket, reject_file_obj)
        else:
            reject_file_obj = {
                "action": "reject_file",
                "message": "Informations de fichier manquantes."
            }
            self.server_send_json(client_socket, reject_file_obj)

if __name__ == "__main__":
    server = SSLServer('0.0.0.0', 8888)
    server.start()
