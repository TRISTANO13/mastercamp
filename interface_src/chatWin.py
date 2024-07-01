# loginWin.py
import tkinter as tk
from tkinter import messagebox
from threading import Thread

class chatWindow(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent.root)
        self.parent = parent
        self.username = username
        self.client = parent.client

        try:
            # Créer une frame principale
            main_frame = tk.Frame(self.parent.root)
            main_frame.pack(pady=20, padx=20)

            # Créer une liste carré pour les noms d'utilisateurs
            self.user_listbox = tk.Listbox(main_frame, width=30, height=10)
            self.user_listbox.pack(pady=10)

            # Ajouter des noms d'utilisateurs à la liste pour la démonstration
            # Créer les boutons
            button_frame = tk.Frame(main_frame)
            button_frame.pack(pady=10)

            self.create_room_button = tk.Button(button_frame, text="Créer une salle", command=None)
            self.create_room_button.pack(side=tk.LEFT, padx=5)

            self.disconnect_button = tk.Button(button_frame, text="Déconnexion", command=None)
            self.disconnect_button.pack(side=tk.LEFT, padx=5)
        except Exception as e:
            print("Erreur :",e)