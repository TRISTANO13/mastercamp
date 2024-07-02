import socket
import ssl
import json
import threading

class SSLClient:
    def __init__(self, host, port, context):
        self.host = host
        self.port = port
        self.context = context  # Ajout du contexte SSL
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket = None
        self.interface = None

    def start(self):
        self.connect()
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.secure_socket = self.context.wrap_socket(self.socket, server_hostname=self.host)
            self.secure_socket.connect((self.host, self.port))
            print(f"Connexion réussie à {self.host}:{self.port}")
            receive_thread = threading.Thread(target=self.client_receive, args=())
            receive_thread.start()
        except Exception as e:
            print(f"Erreur de connexion: {e}")

    def client_send(self, message):
        try:
            self.secure_socket.send(bytes(message, encoding="utf-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def client_send_json(self, json_message):
        try:
            self.secure_socket.sendall(json.dumps(json_message).encode("UTF-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")
    
    def receive(self, buffer_size=1024):
        try:
            data = self.secure_socket.recv(buffer_size)
            return data.decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
            return None
    
    def client_get_logged_users(self):
        data = {
            "action": "get_logged_users"
        }
        self.secure_socket.sendall(bytes(json.dumps(data), encoding='utf-8'))

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

                print(f"Réponse du serveur: {response}")
            except ConnectionResetError:
                print("Connexion réinitialisée par le serveur")
                break

    def close(self):
        try:
            self.secure_socket.close()
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
   
if __name__ == "__main__":
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    client = SSLClient('127.0.0.1', 8888, context)
    client.start()
    # Example usage
    # client.client_register('test_user', 'password123')
    # client.client_login('test_user', 'password123')
    # client.client_create_room('test_user', 'another_user', 'room1')
    # client.client_send_chat_message('room1', 'another_user', 'test_user', 'Hello there!')


