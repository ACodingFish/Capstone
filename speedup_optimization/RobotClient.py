#!/usr/bin/python3
#Server program
import sys
import os
#from PI_Cli import *
from PI_RobotManager import *

robot = PI_RobotManager()

while True:
    #should be able to put pass here
    key_msg = sys.stdin.readline()
    if (key_msg[:4].lower() == "exit"):
        os._exit(0)
    robot.parse(key_msg)
