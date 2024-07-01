# loginWin.py
import tkinter as tk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkImage
from tkinter import messagebox
from threading import Thread
from PIL import Image

class LoginWindow(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent.root,)
        self.client = parent.client # On récupère le client ici héhé :) 
        self.interface = parent
        self.create_widgets()
        self.username = ""
        self.grid(row=0,column=0)

    def create_widgets(self): 
        self.logo_image = CTkImage(light_image=Image.open('img/dasafe-nobg3.png').convert('RGBA'),dark_image=Image.open('img/dasafe-nobg3.png').convert('RGBA'),size=(250,200)) # WidthxHeight

        self.label_logo = CTkLabel(self,text="", image=self.logo_image,height=100,width=150)
        self.label_logo.pack(pady=(20,2),padx=50)

        self.label_username = CTkLabel(self,text="Nom d\'Utilisateur")
        self.label_username.pack(pady=(20,2),padx=50,anchor='sw')

        self.entry_username = CTkEntry(self,height=40,width=250)
        self.entry_username.pack(pady=2,)

        self.label_password = CTkLabel(self, text="Mot de Passe")
        self.label_password.pack(pady=2,padx=50,anchor='sw')

        self.entry_password = CTkEntry(self,height=40,width=250, show="*")
        self.entry_password.pack(pady=5,padx=50)

        self.login_button = CTkButton(self,height=40,width=250, text="Connexion", command=self.login)
        self.login_button.pack(pady=(20,2),padx=50)

        self.register_button = CTkButton(self,height=40,width=250, text="Inscription", command=self.register_user)
        self.register_button.pack(pady=(10,30),padx=50)
        
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.client.client_login(username,password);

    def handle_login_response(self, data):
        if data.get("action") == "accept_login":
            messagebox.showinfo("Success", data.get("message"))
            self.interface.open_main_window(data.get("username"))
        else:
            messagebox.showerror("Error", data.get("message"))
                    
    
    def handle_register_response(self, data):
        if data.get("action") == "accept_register":
            messagebox.showinfo("Success", data.get("message"))
        else:
            messagebox.showerror("Error", data.get("message"))
                
    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.client.client_register(username,password);
        


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

