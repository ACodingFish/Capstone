#Client program - Based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/

#requires installation of pycrypto (or pycryptodome)
#requires installation of adafruit servokit (adafruit-circuitpython-servokit)
import socket
import select
import sys
import os
import time
import traceback
from PI_RSA import *
from PI_AES import *
from PI_Servo import *

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_Cli:
    def __init__(self, ip_addr, port, is_robot=False, is_encrypted=True):
        self.encrypt = is_encrypted
        self.encrypted = False
        self.RSA = PI_RSA()
        #print(self.RSA.get_public())
        self.AES_key = 0
        self.AES = 0
        
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
        
        if (self.encrypt == True):
            start_new_thread(self.Init_Thread,())
        else:
            start_new_thread(self.Recv_Thread,())
        #start_new_thread(self.Send_Thread,())

    def Recv_Thread(self):
        try:
            while True:
                sockets_list = [self.server]
                read_sockets, write_sockets, error_sockets = select.select(sockets_list,sockets_list,[])
                for socks in read_sockets:
                    if socks == self.server:
                        self.in_msg = socks.recv(self.max_msg_size)
                        if (self.encrypt == True):
                            self.in_msg = self.AES.decrypt(self.in_msg)
                            if type(self.in_msg) != str:
                                self.in_msg = self.in_msg.decode('utf-8')
                        else:    
                            self.in_msg = self.in_msg.decode('utf-8')
                        if (self.is_robot == True):
                            self.servo_controller.parse(self.in_msg)
                        print(self.in_msg)
        except Exception as e:
            #print(e)
            print("Lost connection to Server.")
            os._exit(0)
            

    def Init_Thread(self):
        try:
        #time.sleep(.5)
            if (self.encrypt == True):
                connected = False

                while connected == False:
                    #self.Send_Msg(self.svr_RSA.encrypt(self.RSA.get_public()))
                    self.Send_Msg(self.RSA.get_public())
                    #print(self.RSA.get_public())
                    msg = self.server.recv(self.max_msg_size)
                    aes_key = self.RSA.decrypt(msg)
                    self.AES_key = aes_key
                    #print(aes_key) #AES KEY
                    connected = True
                    self.AES = PI_AES(self.AES_key)
                    self.encrypted = True
                    print("Server Verification Successful")
                    start_new_thread(self.Recv_Thread,())

            else:
                start_new_thread(self.Recv_Thread,())
        except Exception as e:
            #print(e)
            print("Lost connection to Server.")
            os._exit(0)
            
                    
    def Send_Msg(self, message):
        sockets_list = [self.server]
        read_sockets, write_sockets, error_sockets = select.select(sockets_list,sockets_list,[])
        for socks in write_sockets:
            if socks == self.server:
                if (type(message) != bytes):
                    message = message.encode('utf-8')
                if self.encrypted == True:
                    message = self.AES.encrypt(message)
                self.server.send(message)
                    