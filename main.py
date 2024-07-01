# main.py
from client import *
from interface import * 


client = SSLClient("10.101.14.137",8888)
client.start()
client.interface = ChatInterface(client)
client.interface.start()

