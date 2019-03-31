#!/usr/bin/python3
import time
import math
import sys
import os
import traceback
from PI_Cli import *
from PI_ADC import *

num_args = len(sys.argv)
if (num_args >3):
    print ("Too many command line args.")
    exit();

port = 10001
ip_addr = "127.0.0.1"

if (num_args == 3):
    try:
        ip_addr = sys.argv[1]
        port = int(sys.argv[2])
    except:
        pass
        
try:
    cli = PI_Cli(ip_addr, port)

    adc = PI_ADC_MONITOR()
    prev_triggered = False
    while True:
        is_triggered = False
        for i in range(adc.num_channels):
            print("ADC:",i)
            print("Value:",round(adc.get_adc_avg(i),2))
            if (adc.channel_triggered(i)):
                is_triggered=True
                #print("Stop Squeezin")
            time.sleep(0.3)
        if (is_triggered==False):
            if (prev_triggered==True): # to only send msg once
                cli.Send_Msg("obcl") #send obstacle cleared message
                prev_triggered=False
        else:
            if (prev_triggered==False):
                cli.Send_Msg("obst") #send obstacle message
                prev_triggered=True
                
except Exception as e:
    print(e)
    os._exit(0)