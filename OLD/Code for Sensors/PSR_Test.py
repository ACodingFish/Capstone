import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
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

# force sensitive resistor connected to adc #0-2
fsr_adc1 = 0
fsr_adc2 = 1
fsr_adc3 = 2

last_read1 = 0       # this keeps track of the last fsr value
last_read2 = 0
last_read3 = 0
tolerance = 5       # imposed tolerance

while True:
        # we'll assume that the fsr hasn't been excited
        fsr_changed = False
        
        ################### Start sensor 1 code #########################
        current_read1 = readadc(fsr_adc1, SPICLK, SPIMOSI, SPIMISO, SPICS)    # read the analog pin
        fsr_adjust1 = abs(current_read1 - last_read1)                         # how much has it changed since the last read

        if DEBUG:
                print ('Current Read:'), current_read1
                print ('Last Read'), last_read1

        if (fsr_adjust1 > tolerance):
               fsr_changed = True

        #if DEBUG:
        #        print ('fsr_changed'), fsr_changed

        if (fsr_changed):
                set_change1 = current_read1 / 10.24       # convert 10bit adc0 fsr read into 0-1024 force level
                set_change1 = round(set_change1)          # round out decimal value
                set_change1 = int(set_change1)            # cast volume as integer

                #if DEBUG:
                #        print ('Changed Amount:'), set_change1

                # save the fsr reading for the next loop
                last_read1 = current_read1
       
       ############### Start sensor 2 code #################################        
        current_read2 = readadc(fsr_adc2, SPICLK, SPIMOSI, SPIMISO, SPICS)    # read the analog pin
        fsr_adjust2 = abs(current_read2 - last_read2)                         # how much has it changed since the last read

        if DEBUG:
                print ('Current Read:'), current_read2
                print ('Last Read'), last_read2

        if (fsr_adjust2 > tolerance):
               fsr_changed = True

        #if DEBUG:
        #        print ('fsr_changed'), fsr_changed

        if (fsr_changed):
                set_change2 = current_read2 / 10.24       # convert 10bit adc0 fsr read into 0-1024 force level
                set_change2 = round(set_change2)          # round out decimal value
                set_change2 = int(set_change2)            # cast volume as integer

                #if DEBUG:
                #        print ('Changed Amount:'), set_change2

                # save the fsr reading for the next loop
                last_read2 = current_read2
                
        ################### Start sensor 3 code #########################
        current_read3 = readadc(fsr_adc3, SPICLK, SPIMOSI, SPIMISO, SPICS)    # read the analog pin
        fsr_adjust3 = abs(current_read3 - last_read3)                         # how much has it changed since the last read

        if DEBUG:
                print ('Current Read:'), current_read3
                print ('Last Read'), last_read3

        if (fsr_adjust3 > tolerance):
               fsr_changed = True

        #if DEBUG:
        #        print ('fsr_changed'), fsr_changed

        if (fsr_changed):
                set_change3 = current_read3 / 10.24       # convert 10bit adc0 fsr read into 0-1024 force level
                set_change3 = round(set_change3)          # round out decimal value
                set_change3 = int(set_change3)            # cast volume as integer

                #if DEBUG:
                #        print ('Changed Amount:'), set_change3

                # save the fsr reading for the next loop
                last_read3 = current_read3       

        # hang out and do nothing for a half second
        time.sleep(0.5)
        os.system('clear')