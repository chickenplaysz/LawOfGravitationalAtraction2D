from time import perf_counter
from turtledemo.nim import SCREENWIDTH, SCREENHEIGHT

import pygame
import math
import time
import random as rnd

G = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

TICK_RATE = 1000

# initialize pygame
pygame.init()
screen_size = (700, 500)

# create a window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("pygame Test")

# clock is used to set a max fps
clock = pygame.time.Clock()
clock.tick(TICK_RATE)
dt = clock.tick(TICK_RATE) / 1000

planetStack = []


class Vector(list):

    def vectorMath2D(self, op, v2: list):
        outV = Vector([0, 0])
        if type(v2) is Vector:
            pass
        else:
            v2 = [v2, v2]

        for i, v in enumerate(v2):
            outV[i] = eval(f"{self[i]} {op} {v}")

        return outV

    def getMagnitude(self):
        return math.sqrt(self[0] **2 + self[1] **2)

    def normalized(self):
        return self.vectorMath2D("/", self.getMagnitude())

class Planet:
    def __init__(self, mass, color: tuple, size: int, position: list, velocity: list,  movable=True):
        self.movable = movable
        self.mass = mass
        self.velocity = Vector(velocity)
        self.position = Vector(position)
        self.size = size
        self.color = color

    def move(self):

        self.position = self.position.vectorMath2D("+", self.velocity.vectorMath2D("*", dt))

def drawPlanets(i):
    center = Vector([SCREENWIDTH / 2, SCREENHEIGHT / 2])
    pygame.draw.circle(screen, i.color, i.position.vectorMath2D("+", center), i.size)


def calculatePhysics(planet):
    for otherPlanet in planetStack:
        if otherPlanet != planet:
            sqrDst = otherPlanet.position.vectorMath2D("-", planet.position).getMagnitude()**2
            forceDir = otherPlanet.position.vectorMath2D("-", planet.position).normalized()
            force = forceDir.vectorMath2D("*", G).vectorMath2D("*", planet.mass).vectorMath2D("*", otherPlanet.mass).vectorMath2D("/", sqrDst)
            acc = force.vectorMath2D("/", planet.mass)
            planet.velocity = planet.velocity.vectorMath2D("+", acc)
            print(f"distance: {math.sqrt(sqrDst)}\nforce: {force}")


planetStack.append(Planet(10**5, (255,255,255), 10, [0, 0], [0, 0  ], False))
planetStack.append(Planet(10**3, (255,255,255), 10, [250, 0], [0, 300], True))
planetStack.append(Planet(10**2, (255,255,255), 10, [-150, 100], [200, 180], True))

# a = list(planetStack[:])
# for step in range(1000):
#     for i in a:
#         calculatePhysics(i)
#         i.move()
#         center = Vector([SCREENWIDTH / 2, SCREENHEIGHT / 2])
#         pygame.draw.circle(screen, i.color, i.position.vectorMath2D("+", center), 1)

running = True
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # clear the screen
    screen.fill(BLACK)
    #track dt
    font = pygame.font.SysFont("Comic Sans MS", 15).render(f"{dt}", True, (255, 255, 255))
    screen.blit(font, (0, 0))




    for planet in planetStack:
        if planet.movable:
            calculatePhysics(planet)
            planet.move()
            planet.color = (max(0,min(planet.velocity[0],255)), max(0, min(planet.velocity[1], 255)), max(0, min(planet.velocity.getMagnitude()-200, 255)))
        drawPlanets(planet)


    # flip() updates the screen to make our changes visible
    pygame.display.flip()
    dt = clock.tick(TICK_RATE) / 1000

pygame.quit()