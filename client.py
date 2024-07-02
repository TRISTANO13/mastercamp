import socket
import ssl
import json
import threading
import os
import base64

class SSLClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket = None
        self.interface = None

    def start(self):
        self.connect()
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.secure_socket = self.socket
            self.secure_socket.connect((self.host, self.port))
            print(f"Connexion réussie à {self.host}:{self.port}")
            receive_thread = threading.Thread(target=self.client_receive, args=())
            receive_thread.start()
        except Exception as e:
            print(f"Erreur de connexion: {e}")

    def client_send(self, message):
        try:
            self.socket.send(bytes(message, encoding="utf-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def client_send_json(self, json_message):
        try:
            self.socket.sendall(json.dumps(json_message).encode("UTF-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")
    
    def receive(self, buffer_size=1000000000):
        try:
            data = self.socket.recv(buffer_size)
            return data.decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
            return None
    
    def client_get_logged_users(self):
        data = {
            "action": "get_logged_users"
        }
        self.socket.sendall(bytes(json.dumps(data), encoding='utf-8'))

    def client_receive(self):
        while True:
            try:
                response = self.receive()
                if not response:
                    print("Connexion fermée par le serveur")
                    break

                dejsonified_data = None
                try:
                    dejsonified_data = json.loads(response)
                except:
                    print("Info : Non JSON data received.")

                if dejsonified_data:
                    if dejsonified_data.get('action') == "accept_login" or dejsonified_data.get('action') == "reject_login":
                        self.interface.login_window.handle_login_response(dejsonified_data)
                    if dejsonified_data.get('action') == "accept_register" or dejsonified_data.get('action') == "reject_register":
                        self.interface.login_window.handle_register_response(dejsonified_data)
                    if dejsonified_data.get('action') == "get_logged_users":
                        self.interface.main_window.set_loggedIn_Users(dejsonified_data.get('value'))
                    if dejsonified_data.get('action') == "close_window":
                        self.interface.main_window.close_window()
                    if dejsonified_data.get('action') == "accept_room" or dejsonified_data.get('action') == "reject_room":
                        self.interface.main_window.handle_room_response(dejsonified_data)
                    if dejsonified_data.get('action') == "accept_message" or dejsonified_data.get('action') == "reject_message":
                        self.interface.chat_window.handle_message_response(dejsonified_data)
                    if dejsonified_data.get('action') == "accept_file" or dejsonified_data.get('action') == "reject_file":
                        self.interface.chat_window.handle_file_response(dejsonified_data)

                print(f"Réponse du serveur: {response}")
            except ConnectionResetError:
                print("Connexion réinitialisée par le serveur")
                break

    def close(self):
        try:
            self.socket.close()
            print("Connexion fermée")
        except Exception as e:
            print(f"Erreur lors de la fermeture de la connexion: {e}")

    def client_login(self, username, password):
        data = {
            "action": "login",
            "username": username,
            "password": password
        }
        self.client_send_json(data)
        
    def client_deco(self, username):
        data = {
            "action": "deconnexion",
            "username": username,
        }
        self.client_send_json(data)

    def client_register(self, username, password):
        data = {
            "action": "register",
            "username": username,
            "password": password
        }
        self.client_send_json(data)
        
    def client_create_room(self, username, selected_user, room_name):
        data = {
            "action": "create_room",
            "From": username,
            "to": selected_user,
            "name": room_name
        }
        self.client_send_json(data)
        
    def client_send_chat_message(self, room_name, selected_user, username, message):
        data = {
            "action": "room_message",
            "From": username,
            "to": selected_user,
            "name": room_name,
            "message": message
        }
        self.client_send_json(data)

    def client_send_file(self, filepath, room_name, selected_user, username):
        try:
            with open(filepath, 'rb') as file:
                file_data = file.read()
                encoded_file_data = base64.b64encode(file_data).decode('utf-8')
                filename = os.path.basename(filepath)
                data = {
                    "action": "send_file",
                    "From": username,
                    "to": selected_user,
                    "name": room_name,
                    "filename": filename,
                    "file_data": encoded_file_data  # Encode file data to base64 string
                }
                self.client_send_json(data)
        except Exception as e:
            print(f"Erreur lors de l'envoi du fichier: {e}")
   

