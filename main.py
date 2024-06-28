#main.py
import tkinter as tk
from loginWin import LoginWindow
from mainWin import MainWindow

class App:
    def __init__(self, root):
        self.root = root
        self.login_window = LoginWindow(self)

    def open_main_window(self, username, client):
        self.login_window.destroy()
        self.main_window = MainWindow(self, username, client)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()