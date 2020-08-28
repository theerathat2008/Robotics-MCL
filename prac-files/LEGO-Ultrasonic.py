import statistics
import sys
import time
import os
from queue import Queue

from Robot import Robot

import brickpi3

DESIRED_DISTANCE = 30
KP = 10

robot = Robot("B", "C")
robot.setMotorLimits(70, 720)

try:

    readings = Queue(3)
    readings.put(sys.maxsize)
    readings.put(-sys.maxsize - 1)

    while True:
        try:
            # Get actual distance from the wall
            actualDistance = robot.getDistance()

            # Put it into the readings queue
            readings.put(actualDistance)

            # Take the mean
            actualDistance = statistics.median(list(readings.queue))

            # Set the speed accordingly
            negativeError = DESIRED_DISTANCE - actualDistance
            velocity = -KP * negativeError
            robot.speedVelocity(velocity)

            print("Measured distance: " + str(actualDistance))
            print("Desired distance: " + str(DESIRED_DISTANCE))
            print("Desired distance - Measured distance: " + str(negativeError))
            print("Calculated motor control speed: " + str(velocity))

            readings.get()

        except brickpi3.SensorError as error:
            print(error)

        time.sleep(0.02)

except KeyboardInterrupt:
    robot.resetAll()