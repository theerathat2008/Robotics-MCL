import brickpi3 # import the BrickPi3 drivers
import math
import time

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
d = 5.7 # This is the diameter of the tire
tyre_distance = 6.0
turn_constant = 3

BP.set_motor_limits(BP.PORT_B, 70, 1080)
BP.set_motor_limits(BP.PORT_C, 70, 1080)

def moveForward(distance):
    revolution = distance * 360 / (d * math.pi)
    
    BP.set_motor_position(BP.PORT_B, -revolution)
    BP.set_motor_position(BP.PORT_C, -revolution)

def turn(angle):
    BP.set_motor_position(BP.PORT_B, -angle * 6 / 5.7)
    BP.set_motor_position(BP.PORT_C, angle * 6/5.7)

def resetEncoder():
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

try:
    resetEncoder()

    turn(90)
    

except KeyboardInterrupt:
    BP.reset_all()
