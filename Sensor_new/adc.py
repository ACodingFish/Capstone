#https://pypi.org/project/mcp3008/
#pip install mcp3008
#or 
#https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython
#sudo pip3 install adafruit-circuitpython-mcp3xxx
#
#pin 7 - CE1#
#Pin 8 - CE0#
#pin 9 - MISO
#pin10 - MOSI
#pin11 - SCLK

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

num_adcs = 7
analog_pins = [MCP.P0,MCP.P1,MCP.P2,MCP.P3,MCP.P4,MCP.P5,MCP.P6,MCP.P7]
channels = []
for i in range(len(analog_pins)):
    channels[i] = AnalogIn(mcp, analog_pins[i])
    
while True:
    for i in range(len(channels)):
        print("Val: ", channel.value)
        print("Volt: ", str(channel.voltage))
        sleep(0.5)
