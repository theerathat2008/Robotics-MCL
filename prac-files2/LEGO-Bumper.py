import brickpi3
import math
import time
import random

BP = brickpi3.BrickPi3()
d = 5.7 # This is the diameter of the tyretyre_distance
turnConstant = 3.4
FULL_REVOLUTION = 360

BP.set_motor_limits(BP.PORT_B, 70, 720)
BP.set_motor_limits(BP.PORT_C, 70, 720)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)

def moveForward(distance, last):
    revolution = distance * FULL_REVOLUTION / (d * math.pi)
    BP.set_motor_position(BP.PORT_B, revolution)
    BP.set_motor_position(BP.PORT_C, revolution)

    while(True):
        currentRevolution = BP.get_motor_status(BP.PORT_B)[2]
        if (currentRevolution > revolution - 5):
            break;

    if (not last):
        resetEncoder()

def moveBackwards(distance, last):
    revolution = distance * FULL_REVOLUTION / (d * math.pi)
    BP.set_motor_position(BP.PORT_B, -revolution)
    BP.set_motor_position(BP.PORT_C, -revolution)

    while(True):
        currentRevolution = -BP.get_motor_status(BP.PORT_B)[2]
        if (currentRevolution > revolution - 5):
            break;

    if (not last):
        resetEncoder()

def turnLeft(angle, last):
    degree = angle * turnConstant

    BP.set_motor_position(BP.PORT_B, -degree)
    BP.set_motor_position(BP.PORT_C, degree)

    while(True):
        currentRevolution = BP.get_motor_status(BP.PORT_C)[2]
        if (currentRevolution > degree - 5):
            break;

    if (not last):
        resetEncoder()

def turnRight(angle, last):
    degree = angle * turnConstant

    BP.set_motor_position(BP.PORT_B, degree)
    BP.set_motor_position(BP.PORT_C, -degree)
    
    while(True):
        currentRevolution = BP.get_motor_status(BP.PORT_B)[2]
        if (currentRevolution > degree - 5):
            break;

    if (not last):
        resetEncoder()

def speedForward():
    BP.set_motor_dps(BP.PORT_B, FULL_REVOLUTION)
    BP.set_motor_dps(BP.PORT_C, FULL_REVOLUTION)

def stop():
    BP.set_motor_dps(BP.PORT_B, 0)
    BP.set_motor_dps(BP.PORT_C, 0)
    resetEncoder()

def resetEncoder():
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

try:
    resetEncoder()
    speedForward()
    while(True):
        try:
            rightSensor = BP.get_sensor(BP.PORT_1)
            leftSensor = BP.get_sensor(BP.PORT_2)

            if(rightSensor or leftSensor):
                stop()
                moveBackwards(5, False)
                angle = random.randint(20, FULL_REVOLUTION / 4)

                if(rightSensor):
                    turnLeft(angle, False)
                if(leftSensor):
                    turnRight(angle, False)
                else:
                    goLeft = random.randint(0, 1)

                    if(goLeft):
                        turnLeft(angle, False)
                    else:
                        turnRight(angle, False)

                speedForward()
        except brickpi3.SensorError as error:
           print(error)
        time.sleep(0.02)
except KeyboardInterrupt:
    BP.reset_all()
