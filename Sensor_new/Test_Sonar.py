import time 
import math
from PI_Sonar import *

sonar = PI_Sonar_Monitor()

while True
    for i in range(sonar.num_sensors):
        print("Sensor: ", i)
        print("Average: ", sonar.get_avg(i))