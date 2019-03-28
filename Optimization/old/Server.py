#!/usr/bin/python3
#Server program
import sys
import os
from PI_Srvr import *
from PI_Conf import *

conf = PI_Conf("conf/srvr.conf")
local = (conf.data[Params.LOCAL] == "1")
ip_addr = conf.data[Params.IP_ADDR]
port = conf.data[Params.PORT]
encryption = (conf.data[Params.ENCRYPTION] == "1")
srvr_id = conf.data[Params.ID]


if (type(ip_addr) != str):
    ip_addr = str(ip_addr)
if (type(port) != int):
    port = int(port)
if (type(srvr_id) != str):
    srvr_id = str(srvr_id)
srvr = PI_Srvr(port)
print("Server -- " + srvr_id + " -- online.")

while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)