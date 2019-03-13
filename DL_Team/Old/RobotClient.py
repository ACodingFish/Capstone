#!/usr/bin/python3
#Server program
import sys
import os
from PI_Cli import *

num_args = len(sys.argv)
if (num_args >3):
    print ("Too many command line args.")
    exit();

port = 10001
ip_addr = "127.0.0.1"

if (num_args == 3):
    try:
        ip_addr = sys.argv[1]
        port = int(sys.argv[2])
    except:
        pass

cli = PI_Cli(ip_addr, port, True)

while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    cli.Send_Msg(key_msg)