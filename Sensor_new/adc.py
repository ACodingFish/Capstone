import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = True

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(channel, clockpin, mosipin, misopin, cspin):
        if ((channel > 7) or (channel < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = channel
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# SPI ports on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
num_channels = 8

while True:
        # we'll assume that the fsr hasn't been excited
        for i in range(num_channels):
            ################### Start sensor 1 code #########################
            current_read1 = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)    # read the analog pin

            if DEBUG:
                print ("Sensor",i)
                print ('Current Read:', current_read1)
       
            # hang out and do nothing for a half second
            time.sleep(0.5)
            os.system('clear')