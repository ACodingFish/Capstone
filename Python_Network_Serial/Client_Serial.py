#Client program - Based on chatroom program
#Example found at:
#www.geeksforgeeks.org/simple-chat-room-using-python/amp/
# Based on
# https://www.instructables.com/id/Raspberry-Pi-Arduino-Serial-Communication/
# and
# https://classes.engineering.wustl.edu/ese205/core/index.php?title=Serial_Communication_between_Raspberry_Pi_%26_Arduino
# and
# https://stackoverflow.com/questions/13017840/using-pyserial-is-it-possble-to-wait-for-data
import socket
import select
import sys
import os
import serial

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
num_args = len(sys.argv)
if (num_args !=3):
    print("Missing Or Too Many Command Line Args")
    exit();

max_msg_size = 2048

ip_addr = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((ip_addr,port))
in_msg = ""
out_msg = ""
key_msg = ""

def Recv_Thread():
    while True:
        sockets_list = [server]#[sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(sockets_list,sockets_list,[])

        for socks in read_sockets:
            if socks == server:
                in_msg = socks.recv(max_msg_size).decode('utf-8')
                Lib_Serial.serial_write(in_msg)
                print(in_msg)

def Send_Thread():
    while True:
        sockets_list = [server]#[sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(sockets_list,sockets_list,[])
        for socks in write_socket:
            if socks == server:
                key_msg = sys.stdin.readline()
                if (key_msg[:4].lower() == "exit"):
                    os._exit(0)
                out_msg = key_msg
                server.send(out_msg.encode('utf-8'))
                #   sys.stdout.write("<localhost>")
                #   sys.stdout.write(out_msg)
                #   sys.stdout.flush()

ser = serial.Serial(com_port,baud_rate)  #115200 baud rate, could start with 9600    
#use "ls /dev/tty*" to find com port
s = [0,1]
start_new_thread(serial_read_thread,(ser))

def serial_read_thread():
    while True:
        in_msg = ser.read().decode('utf-8')
        print(in_msg)
        
def serial_write(out_msg):
    ser.write(out_msg.encode('utf-8'))                
           
Lib_Serial.init_Serial('/dev/ttyACM0',9600)
start_new_thread(serial_read_thread, ())
start_new_thread(Recv_Thread,())
start_new_thread(Send_Thread,())


while True:
    pass
            
close()
                

