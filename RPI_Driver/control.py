import os
from PI_Servo import *
from commandInput import *

servo_controller = PI_ServoController(16)
while True:
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    servo_controller.parse(key_msg)
    