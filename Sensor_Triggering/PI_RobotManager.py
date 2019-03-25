import sys
import os
import time
from PI_Cli import *
from PI_Servo import *
from PI_Conf import *
#from PI_ADC import *
from PI_Sonar import *





if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *
    
class PI_RobotManager:
    def __init__(self):
        conf = PI_Conf("conf/rob.conf")
        local = (conf.data[Params.LOCAL] == "1")
        ip_addr = conf.data[Params.IP_ADDR]
        port = conf.data[Params.PORT]
        encryption = (conf.data[Params.ENCRYPTION] == "1")
        cli_id = conf.data[Params.ID]
        
        if (type(ip_addr) != str):
            ip_addr = str(ip_addr)
        if (type(port) != int):
            port = int(port)
        if (type(cli_id) != str):
            cli_id = str(cli_id)
            
        self.sonar = PI_Sonar_Monitor()
        start_new_thread(self.sensor_thread,())
        
        #adc = PI_ADC_MONITOR()
        
        self.local = local
        channels = 16
        self.robot = PI_ServoController(channels) # Start servo controller with 16 channels
        #Start remote thread
        if (self.local == False):
            self.cli = PI_Cli(ip_addr, port, encryption)
            start_new_thread(self.command_thread,())
        #start local thread
        start_new_thread(self.local_command_thread,())
        print("Client -- " + cli_id + " -- online.")
        self.left_psr = 0
        self.right_psr = 0

            

    #get msg, parse msg
    def command_thread(self):
        while True:
            msg = self.cli.Recv_Msg()
            if (len(msg) >0):
                #relay msg to robot
                self.parse(msg)
            
    def local_command_thread(self):
        while True:
            msg = sys.stdin.readline()
            if (msg[:4].lower() == "exit"):
                os._exit(0)
            elif (len(msg) >0):
                #relay to robot
                self.parse(msg)
            
    def grab(self):
        while (self.left_psr <=0 and self.right_psr <= 0):
            pass
        
        claw_index = len(self.robot.servo_list)-1 #claw is the last servo
        claw_closed = self.robot.servo_list[claw_index].max_pos
        self.robot.set_servo_position(claw_index, claw_closed)
        #time.sleep(.001) #wait for command
        #operation will terminate if either two sensors are triggered or the arm stops moving
        while (self.left_psr <=0 or self.right_psr <= 0) and (self.robot.servo_list[claw_index].current_angle != claw_closed):# and (self.robot.servo_list[claw_index].is_moving == True):
            pass
        self.robot.servo_list[claw_index].set_hard_stop()
        
        
    #   Parses commands and relays them to their given functions if they are valid.     
    def parse(self, commands):
        for command in commands.split(", "):
            index = 0
            for character in command:
                if (character.isdigit()): 
                    index += 1
                else:#elif (index>0):           
                    #print("\tIndex: ",int(command[:index]),"\tString: ",command[index:])
                    print("Command:",command[index:].replace('\n',''))
                    servo_index = { \
                    \
                    #Servo index
                    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, \
                     #Commands (negative to allow for expandability of servos)
                    "home":-2, "obst":-3, "obcl":-4, "sd":-5, "sdeg":-6, "print":-7, "pos":-8, "grab":-9, "lpsr":-10, "rpsr":-11 \
                    \
                    }.get(command[index:].replace('\n','').lower(), -1)
                    # [num][a-f]    => send servo to this target position
                    # home          => send servos to home position
                    # obst          => tell servos that an obstacle is in the way
                    # obcl          => clear the obstacle command
                    # [num]sd       => set the robot's movement duration to the specified number in MS
                    # [num]sdeg     => set the robot's movement step to the specified number in Degrees
                    # print         => print the robot's current and target positions
                    # pos           => relay the robot's current and target positions to the server
                    # grab          => prepare the robot for an object to grab
                    # lpsr          => set the left number of triggered pressure sensors
                    # rpsr          => set the right number of triggered pressure sensors
                    if servo_index == -2:
                        self.robot.go_home()
                    elif servo_index == -3:
                        self.robot.servos_obstructed = True
                    elif servo_index == -4:
                        self.robot.servos_obstructed = False
                    elif (servo_index == -5) and (index > 0):
                        self.robot.set_movement_duration(command[:index])
                    elif (servo_index == -6) and (index > 0):
                        self.robot.set_movement_step_deg(command[:index])
                    elif servo_index == -7:
                        for servos in self.robot.servo_list:
                            print("[",servos.index, "]: ", servos.current_angle, " TARGET:", servos.target_angle)
                    elif servo_index == -8:
                        if self.local == False:
                            pos = ""
                            for servos in self.robot.servo_list:
                                pos+=("S" + str(servos.index) + "$" + str(servos.current_angle) + "$" + str(servos.target_angle)) # Ex. S0$100$180, s1$50$20, ...
                                pos+=(", ")
                            cli.Send_Msg(pos[:-1]) #remove last char and relay to server
                    elif servo_index == -9:      
                        start_new_thread(self.grab,())
                    elif (servo_index == -10 and index >0):      
                        self.left_psr = int(command[:index])
                    elif (servo_index == -11 and index >0):      
                        self.right_psr = int(command[:index])
                    elif (servo_index >=0 and index >0):
                        self.robot.set_servo_position(servo_index, command[:index]) # servo_index, servo_position
                    break
                
    def sensor_thread(self):
        time.sleep(2)
        while True:
            sonar_bool = False
            for i in range(self.sonar.num_sensors):
                if (self.sonar.channel_triggered(i)):
                    sonar_bool = True
            if (sonar_bool == True):
                self.parse("obst")
            else:
                self.parse("obcl")
