# main.py
from client import SSLClient
from interface import ChatInterface
import ssl
from tkinter import messagebox

if __name__ == "__main__":
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        client = SSLClient("127.0.0.1", 8888, context)  # Passer le contexte SSL lors de l'instanciation
        client.start()
        client.interface = ChatInterface(client)
        client.interface.start()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de l'application: {e}")
        messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'initialisation de l'application: {e}")
