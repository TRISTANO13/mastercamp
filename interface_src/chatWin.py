# chatWin.py
import tkinter as tk
from tkinter import messagebox
from threading import Thread

class ChatWindow(tk.Toplevel):
    def __init__(self, parent, selected_user, room_name, username):
        super().__init__(parent.root)
        self.parent = parent
        self.username = username
        self.selected_user = selected_user
        self.room_name = room_name
        self.client = parent.client

        try:
            self.title(f"Chat Room - {self.room_name}")
            self.geometry("500x500")

            # Créer une frame principale
            main_frame = tk.Frame(self)
            main_frame.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)

            # Créer une liste pour afficher les messages de chat
            self.chat_listbox = tk.Listbox(main_frame, width=50, height=15)
            self.chat_listbox.pack(pady=10)

            # Créer une entrée pour saisir les messages
            self.message_entry = tk.Entry(main_frame, width=40)
            self.message_entry.pack(side=tk.LEFT, pady=10, padx=5)

            # Créer un bouton pour envoyer le message
            self.send_button = tk.Button(main_frame, text="Envoyer", command=self.send_message)
            self.send_button.pack(side=tk.LEFT, pady=10, padx=5)

            # Créer un bouton pour fermer la fenêtre de chat
            self.close_button = tk.Button(main_frame, text="Fermer", command=self.destroy)
            self.close_button.pack(side=tk.RIGHT, pady=10, padx=5)

        except Exception as e:
            print("Erreur :", e)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client.client_send_chat_message(self.room_name,self.selected_user, self.username, message)
            self.message_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Message vide", "Veuillez saisir un message avant d'envoyer.")

   
    def handle_message_response(self, data):
        action = data.get("action")
        message = data.get("message")
        sender = data.get("From")
        room_id = data.get("Id")

        if action == "accept_message":
            if room_id == self.room_name:
                self.chat_listbox.insert(tk.END, f"{message}")
                self.chat_listbox.see(tk.END)  
                
        else:
            messagebox.showerror("Erreur", message)