import os
import sys
from PI_XBEE import *
from SMonitor import *

xb_comm = PI_XBEE('/dev/ttyAMA0')
monitor = SMonitor(3)

while True:
    pass