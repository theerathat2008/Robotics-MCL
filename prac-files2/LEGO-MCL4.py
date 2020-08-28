import math
import random
import sys

from Robot import Robot

from particleData import *

import time

DESIRED_DISTANCE = -20
KP = 20
centerToSensor = 10.5

robot = Robot("B", "C")
robot.setMotorLimits(30, 720)
robot.setSonarLimit(10, 180)

POINTS = [(84, 30), (180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84), (84, 84), (84, 30)]

# First object
robot.stepToWaypoint(65, 30, sys.maxsize)
#robot.turnRight(180)
robot.speedVelocity(100, 100)
robot.findObjectContinuous("right")
robot.stop()
robot.moveForward(10)
robot.turnRight(90)
robot.hitObject(DESIRED_DISTANCE, KP, 0)
print("beans")
robot.moveBackwards(60)
#robot.stepToWaypoint(50, 70, sys.maxsize)
#robot.stepToWaypoint(70, 70, sys.maxsize)
#robot.stepToWaypoint(80, 70, sys.maxsize)
robot.turnRight(99)
robot.moveForward(60)
robot.turnSonar(-90)
d = robot.getDistance()
robot.turnSonar(90)

#x, y, t = robot.particles.getCurrentPosition()
#robot.EXPECTED_VALUE = 210 - x
robot.EXPECTED_VALUE = 210 - d 
robot.speedVelocity(100, 100)
robot.findObjectContinuous("left")
robot.stop()
robot.moveForward(20)
robot.turnLeft(90)
robot.hitObject(DESIRED_DISTANCE, KP, 0)
print("beans2")

robot.turnSonar(-180)
robot.moveBackwards(10)
robot.turnRight(190)
d = robot.getDistance()
robot.moveForward(d - 60)
# Second object

robot.turnSonar(-90)
d = robot.getDistance()
robot.turnSonar(90)

robot.EXPECTED_VALUE = 210 - d
robot.speedVelocity(100, 100)
robot.findObjectContinuous("left")
robot.stop()
robot.moveForward(20)
robot.turnLeft(90)
robot.hitObject(DESIRED_DISTANCE, KP, 0)

d = robot.getDistance()
robot.moveBackwards(d-84)
"""
robot.turnLeft(180)
forwardDistance = robot.getDistance()
robot.turnSonar(-90)
rightDistance = robot.getDistance()

x = rightDistance + centerToSensor
y = forwardDistance + centerToSensor

diffX = 90 - x
diffY = y - 60

robot.moveForward(diffY)
robot.turnLeft(90)
robot.moveForward(diffX)

robot.turnSonar(180)
robot.findObjectContinuous()
robot.speedVelocity(100, 100)
robot.stop()
robot.moveForward(1)
robot.turnLeft(90)
robot.hitObject(DESIRED_DISTANCE, KP, 0)
"""

# First object
#robot.stepToWaypoint(120, 30, sys.maxsize)
#robot.stepToWaypoint(122, 30, sys.maxsize)
#x, y, theta = robot.findObject()
#print("Theta: " + str(theta))
#robot.hitObject(DESIRED_DISTANCE, KP, theta)

# Second object
#robot.stepToWaypoint(120, 30, sys.maxsize)
#robot.stepToWaypoint(120, 100, sys.maxsize)
#x, y, theta = robot.findObject()
#robot.hitObject(DESIRED_DISTANCE, KP, theta)

# Third object
#robot.stepToWaypoint(120, 100, sys.maxsize)
#robot.stepToWaypoint(100, 100, sys.maxsize)
#robot.stepToWaypoint(84, 100, sys.maxsize)
#x, y, theta = robot.findObject()
#if (theta < 2):
    #robot.stepToWaypoint(100, 100, sys.maxsize)
    #robot.stepToWaypoint(100, 102, sys.maxsize)
    #x, y, theta = robot.findObject()
    #robot.hitObject(DESIRED_DISTANCE, KP, theta)
#else:
    #robot.hitObject(DESIRED_DISTANCE, KP, theta)


