Table of Contents
----------------------------------------
I.	System Information and Description
II.	List of Files
III.	External Dependencies
IV.	Setup
V.	Configuration
VI.	Operation
VII.	Credit and Acknowledgements
VIII.	Known Bugs
IV.	Change Log

----------------------------------------
----------------------------------------
I. System Information and Description
----------------------------------------
----------------------------------------
a.	Name: A Framework for Deep Learning and Cloud Controlled Robotics
b.	Version: 0.0.1
c.	Platform: Raspbian Stretch (Raspberry Pi)
d.	Language: Python 3.5.3 (or higher)
e.	Hardware Used In Testing:
	i.	Raspberry Pi B
	ii.	Adafruit Servo Controller Hat
		a. https://www.adafruit.com/product/2327
	iii.	SainSmart 6DOF Robotic Arm
		a. https://www.amazon.com/SainSmart-Platform-Robotics-Compatible-Mega2560/dp/B01GJ5X128/ref=sr_1_fkmr0_4?s=electronics&ie=UTF8&qid=1549572797&sr=8-4-fkmr0&keywords=6dof+sainsmart+robotic+arm
	iv.	Custom Designed 5v/6A Battery Operated Power Supply
	v.	14.8V, 6500mAh Zeee Power Battery
f.	Goal: To create a flexible framework for controlling robotics
g.	Content:
	i.	Server/Client Socket Server classes used for remote communication
	ii.	Servo Control class used for servo movement to a specified degree position with configurable parameters and servo number
	iii.	RSA Encryption class for using RSA encryption methods
	iv.	AES Encryption class for using AES encryption methods
h.	Features:
	i.	Server/Client communication with optional RSA and AES encryption and hashing.
	ii.	Servo control with the ability to specify positions of multiple servos at once.
	iii.	Configurable degree steps for servo movement.
	iv.	Configurable duration for approximating the same arrival time for each servo (if capable).
	v.	Servo controller flag option for the Client program to allow communication with servos over WiFi
	vi.	Servo controller allows for changing and tracking of direction
	vii.	Servo controller allows the developer to specify a home position for a servo
	viii.	Servo controller allows the developer to specify the movement range of a servo
	ix.	Encryption protocol creates a randomly generated key for each client
	x.	Encryption initiation methods protect against messages sent by unapproved connections
	xi.	Encryption initiation methods protect messages from being heard by unapproved connections
	xii.	Encryption uses hashing to prevent messages from being tampered with

----------------------------------------
----------------------------------------
II. List of Files
----------------------------------------
----------------------------------------
a.	PI_Srvr.py
b.	PI_Cli.py
c.	PI_Servo.py
d.	PI_RSA.py
e.	PI_AES.py

----------------------------------------
----------------------------------------
III. External Dependencies
----------------------------------------
----------------------------------------
a.	Pycrypto
b.	Adafruit ServoKit

----------------------------------------
----------------------------------------
IV. Setup
----------------------------------------
----------------------------------------
a.	Raspberry Pi
	i.	Install Raspbian Stretch on Raspberry PI
		a. https://www.raspberrypi.org/downloads/raspbian/
	ii.	Install python
		a. sudo apt-get update
		b. sudo apt-get install python3
	iii.	Install Dependencies
		a. sudo pip3 install pycrypto
		b. sudo pip3 install adafruit-circuitpython-servokit
b.	Servo Hat
	i.	Assemble the Adafruit Servo Hat
	ii.	Follow instructions to get software set up:
		a. https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/overview
c.	Robotic Arm
	i.	Assemble the desired robotic arm and associated servos
	ii.	Connect robotic arm to servos
	iii.	Connect the servo hat to power

----------------------------------------
----------------------------------------
V. Configuration
----------------------------------------
----------------------------------------
a.	Configuring Servo Initialization Parameters
	i. ###TBD
b.	Configuring Server Parameters
	i. ###TBD
c.	Configuring Client Parameters
	i. ###TBD

----------------------------------------
----------------------------------------
VI. Operation
----------------------------------------
----------------------------------------
a.	Setting up Server
	i.	The Server program can be launched by entering a port number as a command line argument
		a. Ex. ./Server.py 10001
		b. Ex. ./Server.py - This will launch on a default port of 10001
b.	Setting up Client
	i.	The Client program can be launched by entering an ip address and a port number as command line arguments
		a. Ex. ./Client.py 127.0.0.1 10001
		b. Ex. ./Client.py - This will launch on a default ip of localhost (127.0.0.1) port of 10001
c.	Setting up RobotClient
	i.	The Robot Client program is launched similarly to the Client Program
		a. Ex. ./RobotClient.py 127.0.0.1 10001
		b. Ex. ./RobotClient.py - This will launch on a default ip of localhost (127.0.0.1) port of 10001
d.	Sending Commands
	i.	Using the Socket Server/Client, a command received by the robot client will automatically be sent to the robot.
e.	Valid Commands
	i.	Servo Movement - [servoPosition][servoIndex]
		a. Ex. 20a - Moves servo index 0 to position 20 degrees
		b. Servos that are currently active are a-f, additional servos will need to be added to parse function in PI_Servo.py
	ii.	Set Duration - [DurationInMS]sd
		a. Ex. 1000sd - Sets servo movement duration to 1.0 seconds
	iii.	Set Step Size (Degrees) - [StepSize]sdeg
		a. Ex. 5sdeg - Sets servo step size to 5 degrees
	iv.	Go Home - home
		a. Tells robot to go home
f.	Sending Multiple Commands
	i.	Multiple commands can be sent by separating each command with a comma and a space.
		a. Ex. 1000sd, 5sdeg, 120a, 20b, 20c, 50d, 80e, 30f
	ii.	Commands are processed in order.

----------------------------------------
----------------------------------------
VII. Credits and Acknowledgements
----------------------------------------
----------------------------------------
a.	Author: Jonathan Dean
b.	Team Lead: John Zoodsma
c.	University: Tennessee Technological University
d.	Department: Department of Computer and Electrical Engineering
e.	Professor: Dr. Hasan
f.	Code Authors:
	i.	Jonathan Dean
	ii.	John Zoodsma
	iii.	Slade Spry
g.	Contributors:
	i.	Jonathan Dean
	ii.	John Zoodsma
	iii.	Slade Spry
	iv.	John Dickinson
h.	Code Resources:
	i.	Adafruit Industries
	ii.	Raspberry Pi
	iii.	PyPI
	iv.	Geeks For Geeks

----------------------------------------
----------------------------------------
VIII. Known Bugs
----------------------------------------
----------------------------------------
a.	Server hangs on Unencrypted Client Connection
	i.	Need to fix unencrypted side of server/client
	ii.	Not an issue on encrypted (default) client
----------------------------------------
----------------------------------------
IX. Change Log
----------------------------------------
----------------------------------------
	02/07/2019 	Initial Document Creation