import tkinter as tk
from tkinter import messagebox
from chatRoomWin import ChatRoomWindow

class UserSelectWindow(tk.Frame):
    def __init__(self, parent, username, client):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.client = client
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        print("Creating UserSelectWindow widgets")
        self.label = tk.Label(self, text="Select User to Chat:")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.load_users()

        self.chat_button = tk.Button(self, text="Chat", command=self.open_chat)
        self.chat_button.pack(pady=10)
        print("Widgets created")

    def load_users(self):
        print("Loading users")
        self.listbox.delete(0, tk.END)
        try:
            print("Sending /get_users command to server")
            self.client.send_message("/get_users")
            response = self.client.client_socket.recv(1024).decode()
            print(f"Received response: {response}")
            users = response.split(',')
            for user in users:
                if user != self.username:
                    self.listbox.insert(tk.END, user)
            print("Users loaded:", users)
        except Exception as e:
            print(f"Error loading users: {e}")

    def open_chat(self):
        selected_user = self.listbox.get(tk.ACTIVE)
        if selected_user:
            self.destroy()
            self.chat_window = ChatRoomWindow(self.parent, self.username, selected_user, self.client)
            self.chat_window.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("Selection Error", "Please select a user to chat with")
