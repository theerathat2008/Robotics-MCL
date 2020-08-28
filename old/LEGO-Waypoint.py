import math
import random
import statistics

from Robot import Robot

from Particle import Particle


import time

NUM_OF_PARTICLES = 100
particles = [0] * NUM_OF_PARTICLES

robot = Robot("B", "C")
robot.setMotorLimits(30, 720)


def initialiseParticles():
    for i in range(NUM_OF_PARTICLES):
        particles[i] = Particle(0, 0, 0, 1 / NUM_OF_PARTICLES)

def calculateCurrentPosition():
    currentPositionX = sum([particle.toTuple()[0] * particle.toTuple()[3] for particle in particles])
    currentPositionY = sum([particle.toTuple()[1] * particle.toTuple()[3] for particle in particles])
    currentAngle = sum([particle.toTuple()[2] * particle.toTuple()[3] for particle in particles])
    return (currentPositionX, currentPositionY, currentAngle)

def updateParticles(distance, angle):
    if angle == 0:
        e = random.gauss(0, 1)
        f = random.gauss(0, 0.05)

        for i in range(NUM_OF_PARTICLES):
            particles[i].updateParticle(particles[i].weight, distance, [0, 0, 0], angle)
    else:
        g = random.gauss(0, 2)

        for i in range(NUM_OF_PARTICLES):

            particles[i].updateParticle(particles[i].weight, distance, [0, 0, 0], angle)

def navigateToWaypoint(x, y):

    position = calculateCurrentPosition()
    currentX = position[0]
    currentY = position[1]
    currentAngle = position[2]

    distance = math.sqrt((x-currentX) ** 2+(y-currentY) ** 2)

    if (abs(x - currentX) < 0.001):

        if (abs(y - currentY) < 0.001):
            print("No movement")
            return

        print("Firt if")

        if (y - currentY > 0):
            print("Hello")

            computedAngle = (round(450 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            updateParticles(0, computedAngle)

            print(str(currentAngle))
            print(str(computedAngle))
        else:
            computedAngle = (round(630 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            updateParticles(0, computedAngle)

    elif (abs(y - currentY) < 0.001):

        if (x - currentX > 0):
            print("Hello")

            computedAngle = (round(360 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            updateParticles(0, computedAngle)

            print(str(currentAngle))
            print(str(computedAngle))
        else:
            computedAngle = (round(540 - currentAngle)) % 360
            robot.turnLeft(computedAngle)
            updateParticles(0, computedAngle)
    else:
        relativeAngle = math.degrees(math.atan((y-currentY)/(x-currentX)))
        computedAngle = 0

        if(x < currentX):
            if(y < currentY):
                computedAngle = relativeAngle + 180 - currentAngle
            else:
                computedAngle = relativeAngle + 90 - currentAngle
        else:
            if(y < currentY):
                computedAngle = relativeAngle + 270 - currentAngle
            else:
                computedAngle = relativeAngle - currentAngle

        print(str(computedAngle))

        robot.turnLeft(abs(computedAngle))
        updateParticles(0, computedAngle)


    robot.moveForward(distance)

    updateParticles(distance, 0)

    print(str(calculateCurrentPosition()))






initialiseParticles()

# Estimate current position by taking the mean of all the particles

while True:

    try:

        print("Please input two coordinates: ")

        target = input().split()

        x = float(target[0])
        y = float(target[1])

        navigateToWaypoint(float(x), float(y))

    except KeyboardInterrupt:
        robot.resetAll()
        exit()