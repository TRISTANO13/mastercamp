
# main.py
import tkinter as tk
from tkinter import messagebox
from interface_src.loginWin import LoginWindow
from interface_src.mainWin import MainWindow
from interface_src.chatWin import chatWindow
import threading

class ChatInterface:
    def __init__(self,client):
        self.root = tk.Tk()
        self.client = client
        self.login_window = LoginWindow(self)

    def open_main_window(self,username):
        try:
            self.login_window.destroy()
            self.main_window = MainWindow(self, username)
        except Exception as e:
            messagebox.showerror("Erreur", e)
            
    def open_chat_window(self,select_user,room_name,username):
        # room_window = chatWindow(self.parent.root, room_name, self.username, self.selected_user)
        print(" h ")
    
    def get_main_window(self):
        return self.main_window
        
    def start(self):
        self.root.mainloop()

    """def start(self):
        threading.Thread(target=self.start).start()"""

