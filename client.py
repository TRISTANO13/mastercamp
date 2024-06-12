import socket
import ssl
import tkinter as tk

# Configuration du client SSL/TLS
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.load_verify_locations("server.crt")

# Connexion au serveur
def connect_to_server(username, password):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(sock, server_hostname="localhost")
    conn.connect(('localhost', 10023))
    conn.send(f"{username}:{password}".encode())
    response = conn.recv(1024).decode()
    if response == "AUTH_SUCCESS":
        return conn
    else:
        return None

# Envoi des messages
def send_message():
    message = entry.get()
    conn.send(message.encode())
    response = conn.recv(1024).decode()
    msg_list.insert(tk.END, f"You: {message}")
    msg_list.insert(tk.END, f"Server: {response}")
    entry.delete(0, tk.END)

# Interface graphique
root = tk.Tk()
root.title("Secure Chatroom")

messages_frame = tk.Frame(root)
scrollbar = tk.Scrollbar(messages_frame)
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry = tk.Entry(root, width=50)
entry.pack()
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

username = input("Username: ")
password = input("Password: ")
conn = connect_to_server(username, password)
if conn:
    tk.mainloop()
else:
    print("Authentication failed")
