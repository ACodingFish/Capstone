#!/usr/bin/python3
#Server program
import sys
import os
#from PI_Cli import *
from PI_RobotManager import *

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

robot = PI_RobotManager(False, ip_addr, port)

while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    robot.parse(key_msg)