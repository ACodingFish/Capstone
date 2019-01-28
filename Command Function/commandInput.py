
import sys

# allows code in python 2 AND 3 
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *
        
angle = ""
servo = ""
        
def parse_function(command_in):
    
    global angle
    global servo
    j = 0
    temp = ""
    
    for i in command_in:
        sorter = list(command_in[j])
        #print(sorter)
        m = 0
        
        for k in sorter:
            number_indicator = sorter[m].isdigit()
            
            if number_indicator == True:
                temp = sorter[m]
                angle = angle+temp
                m = m+1
                
            if number_indicator == False:
                servo = sorter[m]
                m = m+1
                print(angle, servo)
                angle = ""
                servo = ""
        j = j+1
            
   

parse_function("12a 14b")