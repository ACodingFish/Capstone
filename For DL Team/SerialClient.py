#Server program
import sys
import os
from PI_SerCli import *

num_args = len(sys.argv)
if (num_args >4):
    print ("Too many command line args.")
    exit();

port = 10001
ip_addr = "127.0.0.1"
baud_rate = 9600

if (num_args == 4):
    try:
        ip_addr = sys.argv[1]
        port = int(sys.argv[2])
        baud_rate = int(sys.argv[3])
    except:
        pass

cli = PI_SerCli(ip_addr, port, baud_rate)

while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    cli.Send_Msg(key_msg)