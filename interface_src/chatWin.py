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
            self.geometry("500x460")
            self.send_image = CTkImage(light_image=Image.open('img/send-hor-svgrepo-com.png').convert('RGBA'),dark_image=Image.open('img/send-hor-svgrepo-com.png').convert('RGBA'),size=(40,40)) # WidthxHeight
            self.file_image = CTkImage(light_image=Image.open('img/clip-svgrepo-com.png').convert('RGBA'),dark_image=Image.open('img/clip-svgrepo-com.png').convert('RGBA'),size=(25,25)) # WidthxHeight
            self.emote_image = CTkImage(light_image=Image.open('img/clip-svgrepo-com.png').convert('RGBA'),dark_image=Image.open('img/clip-svgrepo-com.png').convert('RGBA'),size=(25,25)) # WidthxHeight
            self.trash_image = CTkImage(light_image=Image.open('img/clip-svgrepo-com.png').convert('RGBA'),dark_image=Image.open('img/clip-svgrepo-com.png').convert('RGBA'),size=(25,25)) # WidthxHeight


            # Créer une frame principale
            self.main_frame = CTkFrame(self)
            self.main_frame.pack(pady=(25), padx=20, expand=True, fill=tk.BOTH)

            # Créer une liste pour afficher les messages de chat
            self.chat_listbox = CTkListbox(self.main_frame, width=420, height=270)
            self.chat_listbox.pack(pady=10)

            self.misc_frame = CTkFrame(self.main_frame, width=50,height=85,fg_color="transparent",bg_color="transparent")
            self.misc_frame.pack(side=tk.LEFT,pady=(2,0), padx=(6,2),anchor='n')

            # Envoyer fichier
            self.file_button = CTkButton(self.misc_frame, text="a",command=self.send_message,width=28,height=28,image=self.file_image)
            self.file_button.pack(side=tk.TOP,pady=(1),padx=(4),anchor="n")
            
            self.emote_button = CTkButton(self.misc_frame, text="b",command=self.send_message,width=28,height=28)
            self.emote_button.pack(side=tk.BOTTOM,pady=(1),padx=(4),anchor="w")

            self.junk_button = CTkButton(self.misc_frame, text="c",command=self.send_message,width=28,height=28)
            self.junk_button.pack(side=tk.BOTTOM,pady=(1),padx=(4),anchor="w")

            # Créer une entrée pour saisir les messages
            self.message_entry = CTkEntry(self.main_frame, width=330,height=85)
            self.message_entry.pack(side=tk.LEFT,pady=(2,0),padx=(2),anchor='n')

            # Créer un bouton pour envoyer le message
            self.send_button = CTkButton(self.main_frame, text="",command=self.send_message,width=90,height=85,image=self.send_image)
            self.send_button.pack(side=tk.LEFT, pady=(2,0), padx=(2,10),anchor='n')

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