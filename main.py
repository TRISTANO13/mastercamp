# main.py
from client import *
from interface import *
import ssl

if __name__ == "__main__":
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    client = SSLClient("127.0.0.1", 8888, context)  # Passer le contexte SSL lors de l'instanciation
    client.start()
    client.interface = ChatInterface(client)
    client.interface.start()
