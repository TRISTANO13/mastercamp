# mainWin.py
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext  # Importez scrolledtext pour la Scrollbar

class MainWindow(tk.Frame):
    def __init__(self, parent, username, client):
        super().__init__(parent.root)
        self.parent = parent
        self.username = username
        self.client = client
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_info = tk.Label(self, text=f"Connected as {self.username}")
        self.label_info.pack(pady=10)

        self.chat_history = scrolledtext.ScrolledText(self, height=20, width=50)
        self.chat_history.pack(pady=10)

        self.text_entry = tk.Entry(self, width=50)
        self.text_entry.pack(pady=10)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

    def send_message(self):
        message = self.text_entry.get()
        if message:
            try:
                self.client.send(message)
                self.display_message(f"You: {message}")  # Affiche le message dans l'interface utilisateur
                self.text_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Erreur lors de l'envoi du message: {e}")
        else:
            messagebox.showerror("Error", "Message cannot be empty")

    def display_message(self, message):
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.see(tk.END)  # Scroll jusqu'à la fin du texte

