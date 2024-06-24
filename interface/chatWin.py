import tkinter as tk
from threading import Thread

class ChatWindow:
    def __init__(self, secure_socket):
        self.root = tk.Tk()
        self.root.title("Chat Window")
        self.secure_socket = secure_socket

        self.messages_frame = tk.Frame(self.root)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.msg_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()

        self.entry_field = tk.Entry(self.root)
        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.pack()
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

    def display_message(self, message):
        self.msg_list.insert(tk.END, message)

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        self.display_message(f"You: {message}")
        self.secure_socket.sendall(message.encode())

    def start(self):
        self.root.mainloop()

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        self.msg_list.insert(tk.END, f"You: {message}")
        self.secure_socket.sendall(message.encode())

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatWindow(root, "test@example.com", None)  # Passer None temporairement pour le socket sécurisé
    root.mainloop()
