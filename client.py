import socket
import ssl
import json
import threading

class SSLClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket = None

    def connect(self):
        try:
            # Créer un socket TCP standard
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Enrouler le socket avec SSL
            #self.secure_socket = self.context.wrap_socket(self.socket, server_hostname=self.host)
            self.secure_socket = self.socket
            
            # Connecter au serveur
            self.secure_socket.connect((self.host, self.port))
            print(f"Connexion réussie à {self.host}:{self.port}")
            #response = self.receive(1024)
            receive_thread = threading.Thread(target=client.client_receive, args=())
            receive_thread.start()
        except Exception as e:
            print(f"Erreur de connexion: {e}")

    def send(self, message):
        try:
            self.socket.send(bytes(message,encoding="utf-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def receive(self, buffer_size=1024):
        try:
            data = self.socket.recv(buffer_size)
            return data.decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
            return None

    def client_receive(self):
        while True:
            try:
                # Recevoir des données du serveur
                response = self.receive()
                if not response:
                    print("Connexion fermée par le serveur")
                    break
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

    """ Commandes client """

    def client_login(self,username,password):
        data = {
            "action": "login",
            "username": username,
            "password": password
        }
        
        # On jsonifie le dictionnaire puis on encode le message afin de 
        # pouvoir l'envoyer, puis on l'envoie
        jsonified_data = json.dumps(data)
        self.send(jsonified_data)

try:
    # On exporte cet objet de manière à ce que le client puisse être utilisé dans les autres fichiers
    client = SSLClient("0.0.0.0",8888)
    client.connect()

except Exception as e :
    print("Erreur lors de la connexion au serveur.")
    print("\n",e);

else:
    print("Vous êtes connecté au serveur.")

