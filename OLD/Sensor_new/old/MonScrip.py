import sys
import os
from SMonitor import *

max_length = 3
monitor = SMonitor(max_length)
philactory = SMonitor(max_length)
p = SMonitor(max_length)

while True:
    distance = monitor.get_avg()
    pressure = philactory.psr_avg()
    #print(distance)
    #print(pressure)
    time.sleep(0.1)


    
    