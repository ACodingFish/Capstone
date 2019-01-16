# PWM program based on example found at https://circuitdigest.com/microcontroller-projects/raspberry-pi-pwm-tutorial


import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI

import time                            #calling time to provide delays in program

IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

IO.setup(15,IO.OUT)           # initialize GPIO19 as an output.

p = IO.PWM(15,100)          #GPIO19 as PWM output, with 100Hz frequency
p.start(10)                              #generate PWM signal with 0% duty cycle
