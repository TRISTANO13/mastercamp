import tkinter as tk
from tkinter import messagebox
from threading import Thread
from client import SSLClient  
from database import verify_user_db, register_user_db

class LoginWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root)
        self.parent = parent
        self.pack()
        self.create_widgets()

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

        self.register_button = tk.Button(self, text="Register", command=self.register_user)
        self.register_button.pack(pady=10)
        
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            if verify_user_db(username, password):
                try:
                    self.client = SSLClient('localhost', 8443)
                    self.connect_and_send(username)
                except Exception as e:
                    messagebox.showerror("Error", f"Erreur lors de la connexion: {e}")
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Username and password are required")

    def connect_and_send(self, username):
        try:
            self.client.connect(username)
            self.client.send("Bonjour serveur!")
            response = self.client.receive()
            print(f"Reçu: {response}")
            self.parent.open_main_window(username, self.client)
        except Exception as e:
            messagebox.showerror("Error", f"Erreur lors de la connexion: {e}")

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
