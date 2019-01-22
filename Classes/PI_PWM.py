# PWM program based on example found at https://circuitdigest.com/microcontroller-projects/raspberry-pi-pwm-tutorial


import RPi.GPIO as IO           #calling header file which helps us use GPIO’s of PI
from _thread import *

import time                     #calling time to provide delays in program

class PI_PWM:
    def __init__(self, pin, DC, Freq):
        self.pin = pin
        self.DC = DC
        if (self.Freq < 1.0):
            self.Freq = 1.0
        else:
            self.Freq = Freq
            
        period = (1/self.Freq)
        self.on_period = period*(self.DC/100)
        self.off_period = period*(1-(self.DC/100))
        
        self.PWM_ACTIVE = False
        IO.setwarnings(False) 
        IO.setmode (IO.BCM)
        IO.setup(self.pin,IO.OUT)
        start_new_thread(self.monitor_pwm,())
        
        
    def start_pwm(self):
        self.PWM_ACTIVE = True
        
    def start_pwm(self, DC, Freq):
        self.DC = DC
        if (self.Freq < 1.0):
            self.Freq = 1.0
        else:
            self.Freq = Freq
        self.update_period()
        self.PWM_ACTIVE = True
        
    def update_period(self):
        period = (1/self.Freq)
        self.on_period = period*(self.DC/100)
        self.off_period = period*(1-(self.DC/100))
        
    def set_dc(self, DC):
        self.DC = DC
        self.update_period()
        
    def set_freq(self, Freq):
        if (self.Freq < 1.0):
            self.Freq = 1.0
        else:
            self.Freq = Freq
        self.update_period()
        
    def stop_pwm(self)
        self.PWM_ACTIVE = False
        
    def monitor_pwm(self)
        while True:
            self.update_period()    # Update after toggle
            while self.PWM_ACTIVE:
                IO.output(self.pin, 0)
                time.sleep(self.off_period)
                IO.output(self.pin, 1)
                time.sleep(self.on_period)
                
            IO.output(self.pin, 0)  # Turn off when not using
            while (self.PWM_ACTIVE == False):
                pass
                