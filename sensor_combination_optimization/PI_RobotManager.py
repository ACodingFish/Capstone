import sys
import os
import time
import traceback
from PI_Cli import *
from PI_Servo import *
from PI_Conf import *
from PI_SensorManager import *


if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *

class PI_RobotManager:
    def __init__(self):
        self.ROBOT_INTIALIZED = False
        self.streaming = False
        conf = PI_Conf("conf/rob.conf")
        local = (conf.data[Params.LOCAL] == "1")
        ip_addr = conf.data[Params.IP_ADDR]
        port = conf.data[Params.PORT]
        encryption = (conf.data[Params.ENCRYPTION] == "1")
        cli_id = conf.data[Params.ID]
        auth = (conf.data[Params.AUTHENTICATION] == "1")


        if (type(ip_addr) != str):
            ip_addr = str(ip_addr)
        if (type(port) != int):
            port = int(port)
        if (type(cli_id) != str):
            cli_id = str(cli_id)

        #self.sonar = PI_Sonar_Monitor()
        #self.adc = PI_ADC_MONITOR()
        self.sensors = PI_SensorManager()

        #sensor thread moved inside of monitor thread
        #start_new_thread(self.sensor_thread,())


        self.local = local
        channels = 16
        self.robot = PI_ServoController(channels) # Start servo controller with 16 channels
        #Start remote thread
        if (self.local == False):
            self.cli = PI_Cli(ip_addr, port, encryption, auth, cli_id)
            #start_new_thread(self.command_thread,())
            if (auth == True):
                self.associated_clients = []

        #start command thread
        #start_new_thread(self.local_command_thread,())
        #start_new_thread(self.command_thread,())
        #print("Client -- " + cli_id + " -- online.")
        self.left_psr = 0
        self.right_psr = 0

        self.ROBOT_INTIALIZED = True
        #start command thread - Calling as function instead to prevent opening a new thread
        #start_new_thread(self.local_command_thread,())
        self.command_thread()



    #get msg, parse msg
    def command_thread(self):
        print("Client -- " + self.cli.name + " -- online.")
        self.parse("obcl")
        if (self.local == False):
            while True:

                if (self.ROBOT_INTIALIZED == True):
                    #could optimize by setting a sleep call here (latency from cli end)

                    msg = self.cli.Recv_Msg()
                    if (len(msg) >0):
                        if (self.cli.auth == True):
                            #send only the message to be parsed
                            in_cmd = msg.split(":")
                            self.add_associated_client(in_cmd[0])
                            self.parse(in_cmd[1])
                        else:
                            #relay msg to robot
                            self.parse(msg)
                    try:

                        if self.streaming == True:
                            #time.sleep(0.1) # send every 100 ms or so
                            #get data
                            stream_str = ""
                            self.send_associated_clients(stream_str)
                    except Exception as e:
                        print(e)

                    #sensors
                    #sonar
                    try:
                        sonar_cmds = self.sensors.detect_sonar()
                        for sonar_cmd in sonar_cmds:
                            self.parse(sonar_cmd)
                    #adc
                        adc_cmds = self.sensors.detect_adc()
                        for adc_cmd in adc_cmds:
                            self.parse(adc_cmd)
                    except Exception as e:
                        print(e)
                        os._exit(0)

        else:
            while True:
                if (self.ROBOT_INTIALIZED == True):
                    msg = sys.stdin.readline()
                    if (len(msg) >0):
                        #relay to robot
                        self.parse(msg)

#    def local_command_thread(self):
#        while True:
#            msg = sys.stdin.readline()
#            if (msg[:4].lower() == "exit"):
#                os._exit(0)
#            elif (len(msg) >0):
#                #relay to robot
#                if (self.ROBOT_INTIALIZED == True):
#                    self.parse(msg)

