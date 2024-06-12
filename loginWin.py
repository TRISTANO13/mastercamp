import tkinter as tk
from tkinter import messagebox
from mainWin import MainWindow

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

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Simuler l'authentification
        if self.authenticate_user(username, password):
            self.root.withdraw()  # Ferme la fenêtre de connexion
            self.open_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def authenticate_user(self, username, password):
        # Vous devriez remplacer cette fonction par une vérification réelle
        return username == "user" and password == "pass"

    def open_main_window(self):
        main_window = tk.Toplevel(self.root)
        MainWindow(main_window)
