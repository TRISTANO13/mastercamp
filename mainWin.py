import tkinter as tk
from tkinter import Listbox, messagebox
import socket
import ssl
from threading import Thread
from chatWin import*

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("User Chat Application")

        self.user_listbox = Listbox(root)
        self.user_listbox.pack(fill=tk.BOTH, expand=True)

        self.user_listbox.bind('<Double-1>', self.open_chat_window)

        # Liste des utilisateurs connectés
        self.connected_users = []

        # Configuration du socket et de la connexion sécurisée
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.sock = socket.create_connection(('localhost', 8888))
        self.secure_socket = self.context.wrap_socket(self.sock, server_hostname='localhost')

        # Envoyer le nom d'utilisateur au serveur
        self.send_username_to_server()

        # Démarrer le thread pour recevoir les utilisateurs connectés
        Thread(target=self.receive_connected_users).start()

    def send_username_to_server(self):
        username = "admin"  # Remplacez par le nom d'utilisateur de l'utilisateur actuel
        self.secure_socket.sendall(username.encode())

    def receive_connected_users(self):
        print('Thread started to receive connected users')
        while True:
            try:
                data = self.secure_socket.recv(1024)
                if not data:
                    print("no data")
                    break
                self.connected_users = data.decode().split(',')
                self.update_user_list()
            except Exception as e:
                print(f'Error receiving connected users: {e}')
                break

    def update_user_list(self):
        self.user_listbox.delete(0, tk.END)
        for user in self.connected_users:
            self.user_listbox.insert(tk.END, user)

    def open_chat_window(self, event):
        try:
            selected_user = self.user_listbox.get(self.user_listbox.curselection())
            if selected_user in self.connected_users:
                ChatWindow(self.root, selected_user)
            else:
                messagebox.showerror("Error", "Selected user is not currently connected.")
        except tk.TclError:
            pass  # Aucune sélection

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
