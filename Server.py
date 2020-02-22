from socket import AF_INET, socket, SOCK_STREAM #AF_INET and SOCK_STREAM are for TCP
from threading import Thread
import time

clients = {}
addresses = {}
freeClients = []

HOST = "192.168.1.169"
PORT = 33500
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def incommingConnections():
       while True:
              client, client_address = SERVER.accept()
              print("%s:%s has connected." % client_address)
              client.send(bytes("Greetings from the cave!"+
                          "Now type your name and press enter!", "utf8"))
              addresses[client] = client_address
              Thread(target=handle_client, args=(client,)).start()

def freeClient():
       question = "please respond to this message with 'yes' if you are free to recive and new order"
       broadcast(bytes(question, "utf8"))
       
       


def handle_client(client):
       name = client.recv(BUFFERSIZE).decode("utf8")
       welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
       client.send(bytes(welcome, "utf8"))
       msg = "%s has joined the chat!" % name
       broadcast(bytes(msg, "utf8"))
       clients[client] = name
       while True:
              msg = client.recv(BUFFERSIZE)
              if msg != bytes("{quit}", "utf8"):
                     broadcast(msg, name+": ")
              else:
                     client.send(bytes("{quit}", "utf8"))
                     client.close()
                     del clients[client]
                     broadcast(bytes("%s has left the chat." % name, "utf8"))
              break

def orderInfomation():
       my_file = open("wabaki.txt", "r")
       text = my_file.readlines()
       textlength = len(text)
       print (text)
       print (textlength)
       for i in range (0,textlength):
              string = text[i]
              string = string.translate(None, "\nn")
              print (string)






def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=incommingConnections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
