import tkinter as tk
from loginWin import LoginWindow
from userSelectWin import UserSelectWindow

class ChatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat Application")
        self.client = None
        self.login_window = LoginWindow(self)
        self.main_window = None

    def setup_client(self, username):
        from client import ChatClient  # Assurez-vous que le nom du fichier est correct
        self.client = ChatClient(username=username)
        self.client.connect()

    def login_handler(self, username):
        try:
            print("Setting up client")
            self.setup_client(username)
            print("Client setup done")
            self.login_window.destroy()
            self.main_window = UserSelectWindow(self.root, username, self.client)
            self.main_window.pack(fill="both", expand=True)
            print("Main window setup done")
        except Exception as e:
            print(f"Error in login_handler: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatApp()
    app.run()
