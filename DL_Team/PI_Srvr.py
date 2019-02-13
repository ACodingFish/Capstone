#Server program - Based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/
import socket
import select
import sys
import os
import traceback
from PI_RSA import *
from PI_AES import *

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *
    
class PI_Srvr:
    def __init__(self, port_num, is_encrypted=True):
        self.encrypted = is_encrypted
        self.RSA = PI_RSA()
        self.AES_KEYS = PI_KEY_AES()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port_num
        self.max_num_connections = 20
        self.clients_list = []
        
        self.max_msg_size = 2048
        #ip_addr = str(sys.argv[1])
        self.server.bind(('',self.port)) #was ip_addr #localhost
        self.server.listen(self.max_num_connections)
        
        print("<Server Is Running>")# On: " + ip_addr)
        #start_new_thread(menu_thread,())
        start_new_thread(self.listening_thread,())

    def client_thread(self, client, addr):
        thread_open = True
        #client.send("You are now connected.".encode('utf-8'))
        if (self.encrypted == True):
            aes_key = self.AES_KEYS.get_key(client)
            aes = PI_AES(aes_key)
        while thread_open == True:
            try:
                message = client.recv(self.max_msg_size)
                if (self.encrypted == True):
                    message = aes.decrypt(message)
                
                if type(message) != str:
                    message = message.decode('utf-8')
                if message:
                    if (len(message) > 0):
                        print(message)
                        self.relay_all(message,client)
                else:
                    self.remove(client)
                    thread_open = False
            except Exception as e:
                print(e)
                self.remove(client)
                thread_open = False
                continue

    def relay_all(self, message, source_client):
        for clients in self.clients_list:
            if (clients!=source_client):
                try:
                    if (type(message) != bytes):
                        message = message.encode('utf-8')
                    if (self.encrypted == True):
                        if (type(self.AES_KEYS.get_key(clients)) != bool):
                            self.send_msg(message, clients)
                    else:
                        self.send_msg(message, clients)
                except:
                    self.remove(clients)
                    
    def send_msg(self, message, client):
        try:
            if (type(message) != bytes):
                message = message.encode('utf-8')
            if (self.encrypted == True):
                aes_key = self.AES_KEYS.get_key(client)
                if (type(aes_key) != bool):
                    aes = PI_AES(aes_key)
                    message = aes.encrypt(message)
            client.send(message)
        except:
            self.remove(client)
                    

    def remove(self, old_client):
        print("Removing Client")
        old_client.close()
        if old_client in self.clients_list:
            self.clients_list.remove(old_client)
            if (self.encrypted == True):
                self.AES_KEYS.remove(old_client)
            
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
            thread_open = True
            while (connected == False) and (thread_open == True):
                try:
                    message = client.recv(self.max_msg_size) #get rsa key from client
                
                    if message:
                        if (len(message) > 0):
                            #message = self.RSA.decrypt(message)
                            cli_RSA = PI_RSA_SN(message)
                            #print(message)
                            cli_AES = PI_AES()
                            aes_key = cli_AES.get_key()#"AES KEY" #woo!
                            key_msg = cli_RSA.encrypt(aes_key)
                            self.send_msg(key_msg, client)
                            self.AES_KEYS.add(client, aes_key)
                            connected = True
                            #print(aes_key)
                        
                    if connected == True:
                        print("Client Verification Successful.")
                        start_new_thread(self.client_thread,(client,addr))
                    else:
                        thread_open = False
                        self.remove(client)
                except Exception as e:
                    print(e)
                    #traceback.print_exc()
                    self.remove(client)
                    thread_open = False
        else:
            start_new_thread(self.client_thread,(client,addr))
        
    def close_server(self):
        self.server.close()

