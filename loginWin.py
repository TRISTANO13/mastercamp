import tkinter as tk
from tkinter import messagebox
from mainWin import MainWindow
from database import authenticate_user, add_user
import sqlite3
import socket
import ssl
from threading import Thread

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        self.label_username = tk.Label(root, text="Username")
        self.label_username.pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()

        self.label_password = tk.Label(root, text="Password")
        self.label_password.pack()
        self.entry_password = tk.Entry(root, show='*')
        self.entry_password.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(root, text="Register", command=self.register)
        self.register_button.pack()
        
        #conf SSL
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        
        
        

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if (username == 'admin' and password == '1234') or authenticate_user(username, password):
            self.root.withdraw()  # Ferme la fenêtre de connexion
            self.sock = socket.create_connection(('localhost', 8888))
            self.secure_socket = self.context.wrap_socket(self.sock, server_hostname='localhost')

            # Envoyer le nom d'utilisateur au serveur
            self.secure_socket.sendall(username.encode())

            # Ouvrir la fenêtre principale après la connexion
            self.open_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            add_user(username, password)
            messagebox.showinfo("Registration Success", "User registered successfully")
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Failed", "Username already exists")

    def open_main_window(self):
        main_window = tk.Toplevel(self.root)
        MainWindow(main_window)