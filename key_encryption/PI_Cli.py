#Client program - Based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/
import socket
import select
import sys
import os
from PI_RSA import *
from PI_AES import *
from PI_Servo import *

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_Cli:
    def __init__(self, ip_addr, port, is_robot):
        self.encrypted = True
        if (self.encrypted == True):
            self.RSA = PI_RSA()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.max_msg_size = 2048
        try:
            self.server.connect((ip_addr,port))
        except:
            print("Failed to connect")
            os._exit(0)
            
        self.in_msg = ""
        
        self.is_robot = is_robot
        if (self.is_robot == True):
            self.servo_controller = PI_ServoController(16) # Start servo controller with 16 channels
        
        if (self.encrypted == True):
            start_new_thread(self.Init_Thread,())
        else:
            start_new_thread(self.Recv_Thread,())
        #start_new_thread(self.Send_Thread,())

    def Recv_Thread(self):
        while True:
            sockets_list = [self.server]
            read_sockets, write_sockets, error_sockets = select.select(sockets_list,sockets_list,[])
            for socks in read_sockets:
                if socks == self.server:
                    self.in_msg = socks.recv(self.max_msg_size).decode('utf-8')
                    if (self.is_robot == True):
                        self.servo_controller.parse(self.in_msg)
                    print(self.in_msg)
                    
    def Init_Thread(self):
        if (self.encrypted == True):
            connected = False
            enc = False
            while connected == False:
                sockets_list = [self.server]
                read_sockets, write_sockets, error_sockets = select.select(sockets_list, sockets_list,[])
                for socks in read_sockets:
                    if socks == self.server:
                        if enc == False:
                            message = socks.recv(self.max_msg_size).decode('utf-8')
                            self.svr_RSA = PI_RSA_SN(message) #could send that i am the robot?
                            if (self.svr_RSA.initialized == False):
                                print("INVALID SERVER KEY.")
                                os._exit(0)
                            #self.Send_Msg(self.svr_RSA.encrypt(self.RSA.get_public()))
                            self.Send_Msg(self.RSA.get_public())
                            enc = True
                        else:
                            msg = socks.recv(self.max_msg_size)
                            aes_key = self.RSA.decrypt(msg)
                            self.AES_key = aes_key
                            print(aes_key) #AES KEY
                            connected = True
                            start_new_thread(self.Recv_Thread,())
                        
            
        else:
            start_new_thread(self.Recv_Thread,())
                    
    def Send_Msg(self, message):
        sockets_list = [self.server]
        read_sockets, write_sockets, error_sockets = select.select(sockets_list,sockets_list,[])
        for socks in write_sockets:
            if socks == self.server:
                if (type(message) != bytes):
                    message = message.encode('utf-8')
                self.server.send(message)
                    