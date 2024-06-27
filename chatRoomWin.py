import tkinter as tk
from threading import Thread

class ChatRoomWindow(tk.Frame):
    def __init__(self, parent, username, recipient, client):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.recipient = recipient
        self.client = client
        self.pack(fill="both", expand=True)
        self.create_widgets()

        # Thread pour recevoir les messages
        Thread(target=self.receive_messages).start()

    def create_widgets(self):
        print("Creating ChatRoomWindow widgets")
        self.text_area = tk.Text(self)
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=10, padx=10, fill=tk.X)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to User Selection", command=self.back_to_user_select)
        self.back_button.pack(pady=10)
        print("Widgets created")

    def receive_messages(self):
        while True:
            try:
                message = self.client.client_socket.recv(1024).decode()
                if message:
                    self.text_area.insert(tk.END, f"{message}\n")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_message(self):
        message = self.entry.get()
        if message:
            full_message = f"{self.username}: {message}"
            self.client.send_message(full_message)
            self.text_area.insert(tk.END, f"{full_message}\n")
            self.entry.delete(0, tk.END)

    def back_to_user_select(self):
        self.destroy()
        from userSelectWin import UserSelectWindow  # Import dynamique pour éviter une boucle d'import
        user_select_window = UserSelectWindow(self.parent, self.username, self.client)
        user_select_window.pack(fill="both", expand=True)
