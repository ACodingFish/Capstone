
import sys
import os
import time

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16) #creates the serevokit class with channels set to 16
#kit.servo[0].set_pulse_width_range(1000, 2000) #to change pulse width range
#kit.servo[0].actuation_range = 160 # to set actuation range

kit.servo[0].actuation_range = 120 # to set actuation range
num_args = len(sys.argv)
if (num_args == 2):
    kit.servo[0].angle = int(sys.argv[1]) #move hat 0 to 180 degrees.
    
time.sleep(1.5)
print("FIN!")
time.sleep(0.5)
    
class PI_Servo:
    def __init__(self, index, range_deg, home_pos):
        self.index = index
        self.range = range_deg
        self.home = home_pos
        self.current_angle = home_pos
        self.prev_angle = home_pos
        self.target_angle = home_pos
        
    def set_current_angle(self, angle):
        self.target_angle = angle;
        
    def set_obstruction(self, angle):
        self.current_angle = self.prev_angle
        self.target_angle = self.prev_angle
    
class PI_ServoController:
    def __init__(self, max_channels):
        self.servos_controlled = False;
        self.max_channels = max_channels
        self.kit = ServoKit(channels=self.max_channels)
        self.servo_list = []
        #add servos
        add_servo(120, 60)
        start_new_thread(self.servo_manager_thread,())  #start thread
        self.servos_controlled = True
        
    def add_servo(self, range_deg, home_pos):
        index = len(self.servo_list)
        if (index < self.max_channels):
            self.kit.servo[index].actuation_range = range_deg
            self.servo_list[index].append(PI_Servo(index, range_deg, home_pos))
        else:
            print("Servos at Max Capacity")
            
    def go_home(self):
        for servos in self.servo_list:
            #self.kit.servo[servos.index].angle = int(servos.home)
            servos.set_current_angle(servos.home)
    
    def set_servo_position(self, index, new_pos):
        if ((new_pos > self.servo_list[index].range)||(new_pos < 1)):
            print("Invalid Servo Position")
        else:
           self.servo_list[index].set_current_angle(new_pos)
            
    def servo_manager_thread(self):
        while True:
            if (self.servos_controlled == True):
                for servos in self.servo_list:
                    if (servos.current_angle != servos.target_angle):
                        #if there is no obstruction
                        self.kit.servo[servos.index].angle = int(servos.target_angle)
                        servos.prev_angle = servos.current_angle
                        servos.current_angle = servos.target_angle
