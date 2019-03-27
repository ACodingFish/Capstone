# Uses product/libraries from:
# https://www.adafruit.com/product/2327
# https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/
#requires installation of adafruit servokit (adafruit-circuitpython-servokit)
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

# Servo class to hold control parameters such as home position, range, etc.
class PI_Servo:
    # Initialize the servo class with its parameters
    def __init__(self, index, range_deg, home_pos, max_pos, min_pos, step, dur):
        self.index = int(index)
        self.range = int(range_deg)
        self.max_pos = int(max_pos)
        self.min_pos = int(min_pos)
        self.home = int(home_pos)

        self.current_angle = int(home_pos)
        self.prev_angle = int(home_pos)
        self.target_angle = int(home_pos)
        self.incrementing = False
        self.force_home()
        self.last_step_time = time.time()
        self.step_length = 1.0 #seconds
        self.step_deg = step # number of degrees per step
        self.default_duration = dur # Total movement duration in seconds
        
    def is_moving(self):
        #does not work.
        if (self.current_angle != self.target_angle):
            return True
        else:
            return False
    
    # Sets the duration and angle of a servo
    # Takes inputs of angle and duration
    def set_current_angle(self, angle, duration=-1): #duration is in seconds
        duration = int(duration)
        angle = int(angle)
        if (duration < 0):
            duration = self.default_duration
        if (duration > 0) and (angle > 0):
            distance = abs(angle - self.current_angle)
            if (distance > 0):
                self.target_angle = angle;

                if (angle < self.current_angle):
                    self.incrementing = False
                else:
                    self.incrementing = True
                self.step_length = duration*self.step_deg/distance #step_duration = duration/(distance/step_distance)
                print(self.target_angle)
                print(self.current_angle)
                #elf.last_step_time = time.time()
        else:
            print("Invalid duration or angle")
    
    # Sets angle with a movement speed
    # takes input of an angle and a speed in degrees per second
    def set_current_angle_w_speed(self, angle, speed):  #speed is in deg/sec
        #speed = distance/duration
        #distance/speed = duration
        speed = int(speed)
        angle = int(angle)
        if (angle > 0) and (speed > 0):
            duration = abs(angle - self.current_angle)/speed
            self.set_current_angle(angle, duration)
        else:
            print("Invalid Speed or Angle")
    
    # Sets the default duration of a servo's movement.
    def set_default_duration(self, duration):
        duration = float(duration)
        if (duration > 0):
            self.default_duration = duration
        else:
            print("Invalid duration: ", duration)
    
    # Sets the step length in degrees of a servo.
    def set_step_deg (self, step_deg):
        step_deg = int(step_deg)
        if (step_deg > 0):
            self.step_deg = step_deg
        else:
            print("Invalid step value: ", step_deg)
    
    # Stops the servo (Because of obstruction)
    def set_obstruction(self):
        self.current_angle = self.prev_angle
        self.target_angle = self.prev_angle
    
    # Stops the servo at it's current position
    def set_hard_stop(self):
        self.target_angle = self.current_angle
    
    # Forces the robot to go home.
    def force_home(self): # be careful with this as it may damage equipment or persons if they are in the robot's path
        self.current_angle = self.home-1
        self.prev_angle = self.home-1
        self.target_angle = self.home
    
    # Determines the time since the last movement step was taken
    def time_since_step(self):
        return (time.time() - self.last_step_time)
    
    # Resets the time since the last movement step was taken
    def reset_time(self):
        self.last_step_time = time.time()
        
