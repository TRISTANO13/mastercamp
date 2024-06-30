# loginWin.py
import tkinter as tk
from tkinter import messagebox
from threading import Thread

class LoginWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root)
        self.client = parent.client # On récupère le client ici héhé :) 
        self.interface = parent
        self.pack()
        self.create_widgets()
        self.username = ""

    def create_widgets(self):
        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack(pady=10)

        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=10)

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack(pady=10)

        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=10)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self, text="Register", command=self.login)
        self.register_button.pack(pady=10)
        
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.client.client_login(username,password);

    def handle_login_response(self,data):
        if "accept_login" in data.get("action"):
                messagebox.showinfo("Success", data.get("message"))
                self.interface.open_main_window(data.get("username"))
        else:
                messagebox.showerror("Error", data.get("message"))
        

"""
    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            if register_user_db(username, password):
                messagebox.showinfo("Success", "User registered successfully")
            else:
                messagebox.showerror("Error", "Username already exists")
        else:
            messagebox.showerror("Error", "Username and password are required")
"""

"""
if username and password:
            if verify_user_db(username, password):
                try:
                    self.client = client
                    self.client.client_login(username,password);
                except Exception as e:
                    messagebox.showerror("Error", f"Erreur lors de la connexion: {e}")
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Username and password are required")"""

