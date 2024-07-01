# main.py
from client import *
from interface import * 


client = SSLClient("127.0.0.1",8888)
client.start()
client.interface = ChatInterface(client)
client.interface.start()

