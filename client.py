import socket
import ssl
import json
import threading
import tkinter as tk
from tkinter import messagebox


class SSLClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket = None
        self.interface = None

    def start(self):

        self.connect()
    ## ========== FONCTIONS ESSENTIELLES 
    def connect(self):
        try:
            # Créer un socket TCP standard
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Enrouler le socket avec SSL
            #self.secure_socket = self.context.wrap_socket(self.socket, server_hostname=self.host)
            self.secure_socket = self.socket
            # Connecter au serveur
            self.secure_socket.connect((self.host, self.port))
            print(f"Connexion réussie à {self.host}:{self.port}")
            #response = self.receive(1024)
            receive_thread = threading.Thread(target=self.client_receive, args=())
            receive_thread.start()

        except Exception as e:
            print(f"Erreur de connexion: {e}")

    def client_send(self, message):
        try:
            self.socket.send(bytes(message,encoding="utf-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def client_send_json(self, json_message):
        try:
            self.socket.sendall(json.dumps(json_message).encode("UTF-8"))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message: {e}")

    def receive(self, buffer_size=1024):
        try:
            data = self.socket.recv(buffer_size)
            return data.decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
            return None

    def client_receive(self):
        while True:
            try:
                # Recevoir des données du serveur
                response = self.receive()
                if not response:
                    print("Connexion fermée par le serveur")
                    break

                dejsonified_data = None
                    # print(decoded_data)
                try:
                    dejsonified_data = json.loads(response)  # Convertit le JSON en dictionnaire pour pouvoir l'utiliser avec Python
                except:
                    print(f"Info : Non JSON data received.")

                # actions disponible pour le serveur 
                if dejsonified_data and dejsonified_data.get('action') == "accept_login":
                    messagebox.showinfo("Success", dejsonified_data.get('message'))
                
                if dejsonified_data and dejsonified_data.get('action') == "reject_login":
                    messagebox.showerror("Error", dejsonified_data.get('message'))

                print(f"Réponse du serveur: {response}")
            except ConnectionResetError:
                print("Connexion réinitialisée par le serveur")
                break

    def close(self):
        try:
            self.socket.close()
            print("Connexion fermée")
        except Exception as e:
            print(f"Erreur lors de la fermeture de la connexion: {e}")

    ## ========== FONCTIONS GESTION DES REQUETES VERS LE CLIENT 

    ## ========== FONCTIONS GESTION DES REQUETES DEPUIS LE CLIENT
    def client_login(self,username,password):
        data = {
            "action": "login",
            "username": username,
            "password": password
        }
        
        self.client_send_json(data)

