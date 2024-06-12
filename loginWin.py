import tkinter as tk
from tkinter import messagebox
from mainWin import MainWindow
from database import authenticate_user, add_user
import sqlite3

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

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if (username == 'admin' and password == '1234') or authenticate_user(username, password):
            self.root.withdraw()  # Ferme la fenêtre de connexion
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