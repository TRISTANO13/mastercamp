# main.py
from client import *
from interface import * 

if __name__ == "__main__":
    try:
        client = SSLClient("0.0.0.0",8888)
        client.start()
        
    except Exception as e :
            print("Erreur lors de la connexion au serveur.")
            print("\n",e);

    else:
            print("Vous êtes connecté au serveur.")
            print("Lancement de l'interface...")
            client.interface = ChatInterface(client)
            client.interface.start()

