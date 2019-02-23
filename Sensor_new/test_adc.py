import time
from PI_ADC import *

adc = PI_ADC_MONITOR()

while True:
    for i in range(adc.num_channels):
        print("ADC:",i)
        print("Value:",adc.get_adc_avg(i))
        time.sleep(0.3)