#Server program - Based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/
import socket
import select
import sys
import os
import traceback
from PI_RSA import *

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_Srvr:
    def __init__(self, port_num):
        self.encrypted = True
        if (self.encrypted == True):
            self.RSA = PI_RSA()
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
                        self.relay_all(message,client)
                else:
                    self.remove(client)
            except:
                continue

    def relay_all(self, message, source_client):
        for clients in self.clients_list:
            if (clients!=source_client):
                try:
                    if (type(message) != bytes):
                        message = message.encode('utf-8')
                    clients.send(message)
                except:
                    clients.close()
                    self.remove(clients)
                    
    def send_msg(self, message, client):
        for clients in self.clients_list:
            if (clients==client):
                try:
                    if (type(message) != bytes):
                        message = message.encode('utf-8')
                    client.send(message)
                except:
                    client.close()
                    self.remove(client)
                    

    def remove(self, old_client):
        if old_client in self.clients_list:
            self.clients_list.remove(old_client)
            
    def listening_thread(self):
        try:
            while True:
                client, addr = self.server.accept()
                self.clients_list.append(client)
                print (addr[0] + " connected")
                if (self.encrypted == True):
                    start_new_thread(self.init_client_thread,(client,addr))
                else:
                    start_new_thread(self.client_thread,(client,addr))
        except:
            print("server_closed.")
            
    def init_client_thread(self, client, addr):
        if (self.encrypted == True):
            connected = False
            self.send_msg(self.RSA.get_public(), client) #send rsa key string
            while connected == False:
                try:
                    message = client.recv(self.max_msg_size) #get rsa key from client
                
                    if message:
                        if (len(message) > 0):
                            #message = self.RSA.decrypt(message)
                            print(message)
                            cli_rsa = PI_RSA_SN(message)
                            print("before before")
                            if (cli_rsa.initialized == True):
                                aes_key = "AES KEY" #woo!
                                print("before")
                                key_msg = cli_rsa.encrypt(aes_key)
                                self.send_msg(key_msg, client)
                                connected = True
                                print(aes_key)
                            else:
                                print("INVALID CLIENT KEY.")
                                self.remove(client)
                        
                    if connected == True:
                        start_new_thread(self.client_thread,(client,addr))
                    else:
                        self.remove(client)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    continue
        else:
            start_new_thread(self.client_thread,(client,addr))
        
    def close_server(self):
        self.server.close()

