import tkinter as tk
from database import add_message, get_messages

class ChatRoomWindow(tk.Frame):
    def __init__(self, parent, username, recipient):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.recipient = recipient
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.text_area = tk.Text(self)
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=10, padx=10, fill=tk.X)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        # Ajout du bouton de retour
        self.back_button = tk.Button(self, text="Back to User Selection", command=self.back_to_user_select)
        self.back_button.pack(pady=10)

        # Appel initial pour charger les messages
        self.load_messages()

        # Appel périodique pour rafraîchir les messages
        self.refresh_messages()

    def load_messages(self):
        messages = get_messages(self.username, self.recipient)
        self.text_area.delete(1.0, tk.END)  # Efface tous les messages actuels
        for sender, message in messages:
            self.text_area.insert(tk.END, f"{sender}: {message}\n")

    def refresh_messages(self):
        self.load_messages()
        self.after(3000, self.refresh_messages)  # Rafraîchit toutes les 3 secondes (3000 ms)

    def send_message(self):
        message = self.entry.get()
        if message:
            self.text_area.insert(tk.END, f"{self.username}: {message}\n")
            add_message(self.username, self.recipient, message)
            self.entry.delete(0, tk.END)

    def back_to_user_select(self):
        self.destroy()  # Détruit la fenêtre actuelle
        from userSelectWin import UserSelectWindow  # Import dynamique pour éviter une boucle d'import
        user_select_window = UserSelectWindow(self.parent, self.username)
        user_select_window.pack(fill="both", expand=True)