#    def stream_thread(self):
#        while self.streaming == True:
#            if (self.ROBOT_INTIALIZED == True):
#                time.sleep(0.1) # send every 100 ms or so
#                #get data
#                stream_str = ""
#                self.send_associated_clients(stream_str)

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
        self.send_associated_clients("grabfinish")

    #   Sends to all registered clients who have sent a msg to robot
    def send_associated_clients(self, message):
        if (self.local == False):
            if (self.cli.auth == True):
                if(len(self.associated_clients)>0):
                    send_str = ",".join([client for client in self.associated_clients]) #relay message to all clients who have talked to us
                    send_str +=":" + message
                    self.cli.Send_Msg(send_str)
            else:
                self.cli.Send_Msg(message)
        else:
            print(message)

    #    Keeps track of associated clients who have sent us messages
    def add_associated_client(self, client):
        if (self.local == False):
            associated = False
            for cli in self.associated_clients:
                if (cli == client):
                    associated = True
                    break
            if (associated == False):
                print("Adding Client:",client)
                self.associated_clients.append(client)

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
                    "home":-2, "obst":-3, "obcl":-4, "sd":-5, "sdeg":-6, "print":-7, "pos":-8, "grab":-9, "lpsr":-10, "rpsr":-11, \
                    "begstr":-12, "endstr":-13, "terminate":-14 \
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
                    # begstr        => begin streaming data
                    # endstr        => end streaming data
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
                            pos = ", ".join([(("S" + str(servos.index) + "$" + str(servos.current_angle) + "$" + str(servos.target_angle))) for servos in self.robot.servo_list])
                            #pos = ""
                            #for servos in self.robot.servo_list:
                            #    pos+=("S" + str(servos.index) + "$" + str(servos.current_angle) + "$" + str(servos.target_angle)) # Ex. S0$100$180, s1$50$20, ...
                            #    pos+=(", ")
                            #cli.Send_Msg(pos[:-1]) #remove last char and relay to server
                            self.send_associated_clients(pos)
                    elif servo_index == -9:
                        start_new_thread(self.grab,())
                    elif (servo_index == -10 and index >0):
                        self.left_psr = int(command[:index])
                    elif (servo_index == -11 and index >0):
                        self.right_psr = int(command[:index])
                    elif (servo_index == -12):
                        if (self.streaming == False):
                            #start_new_thread(self.stream_thread,())
                            self.streaming = True
                    elif (servo_index == -13):
                        if (self.streaming == True):
                            self.streaming = False
                    elif (servo_index == -14):
                        os._exit(0)
                    elif (servo_index >=0 and index >0):
                        self.robot.set_servo_position(servo_index, command[:index]) # servo_index, servo_position
                    break

#    def sensor_thread(self):
#        while True:
#            if (self.ROBOT_INTIALIZED == True):
#                prev_sonar_bool = False
#                num_adc = self.adc.num_channels
#                half_num_adc = num_adc/2
#                prev_adc_left_count = 0
#                prev_adc_right_count = 0
#                #self.parse("0lpsr, 0rpsr") # handled at top
#                while True:
#                    sonar_bool = False
#                    for i in range(self.sonar.num_sensors):
#                        if (self.sonar.channel_triggered(i)):
#                            sonar_bool = True
#                    if (sonar_bool == True)and(prev_sonar_bool == False):
#                        self.parse("obst")
#                        prev_sonar_bool = True
#                    elif (sonar_bool == False)and(prev_sonar_bool == True):
#                        self.parse("obcl")
#                        prev_sonar_bool = False
#
#                    adc_left_count = 0
#                    adc_right_count = 0
#                    for i in range(num_adc):
#                        if (self.adc.channel_triggered(i)):
#                            if (i < half_num_adc):
#                                #left
#                                adc_left_count+=1
#                            else:
#                                #right
#                                adc_right_count+=1
#
#                    if (adc_left_count != prev_adc_left_count):
#                        parse_str = str(adc_left_count) + "lpsr"
#                        self.parse(parse_str)
#                        prev_adc_left_count = adc_left_count
#                    elif (adc_right_count != prev_adc_right_count):
#                        parse_str = str(adc_right_count) + "rpsr"
#                        self.parse(parse_str)
#                        prev_adc_right_count = adc_right_count
