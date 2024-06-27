import tkinter as tk
from Client import ChatClient
from loginWin import LoginWindow
from userSelectWin import UserSelectWindow

class ChatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat Application")
        self.client = None
        self.login_window = LoginWindow(self)
        self.main_window = None

    def login_handler(self, username):
        self.client = ChatClient(username=username)
        self.client.connect()
        self.login_window.destroy()
        self.main_window = UserSelectWindow(self.root, username, self.client)
        self.main_window.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatApp()
    app.run()
