import sys
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *
    
from PI_ADC import *
from PI_Sonar import *

class PI_SensorManager:
    def __init__(self):
        #sonar
        self.sonar = PI_Sonar_Monitor()
        self.prev_sonar_bool = False
        self.sonar_active = True

        
        #ADC
        self.adc = PI_ADC_MONITOR()
        self.num_adc = self.adc.num_channels
        self.half_num_adc = self.num_adc/2
        self.prev_adc_left_count = 0
        self.prev_adc_right_count = 0
        start_new_thread(self.sensor_thread,())
        
    def sensor_thread(self):
        while True:
            if (self.sonar.initialized == True) and (self.adc.initialized == True):
                while True:
                    if(self.sonar_active == True):
                        self.sonar.start_sonar()
                        while (self.sonar.is_sonar_idle() != True):
                            self.sonar.run_sonar_sensors_thread()
                        self.sonar_active =  False
                    else:
                        self.adc.monitor_thread()
                        self.sonar_active = True
                    
    def detect_sonar(self):
        try:
            parse_str = []
            sonar_bool = False
            for i in range(self.sonar.num_sensors):
                if (self.sonar.channel_triggered(i)):
                    sonar_bool = True
                    break

            if (sonar_bool == True)and(self.prev_sonar_bool == False):
                parse_str.append("obst")
                self.prev_sonar_bool = True
            elif (sonar_bool == False)and(self.prev_sonar_bool == True):
                parse_str.append("obcl")
                self.prev_sonar_bool = False
            return parse_str
        except Exception as e:
            print(e)
            return ["obst"]
    
    def detect_adc(self):    
        #adc
        try:
            parse_str = []
            adc_left_count = 0
            adc_right_count = 0
            for i in range(self.num_adc):
                if (self.adc.channel_triggered(i)):
                    if (i < self.half_num_adc):
                        #left
                        adc_left_count+=1
                    else:
                        #right
                        adc_right_count+=1

            if (adc_left_count != self.prev_adc_left_count):
                parse_str.append(str(adc_left_count) + "lpsr")
                self.prev_adc_left_count = adc_left_count
            elif (adc_right_count != self.prev_adc_right_count):
                parse_str.append(str(adc_right_count) + "rpsr")
                self.prev_adc_right_count = adc_right_count
            return parse_str
        except Exception as e:
            self.prev_adc_left_count = 5
            self.prev_adc_right_count = 5
            print(e)
            return ["5lspr","5rpsr"]
