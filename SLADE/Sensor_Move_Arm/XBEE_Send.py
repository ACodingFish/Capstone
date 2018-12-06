import os
import sys
import time
from PI_XBEE import *
from SMonitor import *

xb_comm = PI_XBEE('/dev/ttyAMA0')
monitor = SMonitor(3)

while True:
    time.sleep(.2)
    average = monitor.get_avg()
    xb_comm.send_msg(average)
    