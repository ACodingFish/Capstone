# Uses product/libraries from:
# https://www.adafruit.com/product/2327
# https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/
import sys
import os
import time

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

from adafruit_servokit import ServoKit
#kit = ServoKit(channels=16) #creates the serevokit class with channels set to 16
#kit.servo[0].set_pulse_width_range(1000, 2000) #to change pulse width range
#kit.servo[0].actuation_range = 160 # to set actuation range

#kit.servo[0].actuation_range = 120 # to set actuation range
num_args = len(sys.argv)
if (num_args == 2):
    kit.servo[0].angle = int(sys.argv[1]) #move hat 0 to 180 degrees.
    
class PI_Servo:
    def __init__(self, index, range_deg, home_pos, max_pos, min_pos):
        self.index = index
        self.range = range_deg
        self.max_pos = max_pos
        self.min_pos = min_pos
        self.home = home_pos
        #make a force home
        self.current_angle = home_pos
        self.prev_angle = home_pos
        self.target_angle = home_pos
        self.incrementing = False
        self.force_home()
        self.last_step_time = time.time()
        self.step_length = 1.0
        
        
    def set_current_angle(self, angle, duration=3.0):
        self.target_angle = angle;
        print(self.target_angle)
        print(self.current_angle)
        if (angle < self.current_angle):
            self.incrementing = False
        else:
            self.incrementing = True
        self.step_length = duration/abs(self.target_angle - self.current_angle)
        
    def set_current_angle_w_speed(self, angle, speed):  #speed is in deg/sec
        #speed = distance/duration
        #distance/speed = duration
        duration = abs(angle - self.current_angle)/speed
        self.set_current_angle(angle, duration)
        
    def set_obstruction(self):
        self.current_angle = self.prev_angle
        self.target_angle = self.prev_angle
    
    def set_hard_stop(self):
        self.target_angle = self.current_angle
        
    def force_home(self): # be careful with this as it may damage equipment or persons if they are in the robot's path
        self.current_angle = home_pos-1
        self.prev_angle = home_pos-1
        self.target_angle = home_pos
    
    def time_since_step(self):
        return (time.time() - self.last_step_time)
        
    def reset_time(self):
        self.last_step_time = time.time()
        
    
class PI_ServoController:
    def __init__(self, max_channels):
        self.servos_controlled = False;
        self.max_channels = max_channels
        self.kit = ServoKit(channels=self.max_channels)
        self.servo_list = []
        #add servos [[sv1_range, sv1_home, sv1_max_deg, sv1_min_deg], [sv2...],...]
        sv_info = [[180,90,180,1],[180,30,180,1],[120,90,120,1],[120,60,120,1],[120,44,44,10]]
        # servo 1 - right to left
        # servo 2 - up to down
        # servo 3 - down to up
        # servo ##MISSING## 4 - ????
        # servo 5 - right to left
        # servo 6 - 44 (closed) 10 (open)
        for sv in sv_info:
            self.add_servo(sv[0],sv[1], sv[2], sv[3])
        
        start_new_thread(self.servo_manager_thread,())  #start thread
        self.servos_obstructed = False
        self.servos_controlled = True
        
    def add_servo(self, range_deg, home_pos, max_pos, min_pos):
        index = len(self.servo_list)
        if (index < self.max_channels):
            self.kit.servo[index].actuation_range = range_deg
            self.servo_list.append(PI_Servo(index, range_deg, home_pos, max_pos, min_pos))
        else:
            print("Servos at Max Capacity")
            
    def go_home(self):
        for servos in self.servo_list:
            #self.kit.servo[servos.index].angle = int(servos.home)
            servos.set_current_angle(servos.home)
    
    def force_home(self):
        for servos in self.servo_list:
            #self.kit.servo[servos.index].angle = int(servos.home)
            servos.force_home()
            
    def parse(self, commands):
        for command in commands.split(", "):
            index = 0
            for character in command:
                if (character.isdigit()): 
                    index += 1
                else:#elif (index>0):           
                    #print("\tIndex: ",int(command[:index]),"\tString: ",command[index:])
                    print("Command:",command[index:].replace('\n',''))
                    servo_index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "home":-2, "obst":-3, "obcl":-4}.get(command[index:].replace('\n',''), -1)
                    if servo_index == -2:
                        self.go_home()
                    elif servo_index == -3:
                        servo_controller.servos_obstructed = True
                    elif servo_index == -4:
                        servo_controller.servos_obstructed = False
                    elif (servo_index >=0 and index >0):
                        self.set_servo_position(servo_index, command[:index]) # servo_index, servo_position
                    break
    
    def set_servo_position(self, index, new_pos):
        new_pos = int(new_pos)
        index = int(index)
        if ((index >=0) and (index < len(self.servo_list))):
            if ((new_pos > self.servo_list[index].max_pos)or(new_pos < self.servo_list[index].min_pos)):
                print("Invalid Servo Position")
            else:
               self.servo_list[index].set_current_angle(new_pos)
        else:
            print("Invalid Index: ", index)
            
    def servo_manager_thread(self):
        #could delay here to protect on startup.
        step_deg = 1
        #pre_loop_time = 0
        while True:
            #print((time.time()-pre_loop_time)%1.0)
            time.sleep(.05)
            if (self.servos_controlled == True):
                if (self.servos_obstructed == False):
                    for servos in self.servo_list:
                        if (servos.current_angle != servos.target_angle):
                            #if there is no obstruction
                            if (servos.time_since_step() > servos.step_length):
                                servos.reset_time()
                                servos.prev_angle = servos.current_angle #update prev angle
                                if (servos.incrementing == True):
                                    servos.current_angle += step_deg
                                    if (servos.current_angle >= servos.target_angle):
                                        servos.current_angle = servos.target_angle
                                else:
                                    servos.current_angle -= step_deg
                                    if (servos.current_angle <= servos.target_angle):
                                        servos.current_angle = servos.target_angle 
                                self.kit.servo[servos.index].angle = int(servos.current_angle)
                                print("Servo[", servos.index,"] at: ", servos.current_angle)
                else:
                            # take servo obstructed action
                    for servos in self.servo_list:
                        servos.set_obstruction()
                        self.kit.servo[servos.index].angle = int(servos.target_angle)
                #pre_loop_time = time.time()