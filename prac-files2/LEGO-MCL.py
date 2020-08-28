import math
import random

from Robot import Robot

from Particle import Particle

import time

robot = Robot("B", "C")
robot.setMotorLimits(30, 720)

centerToSensor = 8.5
sd = 2.5

# probability of returning garbage value
k = 0.01

def calculate_likelihood(x, y, theta, z):
    # Find out what wall the sonar will hit
    wall = checkWalls(x, y, theta, [WALL_A, WALL_B, WALL_C, WALL_D, WALL_E, WALL_F, WALL_G, WALL_H])
    m = wall[1]
    likelihoodFactor = math.exp(-((z + centerToSensor - m) ** 2)/(2 * (sd**2))) + k
    print(str(wall))

    return likelihoodFactor

def readSonarValue():
    try:
        return robot.getDistance()
    except KeyboardInterrupt as error:
        robot.resetAll()

def navigateToWaypoint(x, y):
    position = particles.calculateCurrentPosition()
    print("Current position: " + str(position))
    currentX = position[0]
    currentY = position[1]
    currentAngle = position[2]

    distance = math.sqrt((x-currentX) ** 2+(y-currentY) ** 2)

    if (abs(x - currentX) < 3):

        if (abs(y - currentY) < 3):
            return

        if (y - currentY > 0):

            computedAngle = (round(450 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            # Update using odometry
            particles.update(0, computedAngle)

            # Read a value from the sonar
            z = readSonarValue()

            # Update the particles
            likelihood = calculate_likelihood(currentX, currentY, currentAngle, z)
            particles.updateLikelihood(likelihood)

            particles.draw()

            time.sleep(1)
        else:
            computedAngle = (round(630 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            # Update using odometry
            particles.update(0, computedAngle)

            # Read a value from the sonar
            z = readSonarValue()

            # Update particles
            likelihood = calculate_likelihood(currentX, currentY, currentAngle, z)

            particles.updateLikelihood(likelihood)
            particles.draw()

            time.sleep(1)
    elif (abs(y - currentY) < 3):

        if (x - currentX > 0):

            computedAngle = (round(360 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            # Update using odometry
            particles.update(0, computedAngle)

            # Read a value from the sonar
            z = readSonarValue()

            # Update the particles
            likelihood = calculate_likelihood(currentX, currentY, currentAngle, z)
            particles.updateLikelihood(likelihood)

            particles.draw()

            time.sleep(1)
            time.sleep(1)

        else:
            computedAngle = (round(540 - currentAngle)) % 360
            robot.turnLeft(computedAngle)

            # Update using odometry
            particles.update(0, computedAngle)

            # Read a value from the sonar
            z = readSonarValue()

            # Update the particles
            likelihood = calculate_likelihood(currentX, currentY, currentAngle, z)
            particles.updateLikelihood(likelihood)

            particles.draw()

            time.sleep(1)

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


        robot.turnLeft(abs(computedAngle))

        # Update using odometry
        particles.update(0, computedAngle)

        # Read a value from the sonar
        z = readSonarValue()

        # Update the particles
        likelihood = calculate_likelihood(currentX, currentY, currentAngle, z)
        particles.updateLikelihood(likelihood)

        particles.draw()

        time.sleep(1)

    SMALL_STEP = 20
    steps = int(distance / SMALL_STEP)
    remainder = distance % SMALL_STEP

    for i in range(steps):
        robot.moveForward(SMALL_STEP)

        # Update using odometry
        particles.update(SMALL_STEP, 0)
        particles.draw()
        time.sleep(0.5)

        # Read a value from the sonar
        z = readSonarValue()

        # Compute the likelihood
        likelihood = calculate_likelihood(currentX, currentY, currentAngle, z)

        # Update the particles
        particles.updateLikelihood(likelihood)

        particles.draw()

        time.sleep(1)

    if (remainder is not 0):
        robot.moveForward(remainder)

        # Update using odometry
        particles.update(remainder, 0)

        # Read a value from the sonar
        z = readSonarValue()

        # Compute the likelihood
        likelihood = calculate_likelihood(currentX, currentY, currentAngle, z)

        # Update the particles
        particles.updateLikelihood(likelihood)

        particles.draw()

        time.sleep(1)

def checkWalls(x, y, theta, walls):
    candidateWalls = []

    for wall in walls:
        AX = wall[0]
        AY = wall[1]
        BX = wall[2]
        BY = wall[3]

        m = ((BY - AY) * (AX - x) - (BX - AX) * (AY - y)) / (BY - AY) * math.cos(math.radians(theta)) - (BX - AX) * math.sin(math.radians(theta))

        intersectionX = x + m * math.cos(math.radians(theta))
        intersectionY = y + m * math.sin(math.radians(theta))

        if (intersectionX == x and min(AY, BY) <= y and y <= max(AY, BY)):
            candidateWalls.append((wall, m))
        elif (intersectionY == y and min(AX, BX) <= x and x <= max(AX, BX)):
            candidateWalls.append((wall, m))

        return minimumCandidateWall(candidateWalls)

def minimumCandidateWall(candidateWalls):
    m = 0
    minimumWall = (0, 0, 0, 0)

    for wall in candidateWalls:
        if (wall[1] < m):
            m = wall[1]
            minimumWall = wall

    return minimumWall

# A Canvas class for drawing a map and particles:
# 	- it takes care of a proper scaling and coordinate transformation between
#	  the map frame of reference (in cm) and the display (in pixels)
class Canvas:
    def __init__(self, map_size=210):
        self.map_size = map_size  # in cm
        self.canvas_size = 768  # in pixels
        self.margin = 0.05 * map_size
        self.scale = self.canvas_size / (map_size + 2 * self.margin)

    def drawLine(self, line):
        x1 = self.__screenX(line[0])
        y1 = self.__screenY(line[1])
        x2 = self.__screenX(line[2])
        y2 = self.__screenY(line[3])
        print("drawLine:" + str((x1, y1, x2, y2)))

    def drawParticles(self, data):
        display = [(self.__screenX(d[0]), self.__screenY(d[1])) + d[2:] for d in data]
        print("drawParticles:" + str(display))

    def __screenX(self, x):
        return (x + self.margin) * self.scale

    def __screenY(self, y):
        return (self.map_size + self.margin - y) * self.scale


# A Map class containing walls
class Map:
    def __init__(self):
        self.walls = []

    def add_wall(self, wall):
        self.walls.append(wall)

    def clear(self):
        self.walls = []

    def draw(self):
        for wall in self.walls:
            canvas.drawLine(wall)


# Simple Particles set
class Particles:
    NUM_OF_PARTICLES = 100

    def __init__(self):
        self.n = self.NUM_OF_PARTICLES
        self.data = [0] * self.NUM_OF_PARTICLES

    def initialise(self):
        for i in range(self.n):
            self.data[i] = Particle(84, 30, 0, 1 / self.n)

    def update(self, distance, angle):
        if angle == 0 and distance == 0:
            return

        if angle == 0:

            for i in range(self.n):
                e = random.gauss(0, 0.51)

                f = random.gauss(0, 2.1)

                self.data[i].updateParticle(self.data[i].getWeight(), distance, [e, f, 0], angle)
        else:
            for i in range(self.n):
                g = random.gauss(0,11.3)
                self.data[i].updateParticle(self.data[i].getWeight(), distance, [0, 0, g], angle)

    def updateLikelihood(self, likelihood):

        for i in range(self.n):
            self.data[i].updateParticle(likelihood * self.data[i].getWeight(), 0, [0, 0, 0], 0)

        self.__normalise()

        self.__resample()

    def __normalise(self):
        totalWeight = sum([particle.toTuple()[3] for particle in self.data])
        self.data = [Particle(particle.toTuple()[0], particle.toTuple()[1], particle.toTuple()[2], particle.toTuple()[3] / totalWeight) for particle in self.data]

    def __resample(self):

        # Cumulative weight array
        cumulativeWeight = [0] * self.n

        cumulativeWeight[0] = self.data[0].toTuple()[3]

        for i in range(1,self.n):
            cumulativeWeight[i] = cumulativeWeight[i-1] + self.data[i].toTuple()[3]

        newData = [0] * self.n

        for i in range(self.n):
            num = random.randint(0, 1)
            for j in range(self.n):
                if(num < cumulativeWeight[j]):
                    newData[i] = self.__copyParticle(self.data[j])
                    break

        self.data = newData

    def __copyParticle(self, particle):
        return Particle(particle.toTuple()[0], particle.toTuple()[1], particle.toTuple()[2], 1/self.n)

    def draw(self):
        canvas.drawParticles([particle.toTuple() for particle in self.data])

    def calculateCurrentPosition(self):
        currentPositionX = sum([particle.toTuple()[0] * particle.toTuple()[3] for particle in self.data])
        currentPositionY = sum([particle.toTuple()[1] * particle.toTuple()[3] for particle in self.data])
        currentAngle = sum([particle.toTuple()[2] * particle.toTuple()[3] for particle in self.data])
        return (currentPositionX, currentPositionY, currentAngle)


canvas = Canvas()  # global canvas we are going to draw on

mymap = Map()
# Definitions of walls
# a: O to A
# b: A to B
# c: C to D
# d: D to E
# e: E to F
# f: F to G
# g: G to H
# h: H to O
WALL_A = (0, 0, 0, 168)
mymap.add_wall(WALL_A)  # a
WALL_B = (0, 168, 84, 168)
mymap.add_wall(WALL_B)  # b
WALL_C = (84, 126, 84, 210)
mymap.add_wall(WALL_C)  # c
WALL_D = (84, 210, 168, 210)
mymap.add_wall(WALL_D)  # d
WALL_E = (168, 210, 168, 84)
mymap.add_wall(WALL_E)  # e
WALL_F = (168, 84, 210, 84)
mymap.add_wall(WALL_F)  # f
WALL_G = (210, 84, 210, 0)
mymap.add_wall(WALL_G)  # g
WALL_H = (210, 0, 0, 0)
mymap.add_wall(WALL_H)   # h
mymap.draw()

particles = Particles()
particles.initialise()

print("1")
navigateToWaypoint(180, 30)
print("2")
navigateToWaypoint(180, 54)
print("3")
navigateToWaypoint(138, 54)
print("4")
navigateToWaypoint(138, 168)
print("5")
navigateToWaypoint(114, 168)
navigateToWaypoint(114, 84)
navigateToWaypoint(84, 84)
navigateToWaypoint(84, 30)