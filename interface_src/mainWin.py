# mainWin.py
import tkinter as tk
from tkinter import messagebox


class MainWindow(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent.root)
        self.parent = parent
        self.username = username
        self.client = parent.client
        self.client.client_get_logged_users()
        self.interface = parent
        
        try:
            # Créer une frame principale
            main_frame = tk.Frame(self.parent.root)
            main_frame.pack(pady=20, padx=20)

            # Créer une liste carré pour les noms d'utilisateurs
            self.user_listbox = tk.Listbox(main_frame, width=30, height=10)
            self.user_listbox.pack(pady=10)

            # Ajouter un événement de sélection à la Listbox
            self.user_listbox.bind('<<ListboxSelect>>', self.on_user_select)

            # Ajouter des noms d'utilisateurs à la liste pour la démonstration
            # Créer les boutons
            button_frame = tk.Frame(main_frame)
            button_frame.pack(pady=10)

            self.create_room_button = tk.Button(button_frame, text="Créer une salle", command=self.create_room)
            self.create_room_button.pack(side=tk.LEFT, padx=5)

            self.disconnect_button = tk.Button(button_frame, text="Déconnexion", command=lambda: self.deco(username))
            self.disconnect_button.pack(side=tk.LEFT, padx=5)
            
            self.refresh_button = tk.Button(button_frame, text="Rafraichir", command=self.refresh)
            self.refresh_button.pack(side=tk.LEFT, padx=5)
            
            self.parent.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        except Exception as e:
            messagebox.showerror("Erreur", e)
    
    def set_loggedIn_Users(self, users):
        try:
            # Effacer tous les éléments actuels de la Listbox
            self.user_listbox.delete(0, tk.END)

            # Insérer les nouveaux utilisateurs dans la Listbox
            for user in users:
                self.user_listbox.insert(tk.END, user)
        except Exception as e:
            messagebox.showerror("Erreur", e)
            
    def close_window(self):
        print("Déconnecté")
        self.parent.root.destroy()
    
    def deco(self, username):
        self.client.client_deco(username)

    def on_closing(self):
        self.deco(self.username)

    def on_user_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            self.selected_user = widget.get(index)
        else:
            self.selected_user = None

    def create_room(self):
        if hasattr(self, 'selected_user') and self.selected_user:
            room_name = f"Room with {self.selected_user}"
            self.client.client_create_room(self.username,self.selected_user,room_name)
             
        else:
            messagebox.showwarning("Sélectionner un utilisateur", "Veuillez sélectionner un utilisateur pour créer une salle.")


    def handle_room_response(self, data):
        if data.get("action") == "accept_room":
            messagebox.showinfo("Success", data.get("message"))
            self.interface.open_chat_window(data.get("To"),data.get("Name"),data.get("From"))
        else:
            messagebox.showerror("Error", data.get("message"))
            
    def refresh(self):
        self.client.client_get_logged_users()
              