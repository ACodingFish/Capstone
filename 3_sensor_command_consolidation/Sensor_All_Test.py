import time
import math
import os
from PI_ADC import *
from PI_Sonar import *

sonar = PI_Sonar_Monitor()

adc = PI_ADC_MONITOR()

while True:
    os.system('clear')
    for i in range(adc.num_channels):
        print("ADC:",i, "Value:",round(adc.get_adc_avg(i),2))
    
    for i in range(sonar.num_sensors):
        print("Sonar: ", i, "Average: ", round(sonar.get_avg(i),2))
        #print("State ", sonar.sensor_list[i].state)
    
    time.sleep(1.0)
