import math


class Particle:

    def __init__(self, x , y, theta, weight):
        self.x = x
        self.y = y
        self.theta = theta
        self.weight = weight

    def updateParticle(self, weight, distance, noise, angle):
        if angle == 0:
            e = noise[0]
            f = noise[1]

            self.x += (distance + e) * math.cos(math.radians(self.theta))
            self.y += (distance + e) * math.sin(math.radians(self.theta))
            self.theta += f
            self.weight = weight
        else:
            g = noise[2]

            self.theta += angle + g
            self.weight = weight

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWeight(self):
        return self.weight

    def getAngle(self):
        return self.theta

    def updateWeight(self, weight):
        self.weight = weight

    def toTuple(self):
        return (self.x, self.y, self.theta, self.weight)