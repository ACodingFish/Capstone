# Based on
# https://www.instructables.com/id/Raspberry-Pi-Arduino-Serial-Communication/
# and
# https://classes.engineering.wustl.edu/ese205/core/index.php?title=Serial_Communication_between_Raspberry_Pi_%26_Arduino
# and
# https://stackoverflow.com/questions/13017840/using-pyserial-is-it-possble-to-wait-for-data

import serial
import sys
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

ser = serial.Serial(None,0)

def init_Serial(com_port, baud_rate):
    #use "ls /dev/tty*" to find com port
    ser = serial.Serial(com_port,baud_rate)  #115200 baud rate, could start with 9600
    s = [0,1]
    start_new_thread(serial_read_thread,())

def serial_read_thread():
    while True:
        in_msg = ser.read().decode('utf-8')
        print(in_msg)
        
def serial_write(out_msg):
    ser.write(out_msg.encode('utf-8'))

