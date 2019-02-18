import sys
import os
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
trig = 23
echo = 24
# SPI ports on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
DEBUG = 1
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *#Server program

class SMonitor:
    def __init__(self, max_length):
        if (max_length < 1):
            max_length = 1
        self.length = 0
        self.length2 = 0
        self.max_length = 1 #max_length
        self.avg_arr = []
        self.avg = 0
        start_new_thread(self.monitor_thread, ())
        #Configure GPIO pins
        GPIO.setup(trig,GPIO.OUT)
        GPIO.setup(echo,GPIO.IN)
        GPIO.output(trig,False)
        self.adcpin = 0
        self.fsr_avg = 0
        self.avg_fsr_arr = []
        self.count = 0
        start_new_thread(self.psr_thread, ())
        # set up the SPI interface pins
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)
        
        
    
    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(SPICS, True)

        GPIO.output(SPICLK, False)  # start clock low
        GPIO.output(SPICS, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(SPIMOSI, True)
                else:
                        GPIO.output(SPIMOSI, False)
                commandout <<= 1
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)
                adcout <<= 1
                if (GPIO.input(SPIMISO)):
                        adcout |= 0x1

        GPIO.output(SPICS, True)
        print(adcout)
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
        
    def psr_reading(self): #Pressure Sensor ##########################
        # force sensitive resistor connected to adc #0-2
        fsr_adc1 = 0
        fsr_adc2 = 1
        fsr_adc3 = 2
        
        current_read1 = self.readadc(fsr_adc1)    # read the analog pin
                
        return current_read1
    
    def psr_thread(self): #Pressure Sensor #####################
        while True:
            time.sleep(0.1)
            reading = self.psr_reading()
            if self.length2 < self.max_length:
                self.length2 = self.length2 + 1
                self.avg_fsr_arr.append(reading) # appends new elements
            else:
                #shift every array elem down 1 and remove oldest
                #put in new elem
                self.avg_fsr_arr.pop(0) # shifts all elements left
                self.avg_fsr_arr.append(reading) # appends new element
            self.fsr_avg = sum(self.avg_fsr_arr)/self.length2
    
    def psr_avg(self): #Pressure Sensor ######################
        # compute average
        if (self.count >= 20):
            os.system('clear')
            self.count = 0
        else:
            self.count += 1
        print("Measured Pressure: %(fsravg)d" % {"fsravg": self.fsr_avg} )
        return self.fsr_avg
            
            
    def get_elem(self):
        #get some stuff
        while GPIO.input(echo) == 0:
            pulse_start = time.time() #Records the start time of the pulse

        while GPIO.input(echo) == 1:
            pulse_end = time.time() #Records the end time of the pulse

        pulse_duration = pulse_end - pulse_start #Calculates pulse time

        #Speed of sound at sea level is 343m/s
        #Speed = Distance/Time
        #34300/2 = Distance/(Time/2) because we only need the one way distance
        distance = pulse_duration * 17150.0 #Final formula for getting distance
        distance = round(distance,2)
        return distance
        
    def monitor_thread(self):
        while True:
            time.sleep(0.1) #Delay between detections
            GPIO.output(trig,True)
            time.sleep(0.00001) #Pulse time = 10us
            GPIO.output(trig,False)
            new_element = self.get_elem()
            if self.length < self.max_length:
                self.length = self.length + 1
                self.avg_arr.append(new_element) # appends new elements
            else:
                #shift every array elem down 1 and remove oldest
                #put in new elem
                self.avg_arr.pop(0) # shifts all elements left
                self.avg_arr.append(new_element) # appends new element
            self.avg = sum(self.avg_arr)/self.length
            
    def get_avg(self):
        # compute average
        if (self.count >= 20):
            os.system('clear')
            self.count = 0
        else:
            self.count += 1
        print("Measured Distance: %(avg)d" % {"avg": self.avg} )
        return self.avg
