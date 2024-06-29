import socket
import ssl
import json
import threading
from database import verify_user_db

# Créer un contexte SSL
"""context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")"""

# Créer un socket TCP standard
class SSLServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket = None

    def server_send(self, client_socket, message):
        try:
            client_socket.sendall(message.encode("UTF-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def server_send_json(self, client_socket, json_message):
        try:
            client_socket.sendall(json.dumps(json_message).encode("UTF-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def server_receive(self):
        # Accepter la connexion et enrouler avec SSL
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connexion de {addr}")
            """secure_socket = context.wrap_socket(client_socket, server_side=True)"""
            secure_socket = client_socket
            try:
                # Recevoir et traiter les données du client
                while True:
                    data = secure_socket.recv(1024)
                    if not data:
                        break
                    
                    # On décide ce qu'on fait de ce qu'on a reçu
                    self.handle_received_data(secure_socket,data);
                    # On affiche ce qu'on a reçu 
                    print(f"Reçu de {addr} : {data.decode('utf-8')}")

            except Exception as e:
                print(f"Erreur: {e}")
            finally:
                secure_socket.close()

    def handle_login(self, client_socket, data):
        username = data["username"] 
        password = data["password"]

        if username and password:
            if verify_user_db(username, password):
                accept_login_obj = {
                    "action": "accept_login",
                    "message":"Connexion réussie."
                }

                self.server_send_json(client_socket,accept_login_obj)
            else:
                reject_login_obj = {
                    "action": "reject_login",
                    "message":"Utilisateur ou mot de passe incorrect."
                }

                self.server_send_json(client_socket, reject_login_obj)
        else:
            reject_login_obj = {
                    "action": "reject_login",
                    "message":"Utilisateur ou mot de passe manquant."
                }

            self.server_send_json(client_socket, reject_login_obj)

    def handle_received_data(self,client_socket,data):
        decoded_data = data.decode('utf-8') # Je decode la data pour l'avoir en texte
        dejsonified_data = None

        ## =========== DONNEES RECUES EN JSON ============== ##
        if json.loads(decoded_data) :

            dejsonified_data = json.loads(decoded_data);

            if dejsonified_data and dejsonified_data.get('action') == "login":
                self.handle_login(client_socket, dejsonified_data)
            
        ## =========== DONNEES RECUES NON JSON ============== ##



    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print("Le serveur est en attente de connexions...")
            receive_thread = threading.Thread(target=server.server_receive, args=())
            receive_thread.start()
        except Exception as e:
            print("Erreur lors du lancement du server. : \n",e)

        

if __name__ == "__main__":
    server = SSLServer('0.0.0.0', 8888)
    server.start()