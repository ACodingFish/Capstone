#Server program - Based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/
import socket
import select
import sys
import os
import Logging
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
num_args = len(sys.argv)
if (num_args !=2):
    print ("Missing Or Too Many Command Line Args")
    exit();

num_allowable_connections = 20
clients_list = []
max_msg_size = 2048

#   Logging
print("<Logging Has Started>")

#ip_addr = str(sys.argv[1])
port = int(sys.argv[1])
server.bind(('',port)) #was ip_addr
server.listen(num_allowable_connections)

def menu_thread():
    while True:
        key_msg = sys.stdin.readline()
        if (key_msg[:4].lower() == "exit"):
            os._exit(0)

def client_thread(client, addr):
    client.send("You are now connected.".encode('utf-8'))
    while True:
        try:
            message = client.recv(max_msg_size).decode('utf-8')
            if message:
                if (len(message) > 0):
                    recvd_msg = message
                    print(recvd_msg)
                    Logging.log_message(recvd_msg)
                    relay_all(recvd_msg.encode('utf-8'),client)
            
            else:
                remove(client)
        
        except:
            continue

def relay_all(message, source_client):
    for clients in clients_list:
        if (clients!=source_client):
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(old_client):
    if old_client in clients_list:
        clients_list.remove(old_client)

print("<Server Is Running>")# On: " + ip_addr)
start_new_thread(menu_thread,())




while True:
    client, addr = server.accept()
    clients_list.append(client)
    print (addr[0] + " connected")
    start_new_thread(client_thread,(client,addr))

client.close()
server.close()
