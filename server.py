import socket
import ssl
import json
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
            client_socket.sendall(bytes(message, encoding="utf-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def handle_login(self, client_socket, data):
        username = data["username"]
        password = data["password"]

        if username and password:
            if verify_user_db(username, password):
                self.server_send(client_socket, "Connexion réussie !")
            else:
                self.server_send(client_socket, "Utilisateur introuvable !")
        else:
            self.server_send(client_socket, "L'utilisateur et le mot de passe sont nécessaires.")

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Le serveur est en attente de connexions...")

        # Accepter la connexion et enrouler avec SSL
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connexion de {addr}")
            """secure_socket = context.wrap_socket(client_socket, server_side=True)"""
            secure_socket = client_socket
            try:
                # Envoyer un message initial au client
                # secure_socket.send(b"Bonjour client!")

                # Recevoir et traiter les données du client
                while True:
                    data = secure_socket.recv(1024)
                    if not data:
                        break

                    decoded_data = data.decode('utf-8')
                    dejsonified_data = None
                    # print(decoded_data)

                    try:
                        dejsonified_data = json.loads(decoded_data)  # Convertit le JSON en dictionnaire pour pouvoir l'utiliser avec Python
                    except:
                        print(f"Info : Non JSON data received.")

                    if dejsonified_data and dejsonified_data.get('action') == "login":
                        self.handle_login(secure_socket, dejsonified_data)

                    print(f"Reçu de {addr} : {data.decode('utf-8')}")

            except Exception as e:
                print(f"Erreur: {e}")
            finally:
                secure_socket.close()

if __name__ == "__main__":
    server = SSLServer('0.0.0.0', 8888)
    server.start()
