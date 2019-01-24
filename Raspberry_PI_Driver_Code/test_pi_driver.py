
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16) #creates the serevokit class with channels set to 16
#kit.servo[0].set_pulse_width_range(1000, 2000) #to change pulse width range
#kit.servo[0].actuation_range = 160 # to set actuation range



kit.servo[0].angle = 180 #move hat 0 to 180 degrees.

def set_angle(servo,angle):

def parse_message(instruction):
    