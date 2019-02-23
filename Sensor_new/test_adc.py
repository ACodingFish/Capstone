import time
import math
from PI_ADC import *

adc = PI_ADC_MONITOR()

while True:
    for i in range(adc.num_channels):
        max_val = 1
        print("ADC:",i)
        print("Value:",round(adc.get_adc_avg(i),2))
        if (adc.channel_triggered(i)):
            print("Stop Squeezin")
            
        
        time.sleep(0.3)