import tkinter as tk
from tkinter import Toplevel
import socket
import ssl
from threading import Thread

class ChatWindow:
    def __init__(self, parent, email):
        self.top = Toplevel(parent)
        self.top.title(f"Chat with {email}")
        
        self.messages_frame = tk.Frame(self.top)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.msg_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()
        
        self.entry_field = tk.Entry(self.top)
        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.pack()
        self.send_button = tk.Button(self.top, text="Send", command=self.send_message)
        self.send_button.pack()
        
        self.email = email
        
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

        self.sock = socket.create_connection(('localhost', 8888))
        self.secure_socket = self.context.wrap_socket(self.sock, server_hostname='localhost')
        
        Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            try:
                data = self.secure_socket.recv(1024)
                if not data:
                    break
                self.msg_list.insert(tk.END, f"{self.email}: {data.decode()}")
            except:
                break

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        self.msg_list.insert(tk.END, f"You: {message}")
        self.secure_socket.sendall(message.encode())

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatWindow(root, "test@example.com")
    root.mainloop()
