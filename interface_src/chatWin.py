# chatWin.py
import tkinter as tk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkImage, CTkToplevel
from tkinter import messagebox
from threading import Thread
from PIL import Image
from CTkListbox import *
import base64


class ChatWindow(CTkToplevel):
    def __init__(self, parent, selected_user, room_name, username):
        super().__init__(parent.root)
        self.parent = parent
        self.username = username
        self.selected_user = selected_user
        self.room_name = room_name
        self.client = parent.client
        self.resizable(False,False)

        try:
            self.title(f"Chat Room - {self.room_name}")
            self.geometry("500x500")
            self.send_image = CTkImage(light_image=Image.open('img/send-hor-svgrepo-com.png').convert('RGBA'),dark_image=Image.open('img/send-hor-svgrepo-com.png').convert('RGBA'),size=(40,40)) # WidthxHeight


            # Créer une frame principale
            self.main_frame = CTkFrame(self)
            self.main_frame.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)

            # Créer une liste pour afficher les messages de chat
            self.chat_listbox = CTkListbox(self.main_frame, width=420, height=300)
            self.chat_listbox.pack(pady=10)

            # Créer une entrée pour saisir les messages
            self.message_entry = CTkEntry(self.main_frame, width=400,height=80)
            self.message_entry.pack(side=tk.LEFT,pady=5,padx=(5,2),anchor='s')

            # Créer un bouton pour envoyer le message
            #self.send_button = CTkButton(self.main_frame, text="",command=self.send_message,width=120,height=80,image=self.send_image)
            #self.send_button.pack(side=tk.LEFT, pady=5, padx=(2,5),anchor='s')

            # Ajouter un bouton pour envoyer des fichiers
            self.send_file_button = CTkButton(self.main_frame, text="Envoyer un fichier", command=self.send_file, width=120, height=40)
            self.send_file_button.pack(side=tk.LEFT, pady=5, padx=(2, 5), anchor='s')

            # Créer un bouton pour fermer la fenêtre de chat
            #self.close_button = tk.Button(self.main_frame, text="Fermer", command=self.destroy)
            #self.close_button.pack(side=tk.RIGHT, pady=10, padx=5)

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
                #self.chat_listbox.move_down()
                #self.chat_listbox.see(tk.END) dsl je trouverais un fix pour ça plus tards 
                
        else:
            messagebox.showerror("Erreur", message)

    def send_file(self):
        filepath = tk.filedialog.askopenfilename()
        if filepath:
            self.client.client_send_file(filepath, self.room_name, self.selected_user, self.username)
        else:
            messagebox.showwarning("Fichier non sélectionné", "Veuillez sélectionner un fichier à envoyer.")

    def handle_file_response(self, data):
        action = data.get("action")
        filename = data.get("filename")
        encoded_file_data = data.get("file_data")
        sender = data.get("From")
        room_id = data.get("Id")

        if action == "accept_file" and room_id == self.room_name:
            self.chat_listbox.insert(tk.END, f"{encoded_file_data}")
            file_data = base64.b64decode(encoded_file_data)
            self.chat_listbox.insert(tk.END, f"{file_data}")
            with open(f"received_{filename}", 'wb') as file:
                file.write(file_data)
            self.chat_listbox.insert(tk.END, f"{sender} a envoyé un fichier : {filename}")
        else:
            messagebox.showerror("Erreur", "Erreur lors du transfert de fichier.")