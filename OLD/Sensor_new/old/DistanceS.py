import RPi.GPIO as GPIO
import time, serial
from xbee import DigiMesh
GPIO.setmode(GPIO.BCM)
ser = serial.Serial('/dev/ttyAMA0', 9600)
zb = DigiMesh(ser)
trig = 23
echo = 24
a = [0, 0, 0]
i = 0
feedback = 'Obstruction Detected!'

try:
    #Configure GPIO pins
    GPIO.setup(trig,GPIO.OUT)
    GPIO.setup(echo,GPIO.IN)
    GPIO.output(trig,False)

    time.sleep(1.5) #Delay between detections
    GPIO.output(trig,True)
    time.sleep(0.00001) #Pulse time = 10us
    GPIO.output(trig,False)

    while GPIO.input(echo) == 0:
        pulse_start = time.time() #Records the start time of the pulse

    while GPIO.input(echo) == 1:
        pulse_end = time.time() #Records the end time of the pulse

    pulse_duration = pulse_end - pulse_start #Calculates pulse time

    #Speed of sound at sea level is 343m/s
    #Speed = Distance/Time
    #34300 = Distance/(Time/2) because we only need the one way time
    distance = pulse_duration * 17150 #Final formula for getting distance
    distance = round(distance,2)
    print "Distance:",distance,"cm"
    a[0] = distance
    a[1] = distance
    a[2] = distance
    average = (a[0] + a[1] + a[2])/3
    average = round(average,2)
    print "Average:",average
    print(a)
    
    if average <= 5: 
            zb.send("tx", id = b'\x10', frame_id = b'\x00', dest_addr = b'\x00\x13\xA2\x00\x41\x54\xF3\xFF', reserved = b'\xFF\xFE', broadcast_radius = b'\x00', options = b'\x00', data = feedback)
        
    while True:
        a[0] = a[1]
        a[1] = a[2]
        
        #Configure GPIO pins
        GPIO.setup(trig,GPIO.OUT)
        GPIO.setup(echo,GPIO.IN)
        GPIO.output(trig,False)

        time.sleep(1.5) #Delay between detections
        GPIO.output(trig,True)
        time.sleep(0.00001) #Pulse time = 10us
        GPIO.output(trig,False)

        while GPIO.input(echo) == 0:
            pulse_start = time.time() #Records the start time of the pulse

        while GPIO.input(echo) == 1:
            pulse_end = time.time() #Records the end time of the pulse

        pulse_duration = pulse_end - pulse_start #Calculates pulse time

        #Speed of sound at sea level is 343m/s
        #Speed = Distance/Time
        #34300 = Distance/(Time/2) because we only need the one way time
        distance = pulse_duration * 17150 #Final formula for getting distance
        distance = round(distance,2)
        print "Distance:",distance,"cm"
        a[2] = distance
        average = (a[0] + a[1] + a[2])/3
        average = round(average,2)
        print "Average:",average
        print(a)
        
        if average <= 5: 
            zb.send("tx", id = b'\x10', frame_id = b'\x00', dest_addr = b'\x00\x13\xA2\x00\x41\x54\xF3\xFF', reserved = b'\xFF\xFE', broadcast_radius = b'\x00', options = b'\x00', data = feedback)
    
except:
    GPIO.cleanup()
    
    
    
    

