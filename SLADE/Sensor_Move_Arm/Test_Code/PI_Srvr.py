#Server program - Based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/
import socket
import select
import sys
import os
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_Srvr:
    def __init__(self, port_num):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port_num
        self.max_num_connections = 20
        self.clients_list = []
        self.max_msg_size = 2048
        #ip_addr = str(sys.argv[1])
        self.server.bind(('',self.port)) #was ip_addr
        self.server.listen(self.max_num_connections)
        
        print("<Server Is Running>")# On: " + ip_addr)
        #start_new_thread(menu_thread,())
        start_new_thread(self.listening_thread,())

    def client_thread(self, client, addr):
        #client.send("You are now connected.".encode('utf-8'))
        while True:
            try:
                message = client.recv(self.max_msg_size).decode('utf-8')
                if message:
                    if (len(message) > 0):
                        print(message)
                        self.relay_all(message.encode('utf-8'),client)
                else:
                    self.remove(client)
            except:
                continue

    def relay_all(self, message, source_client):
        for clients in self.clients_list:
            if (clients!=source_client):
                try:
                    clients.send(message)
                except:
                    clients.close()
                    self.remove(clients)

    def remove(self, old_client):
        if old_client in self.clients_list:
            self.clients_list.remove(old_client)
            
    def listening_thread(self):
        try:
            while True:
                client, addr = self.server.accept()
                self.clients_list.append(client)
                print (addr[0] + " connected")
                start_new_thread(self.client_thread,(client,addr))
        except:
            print("server_closed.")
        
    def close_server(self):
        self.server.close()

