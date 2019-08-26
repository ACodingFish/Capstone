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
	iii.	Configurable degree steps for servo movement
	iv.	Configurable duration for approximating the same arrival time for each servo (if capable).
	v.	Servo controller flag option for the Client program to allow communication with servos over WiFi
	vi.	Servo controller allows for changing and tracking of direction
	vii.	Servo controller allows the developer to specify a home position for a servo
	viii.	Servo controller allows the developer to specify the movement range of a servo
	ix.	Encryption protocol creates a randomly generated key for each client
	x.	Encryption initiation methods protect against messages sent by unapproved connections
	xi.	Encryption initiation methods protect messages from being heard by unapproved connections
	xii.	Encryption uses hashing to prevent messages from being tampered with
	xiii.	Sensors for protection methods
	xiv.	Sensors for floor detection (dropping objects)
	xv.	Sensors for detecting pressure (grabbing objects)
	xvi.	Configuration files for easy setup of new servers and clients
	xvii.	Authentication for routing and security purposes
	xviii.	Robot Manager to manage all robot control operations.
	xviv.	Sensor Manager to manage the sensors and help generate commands for sensors.

----------------------------------------
----------------------------------------
II. List of Files
----------------------------------------
----------------------------------------
a.	Classes
	i.	PI_Srvr.py
	ii.	PI_Cli.py
	iii.	PI_Servo.py
	iv.	PI_RSA.py
	v.	PI_AES.py
	vi.	PI_Sonar.py
	vi.	PI_ADC.py
	vii.	PI_Conf.py
	viii.	PI_RobotManager.py
	viv.	PI_SensorManager.py
b.	Scripts
	i.	Client.py
	ii.	LocalClient.py
	iii.	RobotClient.py
	iv.	Server.py
c.	Config Files
	i.	conf/cli.conf
	ii.	conf/loc.conf
	iii.	conf/rob.conf
	iv.	conf/srvr.conf

----------------------------------------
----------------------------------------
III. External Dependencies
----------------------------------------
----------------------------------------
a.	Pycrypto (or pycryptodome for PC)
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
d.	Sensors
	i.	Sonar sensors are mounted on front, left, and right side of robotic arm
	ii.	ADC sensors are clipped to the inside of the robot's claw.
e.	Configuration Files
	i. 	LOCAL (0 or 1) - Non functional at the moment due to thread reduction, leave as 0
	ii. 	IP Address - Specifies the IP address of the server for client configuration files. (127.0.0.1 is localhost)
	iii. 	Port - Specifies port number that the server is bound on
	iv.	Encryption (0 or 1) - 1 enables encryption, 0 disables - Authentication will enable encryption by default, 0 is untested
	v.	ID - Specifies the name of the server or client
	vi.	Authentication (0 or 1) - 1 enables authentication, 0 disables - 0 is untested

----------------------------------------
----------------------------------------
V. Configuration
----------------------------------------
----------------------------------------
a.	Configuring Servo Initialization Parameters
	i.	Step length
		a. Change the value of step_len in the PI_ServoController __init__ function in PI_Servo.py
		b. This changes how much the servo moves every step.
	ii.	Movement Duration
		a. Change the value of mov_duration in the PI_ServoController __init__ function in PI_Servo.py
		b. This changes how long it takes for a movement to complete (in seconds)
	iii.	Adding Servos
		a. Servos are added in the list sv_info in PI_ServoController __init__ function
		b. Four parameters are added in a list within the list sv_info.
		c. The first parameter is the movement range in degrees of the servo.
		d. The second parameter is the home position in degrees of the servo.
		e. The third parameter is the maximum degree position of the servo.
		f. The fourth parameter is the minimum degree position of the servo.
	iv.	Adding sensors
		a. Initialization arrays similar to Adding servos can be found in PI_Sonar.py

----------------------------------------
----------------------------------------
VI. Operation
----------------------------------------
----------------------------------------
a.	Setting up Server
	i.	The Server program can be launched using specified info from its config file.
		a. Ex. ./Server.py
b.	Setting up Client
	i.	The Client program can be launched using specified info from its config file.
		a. Ex. ./Client.py
c.	Setting up RobotClient
	i.	The Robot Client program can be launched using specified info from its config file.
		a. Ex. ./RobotClient.py
d.	Sending Commands
	i.	Using the Socket Server/Client, a command received by the robot client will automatically be sent to the robot.
	ii.	If authentication is active, then it will keep track of which clients have sent messages to it and only stream data back to the proper clients.
		a. i.e. the clients who have sent a message to it before.
e.	Valid Commands
	i.	Servo Movement - [servoPosition][servoIndex]
		a. Ex. 20a - Moves servo index 0 to position 20 degrees
		b. Servos that are currently active are a-f, additional servos will need to be added to parse function in PI_Servo.py
	ii.	Set Duration - [DurationInMs]sd
		a. Ex. 1000sd - Sets servo movement duration to 1.0 seconds
	iii.	Set Step Size (Degrees) - [StepSize]sdeg
		a. Ex. 5sdeg - Sets servo step size to 5 degrees
	iv.	Go Home - home
		a. Tells robot to go home
f.	Sending Multiple Commands
	i.	Multiple commands can be sent by separating each command with a comma and a space.
		a. Ex. 1000sd, 5sdeg, 120a, 20b, 20c, 50d, 80e, 30f
	ii.	Commands are processed in order.
g.	All of the valid commands can be seen in the parse function within PI_RobotManager.py

----------------------------------------
----------------------------------------
VII. Credits and Acknowledgements
----------------------------------------
----------------------------------------
a.	Author: Jonathan Dean
b.	Team Lead: John Zoodsma
c.	University: Tennessee Technological University
d.	Department: Department of Computer and Electrical Engineering
e.	Professors: Dr. Hasan, Dr. Guo
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
a.	Possible bugs in unencrypted/unauthenticated version of client/server programs (Untested).

----------------------------------------
----------------------------------------
IX. Change Log
----------------------------------------
----------------------------------------
	04/24/2019	Documentation Update for end of semester
	02/07/2019 	Initial Document Creation