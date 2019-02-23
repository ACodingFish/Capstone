import sys
import os
from SMonitor import *

max_length = 3
monitor = SMonitor(max_length)
p = SMonitor(max_length)

while True:
    distance = monitor.get_avg()
    print(distance)
    
    pressure = p.psr_avg()
    print(pressure)
    time.sleep(0.1)


    
    