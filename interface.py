
# main.py
import customtkinter as tk
from tkinter import messagebox
from interface_src.loginWin import LoginWindow
from interface_src.mainWin import MainWindow
import threading

class ChatInterface:
    def __init__(self,client):
        # Création de la fenêtre principale
        self.root = tk.CTk()
        self.root.title("DaSafe | Chat Sécurisé")
        self.root.geometry("400x600")
        self.client = client
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.resizable(False,False)
        self.login_window = LoginWindow(self)

    def open_main_window(self,username):
        try:
            self.login_window.destroy()
            self.root.geometry("800x500")
            self.main_window = MainWindow(self, username)
        except Exception as e:
            messagebox.showerror("Erreur", e)
    
    def get_main_window(self):
        return self.main_window
        
    def start(self):
        self.root.mainloop()

    """def start(self):
        threading.Thread(target=self.start).start()"""

