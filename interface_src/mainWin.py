# mainWin.py
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkImage
from CTkListbox import *
from PIL import Image

class MainWindow(CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent.root)
        self.parent = parent
        self.username = username
        self.client = parent.client
        self.client.client_get_logged_users()
        self.interface = parent
        
        try:
            # Créer une frame principale
            self.user_frame = CTkFrame(self.parent.root, height=110, width=350, bg_color="#1c1c1c", fg_color="#1c1c1c")
            self.user_frame.pack(anchor='n')

            self.user_image = CTkImage(light_image=Image.open('img/user-svgrepo-com.png').convert('RGBA'), dark_image=Image.open('img/user-svgrepo-com.png').convert('RGBA'), size=(70,70)) # WidthxHeight
            self.chat_image = CTkImage(light_image=Image.open('img/chat-dots-svgrepo-com.png').convert('RGBA'), dark_image=Image.open('img/chat-dots-svgrepo-com.png').convert('RGBA'), size=(20,20)) # WidthxHeight
            self.logout_image = CTkImage(light_image=Image.open('img/logout-svgrepo-com.png').convert('RGBA'), dark_image=Image.open('img/logout-svgrepo-com.png').convert('RGBA'), size=(20,20)) # WidthxHeight
            self.refresh_image = CTkImage(light_image=Image.open('img/refresh-svgrepo-com.png').convert('RGBA'), dark_image=Image.open('img/refresh-svgrepo-com.png').convert('RGBA'), size=(20,20)) # WidthxHeight

            self.user_profile_label = CTkLabel(self.user_frame, text="", height=100, width=100, image=self.user_image)
            self.user_profile_label.pack(side=tk.LEFT, anchor="w")
            
            self.user_name_label = CTkLabel(self.user_frame, text=f"Connected as {self.username}\n", height=100, width=250, anchor='w')
            self.user_name_label.pack(side=tk.RIGHT, anchor='e', pady=(8,0))

            self.main_frame = CTkFrame(self.parent.root, height=500, width=100)
            self.main_frame.pack(anchor='s')

            # Créer une liste carré pour les noms d'utilisateurs
            self.user_listbox = CTkListbox(self.main_frame, width=350, height=400, border_color="#2b2b2b", command=self.on_user_select)
            self.user_listbox.pack(pady=10)

            # Ajouter un événement de sélection à la Listbox
            #self.user_listbox.bind('<<ListboxSelect>>', self.on_user_select)

            # Ajouter des noms d'utilisateurs à la liste pour la démonstration
            # Créer les boutons
            button_frame = CTkFrame(self.main_frame, bg_color="#2b2b2b", fg_color="#2b2b2b", width=350, height=290)
            button_frame.pack(pady=10)

            self.create_room_button = CTkButton(button_frame, text="", height=120, width=90, command=self.refresh, image=self.refresh_image)
            self.create_room_button.pack(side=tk.LEFT, padx=5)

            self.disconnect_button = CTkButton(button_frame, text="", command=self.create_room, height=120, width=80, image=self.chat_image)
            self.disconnect_button.pack(side=tk.LEFT, padx=5)

            self.settings = CTkButton(button_frame, text="", command=lambda: self.deco(username), height=120, width=80, image=self.logout_image)
            self.settings.pack(side=tk.LEFT, padx=5)
            
            self.parent.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        except Exception as e:
            print("Erreur lors de l'initialisation de la fenêtre principale:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de l'initialisation de la fenêtre principale.")
    
    def set_loggedIn_Users(self, users):
        try:
            # Effacer tous les éléments actuels de la Listbox
            self.user_listbox.delete(0, tk.END)

            # Insérer les nouveaux utilisateurs dans la Listbox
            for user in users:
                self.user_listbox.insert(tk.END, user)
        except Exception as e:
            print("Erreur lors de la mise à jour de la liste des utilisateurs connectés:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la mise à jour de la liste des utilisateurs connectés.")
            
    def close_window(self):
        print("Déconnecté")
        self.parent.root.destroy()
    
    def deco(self, username):
        try:
            self.client.client_deco(username)
        except Exception as e:
            print("Erreur lors de la déconnexion:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la déconnexion.")

    def on_closing(self):
        self.deco(self.username)

    def on_user_select(self, value):
        self.selected_user = value

    def create_room(self):
        if hasattr(self, 'selected_user') and self.selected_user:
            room_name = f"Room with {self.selected_user}"
            try:
                self.client.client_create_room(self.username, self.selected_user, room_name)
            except Exception as e:
                print("Erreur lors de la création de la salle:", e)
                messagebox.showerror("Erreur", "Une erreur est survenue lors de la création de la salle.")
        else:
            messagebox.showwarning("Sélectionner un utilisateur", "Veuillez sélectionner un utilisateur pour créer une salle.")

    def handle_room_response(self, data):
        try:
            sanitized_data = self.sanitize_json(data)
            if sanitized_data.get("action") == "accept_room":
                messagebox.showinfo("Success", sanitized_data.get("message"))
                self.interface.open_chat_window(sanitized_data.get("To"), sanitized_data.get("Name"), sanitized_data.get("From"))
            else:
                messagebox.showerror("Error", sanitized_data.get("message"))
        except Exception as e:
            print("Erreur lors de la gestion de la réponse de création de salle:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la gestion de la réponse de création de salle.")
            
    def refresh(self):
        try:
            self.client.client_get_logged_users()
        except Exception as e:
            print("Erreur lors de la récupération des utilisateurs connectés:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la récupération des utilisateurs connectés.")

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
