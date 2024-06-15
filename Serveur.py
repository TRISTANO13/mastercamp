import socket
import ssl
from threading import Thread

def handle_client(conn, addr):
    print(f"Connexion établie avec {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Reçu de {addr}: {data.decode()}")
        conn.sendall(data)
    conn.close()

def start_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('localhost', 8888))
        sock.listen(5)
        print('Serveur en attente de connexion...')

        while True:
            conn, addr = sock.accept()
            secure_conn = context.wrap_socket(conn, server_side=True)
            client_thread = Thread(target=handle_client, args=(secure_conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()