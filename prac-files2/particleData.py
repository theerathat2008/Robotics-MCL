#!/usr/bin/env python 

# Some suitable functions and data structures for drawing a map and particles
import sys
import time
import random
import math

import copy
import numpy as np

from Particle import Particle

centerToSensor = 10.5
sigma = 2
sonarMaxAngle = 25 * math.pi / 180
sonarMaxDistance = 200

# probability of returning garbage value
k = 0.018

# A Canvas class for drawing a map and particles:
#     - it takes care of a proper scaling and coordinate transformation between
#      the map frame of reference (in cm) and the display (in pixels)
class Canvas:
    def __init__(self,map_size=210):
        self.map_size    = map_size     # in cm
        self.canvas_size = 768          # in pixels
        self.margin      = 0.05*map_size
        self.scale       = self.canvas_size/(map_size+2*self.margin)

    def drawLine(self,line):
        x1 = self.__screenX(line[0])
        y1 = self.__screenY(line[1])
        x2 = self.__screenX(line[2])
        y2 = self.__screenY(line[3])
        print("drawLine:" + str((x1,y1,x2,y2)))

    def drawParticles(self,data):
        display = [(self.__screenX(d[0]),self.__screenY(d[1])) + d[2:] for d in data]
        print("drawParticles:" + str(display))

    def __screenX(self,x):
        return (x + self.margin)*self.scale

    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale

# A Map class containing walls
class Map:
    def __init__(self):
        self.walls = []

    def add_wall(self,wall):
        self.walls.append(wall)

    def clear(self):
        self.walls = []

    def draw(self):
        for wall in self.walls:
            canvas.drawLine(wall)

# Simple Particles set
class Particles:

    def __init__(self):
        self.numOfParticles = 100
        self.particles = [0] * self.numOfParticles

    def initialiseParticles(self):
        for i in range(self.numOfParticles):
            self.particles[i] = Particle(0, 0, 0, 1 / self.numOfParticles)

    def initialiseParticles(self, x, y):
        for i in range(self.numOfParticles):
            self.particles[i] = Particle(x, y, 0, 1 / self.numOfParticles)

    def printParticles(self):
        for particle in self.particles:
            print(str(particle.toTuple()))

    def update(self, distance, angle):
        if distance == 0 and angle == 0:
            return

        if angle == 0:

            for i in range(self.numOfParticles):
                # 0.51, 2.1, 11.13
                e = random.gauss(0, 1)
                f = random.gauss(0, 5)
                self.particles[i].updateParticle(self.particles[i].getWeight(), distance, [e, f, 0], angle)
        else:

            for i in range(self.numOfParticles):
                g = random.gauss(0, 0.08)
                self.particles[i].updateParticle(self.particles[i].getWeight(), distance, [0, 0, g], angle)

    def updateLikelihood(self, z):
        for i in range(self.numOfParticles):
            currentParticle = self.particles[i]

            x = currentParticle.getX()
            y = currentParticle.getY()
            theta = currentParticle.getAngle()
            weight = currentParticle.getWeight()

            likelihood = self.__calculateLikelihood(x, y, theta, z)

            currentParticle.updateWeight(weight * likelihood)

    def __calculateLikelihood(self, x, y, theta, z):
        # Find out which wall the sonar will hit
        m = WallsMethods.checkWalls(x, y, theta, WallsMethods.getWalls())

        # Calculate the likelihood
        numerator = - math.pow(z + centerToSensor - m, 2)
        denominator = 2 * math.pow(sigma, 2)
        likelihood = math.exp(numerator / denominator) + k

        return likelihood

    def normalise(self):
        weightSum = sum([particle.getWeight() for particle in self.particles])

        for i in range(self.numOfParticles):
            currentParticle = self.particles[i]
            weight = currentParticle.getWeight()
            currentParticle.updateWeight(weight / weightSum)

    def resample(self):
        particleWeights = [particle.getWeight() for particle in self.particles]

        cumulativeWeight = np.cumsum(particleWeights)

        tmpArray = []

        counter = 0

        for i in range(self.numOfParticles):

            particleSelector = random.random()

            for j in range(self.numOfParticles):
                if (cumulativeWeight[j] > particleSelector):
                    self.__copyParticle(tmpArray, self.particles[j])
                    counter += 1
                    break

        print("Counter: " + str(counter))

        self.particles = tmpArray

    def __copyParticle(self, array, particle):
        array.append(Particle(particle.getX(), particle.getY(), particle.getAngle(), 1 / self.numOfParticles))

    def getCurrentPosition(self):
        x = sum([particle.getX() * particle.getWeight() for particle in self.particles])
        y = sum([particle.getY() * particle.getWeight() for particle in self.particles])
        theta = sum([particle.getAngle() * particle.getWeight() for particle in self.particles])

        return (x, y, theta)

    def __particlesToTuple(self):
        return [particle.toTuple() for particle in self.particles]

    def draw(self):
        canvas.drawParticles(self.__particlesToTuple())

