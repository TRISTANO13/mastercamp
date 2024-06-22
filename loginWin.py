import tkinter as tk
from tkinter import messagebox
from database import check_credentials, add_connected_user

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

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            if check_credentials(username, password):
                add_connected_user(username)
                self.parent.login_handler(username)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password")
