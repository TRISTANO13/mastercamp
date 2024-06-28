#server.py
import socket
import ssl

# Créer un contexte SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Créer un socket TCP standard
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8443))
server_socket.listen(5)

print("Le serveur est en attente de connexions...")

# Accepter la connexion et enrouler avec SSL
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connexion de {addr}")
    secure_socket = context.wrap_socket(client_socket, server_side=True)

    try:
        # Envoyer un message initial au client
        secure_socket.send(b"Bonjour client!")

        # Recevoir et traiter les données du client
        while True:
            data = secure_socket.recv(1024)
            if not data:
                break
            print(f"Reçu de {data.decode('utf-8')}")

    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        secure_socket.close()