canvas = Canvas()    # global canvas we are going to draw on

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
mymap.add_wall(WALL_A)         # a
WALL_B = (0, 168, 84, 168)
mymap.add_wall(WALL_B)         # b
WALL_C = (84, 126, 84, 210)
mymap.add_wall(WALL_C)         # c
WALL_D = (84, 210, 168, 210)
mymap.add_wall(WALL_D)         # d
WALL_E = (168, 210, 168, 84)
mymap.add_wall(WALL_E)         # e
WALL_F = (168, 84, 210, 84)
mymap.add_wall(WALL_F)         # f
WALL_G = (210, 84, 210, 0)
mymap.add_wall(WALL_G)         # g
WALL_H = (210, 0, 0, 0)
mymap.add_wall(WALL_H)         # h
mymap.draw()

class WallsMethods:
    WALL_A = (0, 0, 0, 168)
    WALL_B = (0, 168, 84, 168)
    WALL_C = (84, 126, 84, 210)
    WALL_D = (84, 210, 168, 210)
    WALL_E = (168, 210, 168, 84)
    WALL_F = (168, 84, 210, 84)
    WALL_G = (210, 84, 210, 0)
    WALL_H = (210, 0, 0, 0)

    walls = [WALL_A, WALL_B, WALL_C, WALL_D, WALL_E, WALL_F, WALL_G, WALL_H]

    @classmethod
    def getWalls(self):
        return self.walls

    @classmethod
    def checkWalls(self, x, y, theta, walls):

        candidateWalls = []

        for wall in walls:
            AX = wall[0]
            AY = wall[1]
            BX = wall[2]
            BY = wall[3]

            cosTheta = math.cos(math.radians(theta))
            sinTheta = math.sin(math.radians(theta))

            # Compute the angle at which the sonar cone will hit the wall
            incidenceAngle = math.degrees(math.acos((math.cos(theta) * (AY - BY) + math.sin(theta) * (BX - AX)) / math.sqrt(math.pow(BX - AX, 2) + math.pow(BY - AY, 2))))
            
            if (theta % math.pi == 0):
                m = abs(AX - x)
                
            elif (theta % (math.pi / 2) == 0):
                m = abs(AY - y)
                
            else:

                m = ((BY - AY) * (AX - x) - (BX - AX) * (AY - y)) / ((BY - AY) * cosTheta - (BX - AX) * sinTheta)

                if (m > 0):

                    if (m < sonarMaxDistance):

                        hitX = x + m * cosTheta
                        hitY = y + m * sinTheta

                        if (AX == BX):
                            if (min(AY, BY) <= hitY <= max(AY, BY)):
                                candidateWalls.append(m)
                        elif (AY == BY):
                            if (min(AX, BX) <= hitX <= max(AX, BX)):
                                candidateWalls.append(m)

        if not candidateWalls:
            return sonarMaxDistance
        else:
            return min(candidateWalls)
