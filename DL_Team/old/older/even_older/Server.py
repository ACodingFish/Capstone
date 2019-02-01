#Server program
import sys
import os
from PI_Srvr import *

num_args = len(sys.argv)
if (num_args >2):
    print ("Too many command line args.")
    exit();

port = 10001

if (num_args == 2):
    try:
        port = int(sys.argv[1])
    except:
        pass
   
srvr = PI_Srvr(port)

while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)