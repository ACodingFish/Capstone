#Server program - Loosely based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/
import socket
import select
import sys
import os
import traceback
from PI_RSA import *
from PI_AES import *
from PI_ClientManager import *

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

#   This class is a socket server implementation designed to be used with encryption
class PI_Srvr:
    #   Initializes the server on localhost
    #   Requires an input of port number
    #   Has an optional encryption flag that defaults to true.
    def __init__(self, port_num, is_encrypted=True, use_auth=True, auth_name=""):
        self.encrypted = is_encrypted
        self.RSA = PI_RSA()
        self.AES_KEYS = PI_KEY_AES()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port_num
        self.max_num_connections = 20
        self.clients_list = []

        #authentication (client names)
        self.cli_manager = PI_ClientManager()
        self.auth = use_auth
        if (self.auth == True):
            self.encrypt = True
        self.name = auth_name


        self.max_msg_size = 2048
        #ip_addr = str(sys.argv[1])
        self.server.bind(('',self.port)) #was ip_addr #localhost
        self.server.listen(self.max_num_connections)

        print("<Server Is Running>")# On: " + ip_addr)
        #start_new_thread(menu_thread,())
        start_new_thread(self.listening_thread,())

    #   This thread manages the communication with attached clients
    #   Each client has its own dedicated thread
    #   Takes in parameters of a client and its address
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
                        if (self.auth == True):
                            msg_data = message.split(':')
                            if (msg_data[0]== "ALL"): #if the target is all
                                self.relay_all(msg_data[1] + ":" + msg_data[2],client) #send client id and msg
                            else:
                                client_names = msg_data[0].split(",")
                                for client_name in client_names:
                                    target_clients = self.cli_manager.search(client_name)
                                    for tg in target_clients: #for each client with that name
                                        self.send_msg(msg_data[1] + ":" + msg_data[2],tg) #send to each intended client
                        else:
                            self.relay_all(message,client)
                else:
                    self.remove(client)
                    thread_open = False
            except Exception as e:
                #print(e)
                self.remove(client)
                thread_open = False
                continue

    #   This function relays a message received by a source client to every other client
    #   It takes parameters of a message and a source client (who sent the message)
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

    #   This function sends a message to a specific client
    #   It takes in parameters of a message and a target client
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

    #   Removes a client from the client list
    #   Takes in a parameter of a client
    def remove(self, old_client):
        old_client.close()
        if old_client in self.clients_list:
            self.clients_list.remove(old_client)
            if (self.encrypted == True):
                self.AES_KEYS.remove(old_client)
            if (self.auth == True):
                cli = self.cli_manager.remove(old_client)
                print("Client", cli, "Disconnected")
            else:
                print("Client Removed")
                #self.cli_manager.p_all()

    #   Opens up a thread that looks for new clients attempting to establish a connection
    #   Starts a thread to manage new client connections
    def listening_thread(self):
        try:
            while True:
                client, addr = self.server.accept()
                self.clients_list.append(client)
                print (addr[0] + " connected")
                if (self.encrypted == True)or(self.auth == True):
                    start_new_thread(self.init_client_thread,(client,addr))
                else:
                    start_new_thread(self.client_thread,(client,addr))
        except:
            print("server_closed.")

    #   Manages the client connection before allowing them to communicate (ENCRYPTION ONLY)
    #   Takes in parameters of a client and an address
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
                            if (self.auth == True):
                                message = client.recv(self.max_msg_size)
                                cli_name = cli_AES.decrypt(message)
                                self.cli_manager.add(cli_name,client)
                                self.send_msg(self.name, client)
                                print("Client",cli_name,"Has Been Verified.")

                            connected = True
                            #print(aes_key)

                    if connected == True:
                        if (self.auth == False):
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

    #   Closes the server.
    def close_server(self):
        self.server.close()
