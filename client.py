import socket
import ssl
import threading

class ChatClient:
    def __init__(self, host='localhost', port=8888, username=''):
        self.host = host
        self.port = port
        self.username = username
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.context.load_verify_locations('cert.pem')
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.client_socket = None

    def connect(self):
        try:
            print(f"Connecting to {self.host}:{self.port} as {self.username}")
            self.client_socket = self.context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname='localhost')
            self.client_socket.connect((self.host, self.port))
            self.client_socket.sendall(self.username.encode())
            threading.Thread(target=self.receive_messages).start()
            print("Connected and message receiving thread started")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_message(self, message):
        if self.client_socket:
            try:
                self.client_socket.sendall(message.encode())
            except Exception as e:
                print(f"Error sending message: {e}")
