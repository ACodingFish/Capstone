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

#use "ls /dev/tty*" to find com port
ser = serial.Serial('/dev/ttyACM0',115200)  #115200 baud rate, could start with 9600
s = [0,1]
#will need to change into reading and writing on separate threads

def serial_read_thread():
    while True:
        in_msg = ser.read().decode('utf-8')
        print(in_msg)
            
def serial_write_thread():
    while True:
        key_msg = sys.stdin.readline()
        if (key_msg[:4].lower() == "exit"):
            os._exit(0)
        out_msg = key_msg
        ser.write(out_msg.encode('utf-8'))


start_new_thread(serial_read_thread,())
start_new_thread(serial_write_thread,())

while True:
    pass
	#read_serial=ser.readline()
	#s[0] = str(int (ser.readline(),16))
	#print s[0]
	#print read_serial