
# main.py
import tkinter as tk
from interface_src.loginWin import LoginWindow
from interface_src.mainWin import MainWindow
import threading

class ChatInterface:
    def __init__(self,client):
        self.root = tk.Tk()
        self.client = client
        self.login_window = LoginWindow(self)
    
    def open_main_window(self,username):
        self.login_window.destroy()
        self.main_window = MainWindow(self, username, self.client)

    def start(self):
        self.root.mainloop()

    """def start(self):
        threading.Thread(target=self.start).start()"""

