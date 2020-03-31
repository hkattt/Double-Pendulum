# import modules
import pygame as pg
import math
import time

WIDTH, HEIGHT = 500, 500

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)

pg.init()
background = pg.display.set_mode((WIDTH, HEIGHT))

g = 0.02

class Pendulum():
    def __init__(self, m1, length1, a1, radius):
        # mass
        self.m1 = m1
        # stationary point (the top of the string)
        self.stationary_x = int(WIDTH / 2)
        self.stationary_y = 50.0
        # string length
        self.length1 = length1
        # angle
        self.a1 = a1
        # radius of the masses
        self.radius = radius
        # angluar velocity
        self.a1_v = 0.0
        # angular acceleration
        self.a1_a = 0.0

    def draw(self):
        # string
        pg.draw.lines(background, BLACK, False, [(self.stationary_x, self.stationary_y), (self.x1, self.y1)], 2)
        # mass
        pg.draw.circle(background, BLACK, (int(self.x1), int(self.y1)), int(self.radius) + 2)
        pg.draw.circle(background, GREY, (int(self.x1), int(self.y1)), int(self.radius))
    
    def calc_pos(self):
        # mass 1
        self.x1 = self.stationary_x + self.length1 * math.sin(self.a1)
        self.y1 = self.stationary_y + self.length1 * math.cos(self.a1)

    def move(self):
        self.a1 += self.a1_v
        self.a1_v += self.a1_a
        self.a1_v *= 0.98

    def calc_angular_acceleration(self):
        self.a1_a = -g * math.sin(self.a1)
        # components for calculating the first angular acceleration
        '''com1 = -g * (2 * self.m1 + self.m2) * math.sin(self.a1)
        com2 = self.m2 * g * math.sin(self.a1 - (2 * self.a2))
        com3 = -2 * math.sin(self.a1 - self.a2) * self.m2 * (self.a2_v * self.length2 + math.pow(self.a1_v, 2) * self.length1 * math.cos(self.a1 - self.a2))
        den = self.length1 * (2 * self.m1 + self.m2 - self.m2 * math.cos((2 * self.a1) - (2 * self.a2)))
        # calculation
        self.a1_a = (com1 + com2 + com3) / den

        # componenets for calculating the second angular acceleration
        com1 = 2 * math.sin(self.a1 - self.a2)
        com2 = math.pow(self.a1_v, 2) * self.length1 * (self.m1 + self.m2) * g * (self.m1 + self.m2) * math.cos(self.a1)
        com3 = math.pow(self.a2_v, 2) * self.length2 * self.m2 * math.cos(self.a1 - self.a2)
        den = self.length2 * ((2 * self.m1) + self.m2 - (self.m2 * math.cos((2 * self.a1) - (2 * self.a2))))
        # calculation
        self.a2_a = (com1 * (com2 + com3)) / den'''

pendulum = Pendulum(1.0, 150.0, math.pi / 2, 20)
pendulum.calc_pos()

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    background.fill(WHITE)
    pendulum.draw()
    pg.display.update()

    pendulum.calc_angular_acceleration()
    pendulum.move()
    pendulum.calc_pos()
    time.sleep(0.01)