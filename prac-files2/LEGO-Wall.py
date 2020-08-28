import statistics
import sys
import time
from queue import Queue

from Robot import Robot

import brickpi3

DESIRED_DISTANCE = 30
KP = 5
VC = 720

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
            leftVelocity = VC - (KP * (DESIRED_DISTANCE - actualDistance)) / 2
            rightVelocity = VC + (KP * (DESIRED_DISTANCE - actualDistance)) / 2
            robot.speedVelocity(leftVelocity, rightVelocity)

            print("Measured distance: " + str(actualDistance))
            print("Desired distance: " + str(DESIRED_DISTANCE))
            print("Left velocity: " + str(leftVelocity))
            print("Right velocity: " + str(rightVelocity))

            readings.get()

        except brickpi3.SensorError as error:
            print(error)

        time.sleep(0.02)

except KeyboardInterrupt:
    robot.resetAll()