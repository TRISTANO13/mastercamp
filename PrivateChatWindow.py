import tkinter as tk
from threading import Thread

class PrivateChatWindow:
    def __init__(self, secure_socket, room_name):
        self.top = tk.Toplevel()
        self.top.title(f"Private Room: {room_name}")
        
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
        
        self.secure_socket = secure_socket
        self.room_name = room_name

        Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            try:
                data = self.secure_socket.recv(1024)
                if not data:
                    break
                self.msg_list.insert(tk.END, data.decode())
            except:
                break

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        self.secure_socket.sendall(f"/private {self.room_name}: {message}".encode())
