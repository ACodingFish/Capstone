import sys
import os
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *      #Server program
    
class PI_Sonar:
    def __init__(self, trig, echo, max_length):
        self.trig = trig
        self.echo = echo
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.output(self.trig,False)
        self.max_length = max_length
        self.avg_arr = []
        self.avg = 0
        self.pulse_start = 0
        self.pulse_end = 0
        self.pulse_wait_time = 0
        self.timeout = 0
        self.state = "Start"
    
    
class PI_Sonar_Monitor:
    def __init__(self):
        self.sensor_list = []
        # [[trigger pin, echo pin, num_avgs],....]
        sonar_info=[[23,24,3],[5,6,3]]
        self.num_sensors = len(sonar_info)
        for sensor in sonar_info:
            self.add_sensor(sensor[0], sensor[1], sensor[2]) 
        start_new_thread(self.run_sonar_sensors_thread,())
        
        
    def add_sensor(self, trig, echo, num_avgs):
        new_sensor = PI_Sonar(trig, echo, num_avgs)
        self.sensor_list.append(new_sensor)
    
#    def get_elem(self, index):
#        #get some stuff
#        while GPIO.input(self.sensor_list[index].echo) == 0:
#            pulse_start = time.time() #Records the start time of the pulse
#
#        while GPIO.input(self.sensor_list[index].echo) == 1:
#            pulse_end = time.time() #Records the end time of the pulse

#        pulse_duration = pulse_end - pulse_start #Calculates pulse time

        #Speed of sound at sea level is 343m/s
        #Speed = Distance/Time
        #34300/2 = Distance/(Time/2) because we only need the one way distance
#        distance = pulse_duration * 17150.0 #Final formula for getting distance
#        distance = round(distance,2)
#        return distance
    
    def run_sonar_sensors_thread(self):
        while True:
            for i in range(self.num_sensors):
                prev_state = self.sensor_list[i].state
                if (self.sensor_list[i].state == "Start"):
                    self.sensor_list[i].pulse_wait_time = time.time()
                    self.sensor_list[i].state = "Prep"
                elif (self.sensor_list[i].state == "Prep"):
                    #time.sleep(0.0001) #Delay between detections
                    if ((time.time() - self.sensor_list[i].pulse_wait_time) > 0.06):
                        GPIO.output(self.sensor_list[i].trig,True)
                        self.sensor_list[i].pulse_wait_time = time.time()
                        self.sensor_list[i].state = "Pulse"
                elif (self.sensor_list[i].state == "Pulse"):
                        #time.sleep(0.00001) #Pulse time = 10us
                    if ((time.time() - self.sensor_list[i].pulse_wait_time) > 0.00001):
                        GPIO.output(self.sensor_list[i].trig,False)
                        self.sensor_list[i].pulse_sent = True
                        self.sensor_list[i].state = "Recv"
                    elif ((time.time() - self.sensor_list[i].timeout) > 0.02):
                        #ERROR
                        self.sensor_list[i].state = "Error1"
                elif (self.sensor_list[i].state == "Recv"):
                    self.sensor_list[i].pulse_start = time.time()
                    if (GPIO.input(self.sensor_list[i].echo) == 1):
                        self.sensor_list[i].state = "WaitSig"
                    elif ((time.time() - self.sensor_list[i].timeout) > 0.02): #time based on speed of traversal (4m/(343m/s))
                        #ERROR
                        self.sensor_list[i].state = "Error2"
                elif (self.sensor_list[i].state == "WaitSig"):
                    self.sensor_list[i].pulse_end = time.time()
                    if (GPIO.input(self.sensor_list[i].echo) == 0):
                        self.sensor_list[i].state = "Calc"
                    elif ((time.time() - self.sensor_list[i].timeout) > 0.1):
                        #ERROR
                        self.sensor_list[i].state = "Error3"
                elif (self.sensor_list[i].state == "Calc"):
                    # averaging
                    pulse_duration = self.sensor_list[i].pulse_end - self.sensor_list[i].pulse_start
                    distance = pulse_duration * 17150.0 #343*1000/2, round trip distance, speed of sound at sea level
                    # insert into array
                    if len(self.sensor_list[i].avg_arr) < self.sensor_list[i].max_length:
                        self.sensor_list[i].avg_arr.append(distance) # appends new elements
                    else:
                        #shift every array elem down 1 and remove oldest
                        #put in new elem
                        self.sensor_list[i].avg_arr.pop(0) # shifts all elements left
                        self.sensor_list[i].avg_arr.append(distance) # appends new element
                    self.sensor_list[i].avg = sum(self.sensor_list[i].avg_arr)/len(self.sensor_list[i].avg_arr)
                    self.sensor_list[i].state = "Start"
                else: # Default state
                    print("RANGE EXCEPTION ON SENSOR:", i, self.sensor_list[i].state)
                    self.sensor_list[i].state = "Start"
                
                if (self.sensor_list[i].state != prev_state):
                    self.sensor_list[i].timeout = time.time()
                    

    def get_avg(self, index):
        return self.sensor_list[index].avg
        
    