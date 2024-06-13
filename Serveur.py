import socket
import ssl

def start_server():
    # Créer une socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Lier la socket à l'adresse et au port
    server_address = ('localhost', 65432)
    server_socket.bind(server_address)
    
    # Écouter les connexions entrantes max 5 en attt
    server_socket.listen(5)
    
    print("Serveur en attente de connexion...")

    # Charger les certificats SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion de {addr}")
        
        # Envelopper la socket avec SSL
        secure_socket = context.wrap_socket(client_socket, server_side=True)
        
        try:
            while True:
                data = secure_socket.recv(1024)
                if data:
                    print(f"Reçu: {data.decode('utf-8')}")
                    secure_socket.sendall(data)
                else:
                    break
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            secure_socket.close()

if __name__ == "__main__":
    start_server()
