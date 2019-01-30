import sys
import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16) #creates the serevokit class with channels set to 16
#kit.servo[0].set_pulse_width_range(1000, 2000) #to change pulse width range
#kit.servo[0].actuation_range = 160 # to set actuation range

kit.servo[0].actuation_range = 120
num_args = len(sys.argv)
if (num_args == 2):
    kit.servo[0].angle = int(sys.argv[1]) #move hat 0 to 180 degrees.
    
time.sleep(1.5)
print("FIN!")
time.sleep(0.5)