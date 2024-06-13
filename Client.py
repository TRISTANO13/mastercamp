import socket
import ssl

def start_client():
    # Créer une socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Charger les certificats SSL
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('cert.pem')
    
    # Établir la connexion
    secure_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    server_address = ('localhost', 65432)
    secure_socket.connect(server_address)
    
    try:
        while True:
            message = input("Vous: ")
            secure_socket.sendall(message.encode('utf-8'))
            
            data = secure_socket.recv(1024)
            print(f"Serveur: {data.decode('utf-8')}")
            
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        secure_socket.close()

if __name__ == "__main__":
    start_client()
