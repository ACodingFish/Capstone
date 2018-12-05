import os
import sys
from PI_XBSerCli import *


IP_ADDR = raw_input("Input IP Address: ")
PORT = input("Input Port Number: ")
COM_ARD = raw_input("Input Arduino Serial Port: ")
BAUD_RATE_ARD = input("Input Arduino Baud Rate: ")
COM_XB = raw_input("Input XBee Serial Port: ")
BAUD_RATE_XB = input("Input XBee Baud Rate: ")

xb_serial_client = PI_XBSerCli(IP_ADDR, PORT, COM_ARD, BAUD_RATE_ARD, COM_XB, BAUD_RATE_XB)

while True:
    pass