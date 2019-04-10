#!/usr/bin/python3
#Server program
import sys
import os
from PI_Cli import *
from PI_Conf import *

conf = PI_Conf("conf/cli3.conf")
ip_addr = conf.data[Params.IP_ADDR]
port = int(conf.data[Params.PORT])
encryption = (conf.data[Params.ENCRYPTION] == "1")
cli_id = conf.data[Params.ID]
auth = (conf.data[Params.AUTHENTICATION] == "1")

cli = PI_Cli(ip_addr, port, encryption, auth, cli_id)
print("Client -- " + cli_id + " -- online.")

while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    elif (key_msg[:4].lower() == "recv"):
        msg = cli.Recv_Msg()
        if (len(msg) > 0):
            print(msg)
        else:
            print("NO")
    else:
        cli.Send_Msg(key_msg)
