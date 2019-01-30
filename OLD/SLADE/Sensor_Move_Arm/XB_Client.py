import os
import sys
from PI_XBSerCli import *


if sys.version_info[0] == 3:
    IP_ADDR = input("Input IP Address: ")
    PORT = int(input("Input Port Number: "))
    COM_ARD = input("Input Arduino Serial Port: ")
    BAUD_RATE_ARD = int(input("Input Arduino Baud Rate: "))
    COM_XB = input("Input XBee Serial Port: ")
else:
    IP_ADDR = raw_input("Input IP Address: ")
    PORT = input("Input Port Number: ")
    COM_ARD = raw_input("Input Arduino Serial Port: ")
    BAUD_RATE_ARD = input("Input Arduino Baud Rate: ")
    COM_XB = raw_input("Input XBee Serial Port: ")


xb_serial_client = PI_XBSerCli(IP_ADDR, PORT, COM_ARD, BAUD_RATE_ARD, COM_XB)

while True:
    pass