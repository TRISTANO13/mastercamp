import tkinter as tk
from chatWin import ChatWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Chat Application")
        
        self.email_list = tk.Listbox(root)
        self.email_list.pack(fill=tk.BOTH, expand=True)
        
        self.email_list.bind('<Double-1>', self.open_chat_window)
        
        self.populate_emails()
    
    def populate_emails(self):
        # Sample email addresses
        emails = ["email1@example.com", "email2@example.com", "email3@example.com"]
        for email in emails:
            self.email_list.insert(tk.END, email)
    
    def open_chat_window(self, event):
        selected_email = self.email_list.get(self.email_list.curselection())
        ChatWindow(self.root, selected_email)
