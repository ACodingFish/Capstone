# PWM program based on example found at https://circuitdigest.com/microcontroller-projects/raspberry-pi-pwm-tutorial


import RPi.GPIO as IO           #calling header file which helps us use GPIO’s of PI
from _thread import *

import time                     #calling time to provide delays in program

IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BCM)             #we are programming the GPIO by BCM pin numbers. (PIN15 as ‘GPIO22’)

IO.setup(22,IO.OUT)             # initialize GPIO22 as an output.
IO.setup(27,IO.OUT)
IO.setup(17,IO.OUT)
IO.setup(4,IO.OUT)  

#p = IO.PWM(22,20000)             #GPIO22 as PWM output, with 100Hz frequency
#p.start(10)                     #generate PWM signal with 10% duty cycle

def start_pwm(pin, DC, Freq):
    period = (1/Freq)
    on_period = period*(DC/100)
    off_period = period*(1-(DC/100))
    while True:
        IO.output(pin, 0)
        time.sleep(off_period)
        IO.output(pin, 1)
        time.sleep(on_period)
        
start_new_thread(start_pwm,(22, 10, 50))
start_new_thread(start_pwm,(27, 10, 50))
start_new_thread(start_pwm,(17, 10, 50))
start_new_thread(start_pwm,(4, 10, 50))

#while True:
#    IO.output(22,0)
#    time.sleep(0.018)
#    IO.output(22,1)
#    time.sleep(0.002)
