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
        try:
            self.client.client_login(username, password)
        except Exception as e:
            print("Erreur lors de la tentative de connexion:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la tentative de connexion.")
            
    def handle_login_response(self, data):
        try:
            sanitized_data = self.sanitize_json(data)
            if sanitized_data.get("action") == "accept_login":
                messagebox.showinfo("Success", sanitized_data.get("message"))
                self.interface.open_main_window(sanitized_data.get("username"))
            else:
                messagebox.showerror("Error", sanitized_data.get("message"))
        except Exception as e:
            print("Erreur lors de la gestion de la réponse de connexion:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la gestion de la réponse de connexion.")
                    
    def handle_register_response(self, data):
        try:
            sanitized_data = self.sanitize_json(data)
            if sanitized_data.get("action") == "accept_register":
                messagebox.showinfo("Success", sanitized_data.get("message"))
            else:
                messagebox.showerror("Error", sanitized_data.get("message"))
        except Exception as e:
            print("Erreur lors de la gestion de la réponse d'inscription:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la gestion de la réponse d'inscription.")
                
    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        try:
            self.client.client_register(username, password)
        except Exception as e:
            print("Erreur lors de l'inscription:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de l'inscription.")

    def sanitize_json(self, data):
        try:
            # Vérifie que data est bien un dictionnaire
            if not isinstance(data, dict):
                raise ValueError("Les données ne sont pas un dictionnaire valide.")
            
            # Nettoie les valeurs du dictionnaire
            sanitized_data = {}
            for key, value in data.items():
                if isinstance(value, str):
                    sanitized_data[key] = value.strip()
                else:
                    sanitized_data[key] = value

            return sanitized_data
        except Exception as e:
            print("Erreur lors de la sanitization des données JSON:", e)
            return {}
