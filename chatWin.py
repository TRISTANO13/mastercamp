import tkinter as tk
from tkinter import Toplevel

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
    
    def send_message(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        self.msg_list.insert(tk.END, f"You: {message}")
        # Here you would handle sending the message to the server and getting the response
        self.msg_list.insert(tk.END, f"{self.email}: Echo: {message}")
