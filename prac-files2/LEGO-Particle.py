import random

from Robot import Robot

from Particle import Particle

import time

NUM_OF_PARTICLES = 100
particle = Particle(100, 700, 0, 1 / NUM_OF_PARTICLES)
particles = [0] * NUM_OF_PARTICLES

scale = (100, 500, 0)
lineScale = (100, 500, 300, 500)

robot = Robot("B", "C")
robot.setMotorLimits(30, 720)

def drawParticles(particles):
    print("drawParticles:" + str(particles))

def drawLines(line):
    print("drawLine:" + str(line))

def initialiseParticles():
    for i in range(NUM_OF_PARTICLES):
        particles[i] = Particle(100, 700, 0, 1 / NUM_OF_PARTICLES)

initialiseParticles()

drawParticles([particle.toTuple() for particle in particles])
time.sleep(1)


for i in range(4):

    for j in range(4):
        oldPosition = (particle.getX(), particle.getY())

        robot.moveForward(10)
        time.sleep(1)

        # Update particles
        for i in range(NUM_OF_PARTICLES):

            # Sample random number
            e = random.gauss(0, 1)
            f = random.gauss(0, 0.05)

            particles[i].updateParticle(particles[i].weight, 150, [e, f, 0], 0)

        particle.updateParticle(particle.weight, 150, [0, 0, 0], 0)

        # Draw the particles
        drawParticles([particle.toTuple() for particle in particles])

        newPosition = (particle.getX(), particle.getY())
        drawLines((oldPosition[0], oldPosition[1], newPosition[0], newPosition[1]))

        time.sleep(1)


    robot.turnLeft(90)
    for i in range(NUM_OF_PARTICLES):
        g = random.gauss(0, 2)
        particles[i].updateParticle(particles[i].weight, 0, [0, 0, g], -90)

    particle.updateParticle(particle.weight, 0, [0, 0, 0], -90)

    time.sleep(1)