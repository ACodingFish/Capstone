import serial
import sys
import os
from xbee import DigiMesh
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_XBEE:
    def __init__(self, com_port):
        self.ser = serial.Serial(com_port, 9600)
        self.zb = DigiMesh(self.ser)
        start_new_thread(self.recv_thread,())
        self.data = ""
        self.i = 0
        
    def recv_thread(self):
        #while True:
        incoming = self.zb.wait_read_frame()
        self.data = incoming.get('data').decode("utf-8")
        print(self.data)
            
    def send_msg(self, message):
        #sending code
        self.zb.send("tx", id = b'\x10', frame_id = b'\x00', \
                     dest_addr = b'\x00\x13\xA2\x00\x41\x54\xF3\xFF', \
                     reserved = b'\xFF\xFE', broadcast_radius = b'\x00', \
                     options = b'\x00', data = str(message))
                     
    def get_msg(self):
        return self.data
