import sys
import os
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
trig = 23
echo = 24
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *#Server program

class SMonitor:
    def __init__(self, max_length):
        if (max_length < 1):
            max_length = 1
        self.length = 0
        self.max_length = 1 #max_length
        self.avg_arr = []
        self.avg = 0
        start_new_thread(self.monitor_thread, ())
        #Configure GPIO pins
        GPIO.setup(trig,GPIO.OUT)
        GPIO.setup(echo,GPIO.IN)
        GPIO.output(trig,False)
        self.count = 0
            
    def get_elem(self):
        #get some stuff
        while GPIO.input(echo) == 0:
            pulse_start = time.time() #Records the start time of the pulse

        while GPIO.input(echo) == 1:
            pulse_end = time.time() #Records the end time of the pulse

        pulse_duration = pulse_end - pulse_start #Calculates pulse time

        #Speed of sound at sea level is 343m/s
        #Speed = Distance/Time
        #34300/2 = Distance/(Time/2) because we only need the one way distance
        distance = pulse_duration * 17150.0 #Final formula for getting distance
        distance = round(distance,2)
        return distance
        
    def monitor_thread(self):
        while True:
            time.sleep(0.1) #Delay between detections
            GPIO.output(trig,True)
            time.sleep(0.00001) #Pulse time = 10us
            GPIO.output(trig,False)
            new_element = self.get_elem()
            if self.length < self.max_length:
                self.length = self.length + 1
                self.avg_arr.append(new_element) # appends new elements
            else:
                #shift every array elem down 1 and remove oldest
                #put in new elem
                self.avg_arr.pop(0) # shifts all elements left
                self.avg_arr.append(new_element) # appends new element
            self.avg = sum(self.avg_arr)/self.length
            #print(self.avg)
            #return self.avg
            
    def get_avg(self):
        # compute average
        if (self.count >= 20):
            os.system('clear')
            self.count = 0
        else:
            self.count += 1
        print("Measured Value: %(avg)d" % {"avg": self.avg} )
        return self.avg
