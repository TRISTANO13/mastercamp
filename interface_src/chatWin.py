# chatWin.py
import tkinter as tk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkImage, CTkToplevel
from tkinter import messagebox
from threading import Thread
from PIL import Image
from CTkListbox import *
import json

class ChatWindow(CTkToplevel):
    def __init__(self, parent, selected_user, room_name, username):
        super().__init__(parent.root)
        self.parent = parent
        self.username = username
        self.selected_user = selected_user
        self.room_name = room_name
        self.client = parent.client
        self.resizable(False, False)

        try:
            self.title(f"Chat Room - {self.room_name}")
            self.geometry("500x500")
            self.send_image = CTkImage(
                light_image=Image.open('img/send-hor-svgrepo-com.png').convert('RGBA'),
                dark_image=Image.open('img/send-hor-svgrepo-com.png').convert('RGBA'),
                size=(40, 40)
            ) # WidthxHeight

            # Créer une frame principale
            self.main_frame = CTkFrame(self)
            self.main_frame.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)

            # Créer une liste pour afficher les messages de chat
            self.chat_listbox = CTkListbox(self.main_frame, width=420, height=300)
            self.chat_listbox.pack(pady=10)

            # Créer une entrée pour saisir les messages
            self.message_entry = CTkEntry(self.main_frame, width=400, height=80)
            self.message_entry.pack(side=tk.LEFT, pady=5, padx=(5, 2), anchor='s')

            # Créer un bouton pour envoyer le message
            self.send_button = CTkButton(self.main_frame, text="", command=self.send_message, width=120, height=80, image=self.send_image)
            self.send_button.pack(side=tk.LEFT, pady=5, padx=(2, 5), anchor='s')

            # Créer un bouton pour fermer la fenêtre de chat
            # self.close_button = tk.Button(self.main_frame, text="Fermer", command=self.destroy)
            # self.close_button.pack(side=tk.RIGHT, pady=10, padx=5)

        except Exception as e:
            print("Erreur lors de l'initialisation de la fenêtre de chat:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de l'initialisation de la fenêtre de chat.")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                self.client.client_send_chat_message(self.room_name, self.selected_user, self.username, message)
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                print("Erreur lors de l'envoi du message:", e)
                messagebox.showerror("Erreur", "Une erreur est survenue lors de l'envoi du message.")
        else:
            messagebox.showwarning("Message vide", "Veuillez saisir un message avant d'envoyer.")

    def handle_message_response(self, data):
        try:
            sanitized_data = self.sanitize_json(data)
            action = sanitized_data.get("action")
            message = sanitized_data.get("message")
            sender = sanitized_data.get("From")
            room_id = sanitized_data.get("Id")

            if action == "accept_message":
                if room_id == self.room_name:
                    self.chat_listbox.insert(tk.END, f"{message}")
                    # self.chat_listbox.move_down()
                    # self.chat_listbox.see(tk.END) dsl je trouverais un fix pour ça plus tards 
            else:
                messagebox.showerror("Erreur", message)
        except Exception as e:
            print("Erreur lors de la gestion de la réponse du message:", e)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la gestion de la réponse du message.")

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
