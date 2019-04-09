import time
import math
from PI_ADC import *

adc = PI_ADC_MONITOR()

while True:
    for i in range(adc.num_channels):
        print("ADC:",i)
        print("Value:",round(adc.get_adc_avg(i),2))
        if (adc.channel_triggered(i)):
            print("Stop Squeezin")
            
        
        time.sleep(0.3)
        
while True:
    sonar_bool = False
    for i in range(sonar.num_channels):
        if (sonar.channel_triggered(i)):
            sonar_bool = True
    if (sonar_bool == True):
        self.parse("obst")
    else:
        self.parse("obcl")