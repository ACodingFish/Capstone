#Client program - Based on chatroom program
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

class PI_Cli:
    def __init__(self, ip_addr, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.max_msg_size = 2048
        try:
            self.server.connect((ip_addr,port))
        except:
            print("Failed to connect")
            os._exit(0)
            
        self.in_msg = ""
        self.out_msg = ""
        self.sockets_list = [self.server]
        self.read_sockets, self.write_sockets, self.error_sockets = select.select(self.sockets_list,self.sockets_list,[])
        
        start_new_thread(self.Recv_Thread,())
        #start_new_thread(self.Send_Thread,())

    def Recv_Thread(self):
        while True:
            for socks in self.read_sockets:
                if socks == self.server:
                    self.in_msg = socks.recv(self.max_msg_size).decode('utf-8')
                    print(self.in_msg)
                    
    def Send_Msg(self, message):
        for socks in self.write_sockets:
                if socks == self.server:
                    self.out_msg = message
                    self.server.send(self.out_msg.encode('utf-8'))