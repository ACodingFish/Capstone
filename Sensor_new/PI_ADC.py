import time
import os
import RPi.GPIO as GPIO

if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_ADC:
    def __init__(self, num_avgs):
        self.num_avg = 0            #init to 0
        if (num_avgs < 1):
            num_avgs = 1):
        self.max_num_avg = num_avgs #number of times to average
        self.avg_arr = []
        self.avg = 0
    
class PI_ADC_MONITOR:
    def __init__(self, num_channels=8, num_avgs=3):
        self.num_channels = num_channels
        self.adc = [] #insert class here (Somehow pass parameters? or default them?)
        #initialize the adc
        GPIO.setmode(GPIO.BCM)
        
        # SPI ports on the ADC to the Cobbler
        self.SPI_CLK = 11
        self.SPI_MISO = 9
        self.SPI_MOSI = 10
        self.SPI_CS = 8

        # set up the SPI interface pins
        GPIO.setup(self.SPI_MOSI, GPIO.OUT)
        GPIO.setup(self.SPI_MISO, GPIO.IN)
        GPIO.setup(self.SPI_CLK, GPIO.OUT)
        GPIO.setup(self.SPI_CS, GPIO.OUT)
        # initialize number of channels
        for i in range(self.num_channels):
            self.adc.append(PI_ADC(num_avgs)) # average 3 times
            
        #start thread
        start_new_thread(self.monitor_thread,())
        
        
    def read_adc(self, channel):
        #read from ADC at index
        if ((channel > 7) or (channel < 0)):
                return -1
        GPIO.output(self.SPI_CS, True)

        GPIO.output(self.SPI_CLK, False)  # start clock low
        GPIO.output(self.SPI_CS, False)     # bring CS low

        commandout = channel
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(self.SPI_MOSI, True)
                else:
                        GPIO.output(self.SPI_MOSI, False)
                commandout <<= 1
                GPIO.output(self.SPI_CLK, True)
                GPIO.output(self.SPI_CLK, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(self.SPI_CLK, True)
                GPIO.output(self.SPI_CLK, False)
                adcout <<= 1
                if (GPIO.input(self.SPI_MISO)):
                        adcout |= 0x1

        GPIO.output(self.SPI_CS, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
            
    def monitor_thread(self):
        while True:
            for i in range(self.num_channels):
                value = self.read_adc(i)
                if (self.adc[i].num_avg < self.adc[i].max_num_avg):# initialize num avg to zero first (this is the number that have been read)
                    self.adc[i].num_avg += 1
                else:
                    #shift every array elem down 1 and remove oldest
                    #put in new elem
                    self.adc[i].avg_arr.pop(0) # shifts all elements left
                self.adc[i].avg_arr.append(value) # appends new element
                self.adc[i].avg = sum(self.adc[i].avg_arr)/self.length
    
    def get_adc_avg(self, index):
        return self.adc[i].avg #should default to 0
        