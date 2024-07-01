# main.py
from client import *
from interface import * 


client = SSLClient("localhost",8888)
client.start()
client.interface = ChatInterface(client)
client.interface.start()

 