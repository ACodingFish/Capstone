import os
from PI_Servo import *

servo_controller = PI_ServoController(16)
while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    elif(key_msg[:5].lower() == "print"):
        for servos in servo_controller.servo_list:
            print(servos.index, " ", servos.current_angle, " ", servos.target_angle)
    elif(key_msg[:4].lower() == "obst"):
        servo_controller.servos_obstructed = True
    elif(key_msg[:4].lower() == "obcl"):
        servo_controller.servos_obstructed = False
    servo_controller.parse(key_msg)
    