# userChatApp.py

import tkinter as tk

class UserChatApplication(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.welcome_label = tk.Label(self, text=f"Welcome, {self.username}!")
        self.welcome_label.pack()

        # Placez ici la logique pour afficher la liste des utilisateurs ou le chat

        self.logout_button = tk.Button(self, text="Logout", command=self.logout)
        self.logout_button.pack()

    def logout(self):
        self.parent.show_login()
