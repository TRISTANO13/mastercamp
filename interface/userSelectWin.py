import tkinter as tk
from tkinter import messagebox
from database import get_connected_users
from chatRoomWin import ChatRoomWindow

class UserSelectWindow(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Select User to Chat:")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.load_users()

        self.chat_button = tk.Button(self, text="Chat", command=self.open_chat)
        self.chat_button.pack(pady=10)

    def load_users(self):
        users = get_connected_users()
        for user in users:
            if user != self.username:
                self.listbox.insert(tk.END, user)

    def open_chat(self):
        selected_user = self.listbox.get(tk.ACTIVE)
        if selected_user:
            self.destroy()
            self.chat_window = ChatRoomWindow(self.parent, self.username, selected_user)
            self.chat_window.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("Selection Error", "Please select a user to chat with")
