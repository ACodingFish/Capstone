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

class Serial_ARD:
    def __init__(self, baud_rate)
        #use "ls /dev/tty*" to find com port
        self.ser = serial.Serial('/dev/ttyACM0',baud_rate)  #115200 baud rate, could start with 9600
        #will need to change into reading and writing on separate threads
        start_new_thread(self.serial_read_thread,())
        self.in_msg = ""
        self.out_msg = ""
        
    def serial_read_thread(self):
        while True:
            self.in_msg = self.ser.read().decode('utf-8')
            print(self.in_msg)
                
    def serial_write(self, msg):
            self.out_msg = msg
            self.ser.write(msg.encode('utf-8'))


