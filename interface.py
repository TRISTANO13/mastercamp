# interface.py
import customtkinter as tk
from tkinter import messagebox
from interface_src.loginWin import LoginWindow
from interface_src.mainWin import MainWindow
from interface_src.chatWin import ChatWindow
import threading

class ChatInterface:
    def __init__(self, client):
        try:
            # Création de la fenêtre principale
            self.root = tk.CTk()
            self.root.title("DaSafe | Chat Sécurisé")
            self.root.geometry("400x600")
            self.client = client
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.root.resizable(False, False)
            self.login_window = LoginWindow(self)
        except Exception as e:
            print(f"Erreur lors de l'initialisation de l'interface: {e}")
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'initialisation de l'interface: {e}")

    def open_main_window(self, username):
        try:
            self.login_window.destroy()
            self.root.geometry("350x600")
            self.main_window = MainWindow(self, username)
        except Exception as e:
            print(f"Erreur lors de l'ouverture de la fenêtre principale: {e}")
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'ouverture de la fenêtre principale: {e}")
            
    def open_chat_window(self, select_user, room_name, username):
        try:
            print("creation de la room")
            self.chat_window = ChatWindow(self, select_user, room_name, username)
        except Exception as e:
            print(f"Erreur lors de l'ouverture de la fenêtre de chat: {e}")
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'ouverture de la fenêtre de chat: {e}")
            
    def get_main_window(self):
        return self.main_window
        
    def start(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Erreur lors du démarrage de l'interface: {e}")
            messagebox.showerror("Erreur", f"Une erreur est survenue lors du démarrage de l'interface: {e}")

    """def start(self):
        threading.Thread(target=self.start).start()"""
