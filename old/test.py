import brickpi333 as brickpi3
import time
from Robot import Robot

robot = Robot("B", "C")
robot.setMotorLimits(30, 720)

robot.turnLeft(90)