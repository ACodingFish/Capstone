import os
import sys
from PI_Servo import *

servo_controller = PI_ServoController(16)
while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    elif(key_msg[:5].lower() == "print"):
        for servos in servo_controller.servo_list:
            print(servos.index, " ", servos.current_angle, " ", servos.target_angle)
    elif(key_msg[:5].lower() == "fhome"):
        servo_controller.force_home()
    elif(key_msg[:4].lower() == "sdur"):
        for servos in servo_controller.servo_list:
            print("set duration (sec) for servo [", servos.index,"]: ")
            duration = sys.stdin.readline()
            servos.set_default_duration(duration)
    elif(key_msg[:5].lower() == "sstep"):
        for servos in servo_controller.servo_list:
            print("set step #deg for servo [", servos.index,"]: ")
            deg = sys.stdin.readline()
            servos.set_step_deg(deg)
            
    servo_controller.parse(key_msg)
    