# Class to control all of the servos and approximate their movements.        
class PI_ServoController:
    # Initializes the servo controls and the servo classes with all of their parameters.
    def __init__(self, max_channels):
        self.servos_controlled = False;
        self.max_channels = max_channels
        self.kit = ServoKit(channels=self.max_channels)
        self.servo_list = []
        #add servos [[sv1_range, sv1_home, sv1_max_deg, sv1_min_deg], [sv2...],...]
        sv_info = [[180,90,180,1],[180,45,135,1],[180,90,180,1],[180,90,180,1],[180,90,180,1],[120,1,40,1]]
        # servo 1 - right to left
        # servo 2 - top to bottom
        # servo 3 - top to bottom
        # servo 4 - top to bottom
        # servo 5 - right to left
        # servo 6 - 40 (closed) 1 (open)
        step_len = 1
        mov_duration = 3.0
        for sv in sv_info:
            self.add_servo(sv[0],sv[1], sv[2], sv[3], step_len, mov_duration)
        for i in range(len(sv_info)):
            if (sv_info[i][0] == 270):
                #self.kit.servo[i].set_pulse_width_range(500, 4000) #not accurate yet
                pass
            elif (sv_info[i][0] == 180):
                self.kit.servo[i].set_pulse_width_range(500, 2500)
            else:
                self.kit.servo[i].set_pulse_width_range(750, 2000)
                #pass
        
        start_new_thread(self.servo_manager_thread,())  #start thread
        self.servos_obstructed = False #pay attention to this --> may cause issues later
        self.servos_controlled = True
        
    # Creates a servo with given initialization parameters
    # Inputs are:
    #   movement range in degrees
    #   home position in degrees
    #   max position of servo in degrees
    #   min position of servo in degrees
    #   Step length of movement of servo in degrees
    #   Duration of movement in Seconds
    def add_servo(self, range_deg, home_pos, max_pos, min_pos, step, dur):
        index = len(self.servo_list)
        if (index < self.max_channels):
            self.kit.servo[index].actuation_range = range_deg
            new_servo = PI_Servo(index, range_deg, home_pos, max_pos, min_pos, step, dur)
            self.servo_list.append(new_servo)
        else:
            print("Servos at Max Capacity")
    
    #   Sets movement duration in mSec
    def set_movement_duration(self, duration):
        
        duration = float(duration)/1000
        print("Setting duration to: ", duration, "s")
        for servos in self.servo_list:
            servos.set_default_duration(duration)
    
    #   Sets movement step in degrees
    def set_movement_step_deg(self, deg):
        print("Setting step (deg) to: ", deg)
        deg = int(deg)
        for servos in self.servo_list:
            servos.set_step_deg(deg)
    
    #   Sets all servos to home position
    def go_home(self):
        for servos in self.servo_list:
            #self.kit.servo[servos.index].angle = int(servos.home)
            servos.set_current_angle(servos.home)
            
    #   Forces all servos to move to the home position
    def force_home(self):
        for servos in self.servo_list:
            #self.kit.servo[servos.index].angle = int(servos.home)
            servos.force_home()
    
    # Sets a specified servo to a given position
    # Takes in a servo's index and it's desired position
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
    
    # Thread to control the servos and approximate the movement.
    # This allows movements to be controlled, synchronized, and for the direction to be changed mid-movement
    def servo_manager_thread(self):
        #could delay here to protect on startup.
        #pre_loop_time = 0
        while True:
            #print((time.time()-pre_loop_time)%1.0)
            if (self.servos_controlled == True):
                if (self.servos_obstructed == False):
                    for servos in self.servo_list:
                        if (servos.current_angle != servos.target_angle):
                            #if there is no obstruction
                            if (servos.time_since_step() >= servos.step_length):
                                servos.reset_time()
                                servos.prev_angle = servos.current_angle #update prev angle
                                if (servos.incrementing == True):
                                    servos.current_angle += servos.step_deg
                                    if (servos.current_angle > servos.target_angle):
                                        servos.current_angle = servos.target_angle
                                else:
                                    servos.current_angle -= servos.step_deg
                                    if (servos.current_angle < servos.target_angle):
                                        servos.current_angle = servos.target_angle 
                                self.kit.servo[servos.index].angle = int(servos.current_angle)
                                print("Servo[", servos.index,"] at: ", servos.current_angle)
                else:
                            # take servo obstructed action
                    for servos in self.servo_list:
                        servos.set_obstruction()
                        self.kit.servo[servos.index].angle = int(servos.prev_angle)
                #pre_loop_time = time.time()