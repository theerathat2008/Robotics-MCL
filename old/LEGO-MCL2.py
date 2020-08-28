import math
import random
import sys

from Robot import Robot

from particleData import *

import time

robot = Robot("B", "C")
robot.setMotorLimits(30, 720)


def navigateToWaypoint(x, y):
    position = particles.getCurrentPosition()
    currentX = position[0]
    currentY = position[1]
    currentAngle = position[2]

    distance = math.sqrt((x - currentX) ** 2 + (y - currentY) ** 2)

    if (abs(x - currentX) < 1):

        if (abs(y - currentY) < 1):
            return

        if (y - currentY > 0):

            computedAngle = (round(450 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            particles.update(0, computedAngle)

            runMCL()

        else:
            computedAngle = (round(630 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            particles.update(0, computedAngle)
            runMCL()

    elif (abs(y - currentY) < 1):

        if (x - currentX > 0):

            computedAngle = (round(360 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            particles.update(0, computedAngle)
            runMCL()

        else:
            computedAngle = (round(540 - currentAngle)) % 360
            robot.turnLeft(computedAngle)
            particles.update(0, computedAngle)
            runMCL()

    else:
        relativeAngle = math.degrees(math.atan((y - currentY) / (x - currentX)))
        computedAngle = 0

        if (x < currentX):
            if (y < currentY):
                computedAngle = relativeAngle + 180 - currentAngle
            else:
                computedAngle = relativeAngle + 90 - currentAngle
        else:
            if (y < currentY):
                computedAngle = relativeAngle + 270 - currentAngle
            else:
                computedAngle = relativeAngle - currentAngle

        robot.turnLeft(abs(computedAngle))
        particles.update(0, computedAngle)
        runMCL()

    moveSteps(distance)

def runMCL():
    print("Position before MCL: " + str(particles.getCurrentPosition()))
    print("Reading value from the sonar")
    time.sleep(1)
    # Get a value from the sonar
    z = robot.getDistance()
    print("Sonar value: " + str(z))
    time.sleep(1)
    print("Update likelihood")
    # Update the likelihood
    particles.updateLikelihood(z)
    time.sleep(1)
    print("Normalise")
    # Normalise
    particles.normalise()
    time.sleep(1)
    print("Resample")
    # Resample
    particles.resample()
    print("Position after MCL: " + str(particles.getCurrentPosition()))
    time.sleep(1)
    particles.draw()


def moveSteps(distance):
    SMALL_STEP = 20
    steps = int(distance / SMALL_STEP)
    remainder = distance % SMALL_STEP

    for i in range(steps):
        robot.moveForward(SMALL_STEP)

        # Update using odometry
        particles.update(SMALL_STEP, 0)
        particles.draw()
        time.sleep(0.5)

        runMCL()

    if (remainder is not 0):
        robot.moveForward(remainder)

        # Update using odometry
        particles.update(remainder, 0)

        runMCL()


particles = Particles()
particles.initialiseParticles(84, 30)
particles.draw()

navigateToWaypoint(84, 30)
navigateToWaypoint(180, 30)
navigateToWaypoint(180, 54)
navigateToWaypoint(138, 54)
navigateToWaypoint(138, 168)
navigateToWaypoint(114, 168)
navigateToWaypoint(114, 84)
navigateToWaypoint(84, 84)
navigateToWaypoint(84, 30)
