import sys
import os
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *      #Server program
    
class sonar
    def _init_(self, trig, echo, max_length)
        self.trig = trig
        self.echo = echo
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.output(self.trig,False)
        self.max_length = max_length
        avg_arr = []
    
    
class run_sonar
    def _init_(self)
        self.sensor_list = []
        # [[trigger pin, echo pin, num_avgs],....]
        sonar_info[[23,24,3],[5,6,3]]
        for sensor in sonar_info:
            self.add_sensor(sensor[0], sensor[1], sensor[2]) 
        start_new_thread(self.run_sonar_sensors_thread,())
        
        
    def add_sensor(self, trig, echo)
        new_sensor = sonar(trig, echo)
        self.sensor_list.append(new_sensor)
    
    def get_elem(self, index):
        #get some stuff
        while GPIO.input(self.sensor_list[index].echo) == 0:
            pulse_start = time.time() #Records the start time of the pulse

        while GPIO.input(self.sensor_list[index].echo) == 1:
            pulse_end = time.time() #Records the end time of the pulse

        pulse_duration = pulse_end - pulse_start #Calculates pulse time

        #Speed of sound at sea level is 343m/s
        #Speed = Distance/Time
        #34300/2 = Distance/(Time/2) because we only need the one way distance
        distance = pulse_duration * 17150.0 #Final formula for getting distance
        distance = round(distance,2)
        return distance
    
    def run_sonar_sensors_thread(self)
        while True:
            for i in range(len(self.sensor_list)):
                time.sleep(0.0001) #Delay between detections
                GPIO.output(self.sensor_list[i].trig,True)
                time.sleep(0.00001) #Pulse time = 10us
                GPIO.output(self.sensor_list[i].trig,False)
                new_element = self.get_elem(i)
                if len(self.sensor_list[i].avg_arr) < self.sensor_list[i].max_length:
                    self.sensor_list[i].avg_arr.append(new_element) # appends new elements
                else:
                    #shift every array elem down 1 and remove oldest
                    #put in new elem
                    self.sensor_list[i].avg_arr.pop(0) # shifts all elements left
                    self.sensor_list[i].avg_arr.append(new_element) # appends new element
                self.avg = sum(self.sensor_list[i].avg_arr)/len(self.sensor_list[index].avg_arr)
        
    