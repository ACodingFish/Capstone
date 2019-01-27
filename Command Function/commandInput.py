import sys

# allows code in python 2 AND 3 
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *


    
# First we receive the command

command_in = input('Enter a command for the Robot: ')
servo = ""
angle = None



#def recieve_command();
 #   while True:
        
        
            
def send_command();
    while True
        if command_in != "":
                single_command = command_in.split(', ')[0]
                command_characters = list(single_command)
                i = 0
                for command_characters != []
                    number_indicator = command_characters[i].isdigit
                    if number_indicator == True
                        angle = angle+command_characters[i]
                    if number_indicator == False
                        servo = command_characters[i]
                    i++
                    [s[i+2] for s in command_in]
                print(angle, servo)

            
#start_new_thread(recieve_command,())
start_new_thread(send_command,())

while True:
    pass