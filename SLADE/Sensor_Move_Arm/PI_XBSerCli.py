#Client program
import socket
import select
import sys
import os
import serial
import time

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *
    
from PI_XBEE import *

class PI_XBSerCli:
    def __init__(self, ip_addr, port, ard_com_port, ard_baud_rate, xb_com_port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.max_msg_size = 2048
        try:
            self.server.connect((ip_addr,port))
        except:
            print("Failed to connect to server")
            os._exit(0)
            
        try:
            self.ser = serial.Serial(ard_com_port, ard_baud_rate)  
            #115200 baud rate, could start with 9600   
            #'/dev/ttyACM0'
        except:
            print("Failed to connect serially")
            os._exit(0)
        
        #XBee init values
        self.xb_comm = PI_XBEE(xb_com_port)
        self.xb_sleep_time = 1
        self.xb_min_dist = 5.0
        self.GO_HOME = "85a, 35b, 120c, 115d"
        self.LOCKOUT = false
            
        self.in_net_msg = ""
        self.in_ser_msg = ""
        self.out_msg = ""
        
        start_new_thread(self.XB_Thread, ())
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
                    #put check for xb data here
                    if (self.LOCKOUT == False):
                        self.serial_write(self.in_net_msg)
                        print("LOCKOUT")
                    print(self.in_net_msg)
    
    #temporary thread - to be removed in later development
    def XB_Thread(self):
        while True:
            self.LOCKOUT = False
            data = self.xb_comm.get_msg()
            if (len(data) > 0):
                average = float(data)
                if (average <= self.xb_min_dist):
                    self.serial_write(self.GO_HOME)
                    self.Send_Msg("Robot Went Home")
                    self.LOCKOUT = True;
                    time.sleep(1)
                    
            
            
                    
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
            #print(self.in_ser_msg)