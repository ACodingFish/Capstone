import os
import sys
from PI_XBEE import *
from SMonitor import *

xb_comm = PI_XBEE('/dev/ttyAMA0')
monitor = SMonitor(3)

while True:
    average = monitor.monitor_thread()
    if average <= 5: 
        xb_comm.send_msg(average)
    