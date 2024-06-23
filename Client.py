import socket
import ssl
import threading

class ChatClient:
    def __init__(self, host='localhost', port=8888, username=''):
        self.host = host
        self.port = port
        self.username = username
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations('cert.pem')
        self.client_socket = None

    def connect(self):
        self.client_socket = self.context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=self.host)
        self.client_socket.connect((self.host, self.port))
        self.client_socket.sendall(self.username.encode())
        threading.Thread(target=self.receive_messages).start()

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

if __name__ == '__main__':
    username = input("Enter your username: ")
    client = ChatClient(username=username)
    client.connect()

    while True:
        message = input()
        client.send_message(message)
