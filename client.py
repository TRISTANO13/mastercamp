import socket
import ssl

class SSLClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.socket = None
        self.secure_socket = None
        self.username = ""

    def connect(self, username):
        try:
            self.username = username
            # Créer un socket TCP standard
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Enrouler le socket avec SSL
            self.secure_socket = self.context.wrap_socket(self.socket, server_hostname=self.host)
            # Connecter au serveur
            self.secure_socket.connect((self.host, self.port))
            print(f"Connexion réussie à {self.host}:{self.port}")
        except Exception as e:
            print(f"Erreur de connexion: {e}")

    def send(self, message):
        try:
            full_message = f"{self.username}: {message}"
            self.secure_socket.send(full_message.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def receive(self, buffer_size=1024):
        try:
            data = self.secure_socket.recv(buffer_size)
            return data.decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
            return None

    def close(self):
        try:
            self.secure_socket.close()
            print("Connexion fermée")
        except Exception as e:
            print(f"Erreur lors de la fermeture de la connexion: {e}")

if __name__ == "__main__":
    username = input('Entrez votre nom : ')
    client = SSLClient('localhost', 8443)
    client.connect(username)
    client.send("Bonjour serveur!")
    response = client.receive()
    print(f"Reçu: {response}")
    client.close()


