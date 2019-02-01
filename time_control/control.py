import os
import sys
from PI_Servo import *

servo_controller = PI_ServoController(16)
while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    elif(key_msg[:5].lower() == "fhome"):
        servo_controller.force_home()
            
    servo_controller.parse(key_msg)
    