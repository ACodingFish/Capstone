#Client program - Based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/
import socket
import select
import sys
import os
import serial

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_SerCli:
    def __init__(self, ip_addr, port, baud_rate):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.max_msg_size = 2048
        try:
            self.server.connect((ip_addr,port))
        except:
            print("Failed to connect to server")
            os._exit(0)
            
        try:
            self.ser = serial.Serial('/dev/ttyACM0',baud_rate)  #115200 baud rate, could start with 9600   
        except:
            print("Failed to connect serially")
            os._exit(0)
            
        self.in_net_msg = ""
        self.in_ser_msg = ""
        self.out_msg = ""
        
        start_new_thread(self.Recv_Thread,())
        #start_new_thread(self.Send_Thread,())
        start_new_thread(self.serial_read_thread, ())

    def Recv_Thread(self):
        while True:
            sockets_list = [self.server]
            read_sockets, write_sockets, error_sockets = select.select(sockets_list,sockets_list,[])
            for socks in read_sockets:
                if socks == self.server:
                    self.in_net_msg = socks.recv(self.max_msg_size).decode('utf-8')
                    self.serial_write(in_net_msg)
                    print(self.in_net_msg)
                    
    def Send_Msg(self, message):
        sockets_list = [self.server]
        read_sockets, write_sockets, error_sockets = select.select(sockets_list,sockets_list,[])
        for socks in write_sockets:
                if socks == self.server:
                    self.out_msg = message
                    self.server.send(self.out_msg.encode('utf-8'))
                    
    def serial_write(self, msg):
        self.ser.write(msg.encode('utf-8'))   
        
    def serial_read_thread(self):
        while True:
            self.in_ser_msg = self.ser.read().decode('utf-8')
            print(in_ser_msg)