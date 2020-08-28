import brickpi3
import math
import time
import random

BP = brickpi3.BrickPi3()
d = 5.7 # This is the diameter of the tyretyre_distance
turnConstant = 3.4
FULL_REVOLUTION = 360
LEFT_WHEEL = BP.PORT_B
RIGHT_WHEEL = BP.PORT_C

# Set motor limits
BP.set_motor_limits(LEFT_WHEEL, 70, 720)
BP.set_motor_limits(RIGHT_WHEEL, 70, 720)

# Set sensors
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)

def moveForward(distance):
    expectedPosition = distance * FULL_REVOLUTION / (d * math.pi)
    leftPosition = BP.get_motor_status(LEFT_WHEEL)[2]
    rightPosition = BP.get_motor_status(RIGHT_WHEEL)[2]

    BP.set_motor_position(LEFT_WHEEL, expectedPosition)
    BP.set_motor_position(RIGHT_WHEEL, expectedPosition)

    while(leftPosition < expectedPosition - 5 or rightPosition < expectedPosition - 5):
        leftPosition = BP.get_motor_status(LEFT_WHEEL)[2]
        rightPosition = BP.get_motor_status(RIGHT_WHEEL)[2]
        time.sleep(0.02)

def moveBackwards(distance):
    expectedPosition = -distance * FULL_REVOLUTION / (d * math.pi)
    leftPosition = BP.get_motor_status(LEFT_WHEEL)[2]
    rightPosition = BP.get_motor_status(RIGHT_WHEEL)[2]

    BP.set_motor_position(LEFT_WHEEL, expectedPosition)
    BP.set_motor_position(RIGHT_WHEEL, expectedPosition)

    while(leftPosition > expectedPosition + 0.5 or rightPosition > expectedPosition - 0.5):
        leftPosition = BP.get_motor_status(LEFT_WHEEL)[2]
        rightPosition = BP.get_motor_status(RIGHT_WHEEL)[2]
        time.sleep(0.02)

def turnLeft(angle):
    resetEncoder()

    expectedPosition = angle * turnConstant

    rightPosition = BP.get_motor_status(RIGHT_WHEEL)[2]
    leftPosition = BP.get_motor_status(LEFT_WHEEL)[2]

    BP.set_motor_position(LEFT_WHEEL, -expectedPosition)
    BP.set_motor_position(RIGHT_WHEEL, expectedPosition)

    while(leftPosition > -expectedPosition + 5 or rightPosition < expectedPosition - 5):
        rightPosition = BP.get_motor_status(RIGHT_WHEEL)[2]
        leftPosition = BP.get_motor_status(LEFT_WHEEL)[2]
        time.sleep(0.02)

    resetEncoder()

def turnRight(angle):
    resetEncoder()

    expectedPosition = angle * turnConstant

    rightPosition = -BP.get_motor_status(RIGHT_WHEEL)[2]
    leftPosition = BP.get_motor_status(LEFT_WHEEL)[2]

    BP.set_motor_position(LEFT_WHEEL, expectedPosition)
    BP.set_motor_position(RIGHT_WHEEL, -expectedPosition)
    
    while(leftPosition < expectedPosition - 5 and rightPosition > expectedPosition + 5):
        rightPosition = BP.get_motor_status(RIGHT_WHEEL)[2]
        leftPosition = BP.get_motor_status(LEFT_WHEEL)[2]
        time.sleep(0.02)

    resetEncoder()

def speedForward():
    BP.set_motor_dps(BP.PORT_B, FULL_REVOLUTION)
    BP.set_motor_dps(BP.PORT_C, FULL_REVOLUTION)

def stop():
    BP.set_motor_dps(LEFT_WHEEL, 0)
    BP.set_motor_dps(RIGHT_WHEEL, 0)
    resetEncoder()

def resetEncoder():
    BP.offset_motor_encoder(LEFT_WHEEL, BP.get_motor_encoder(LEFT_WHEEL))
    BP.offset_motor_encoder(RIGHT_WHEEL, BP.get_motor_encoder(RIGHT_WHEEL))

try:
    resetEncoder()
    moveForward(40)
    turnLeft(90)
    moveForward(40)
except KeyboardInterrupt:
    BP.reset_all()
