import socket
import ssl
from threading import Thread

def receive_messages(secure_socket):
    while True:
        try:
            data = secure_socket.recv(1024)
            if not data:
                break
            print(f"Reçu: {data.decode()}")
        except:
            break

def start_client():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection(('localhost', 8888)) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as secure_socket:
            print(secure_socket.version())
            Thread(target=receive_messages, args=(secure_socket,)).start()
            while True:
                message = input("Vous: ")
                secure_socket.sendall(message.encode())

if __name__ == "__main__":
    start_client()