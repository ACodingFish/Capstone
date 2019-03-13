
def __init__(self)
    self.servo_controller = PI_ServoController(16) # Start servo controller with 16 channels

#get msg, parse msg
self.servo_controller.parse(self.in_msg)