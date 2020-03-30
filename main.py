# import modules
import pygame as pg
import math
import time

WIDTH, HEIGHT = 600, 800

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pg.init()
background = pg.display.set_mode((WIDTH, HEIGHT))

g = 1

class Pendulum():
    def __init__(self, m1, m2, x1, y1, x2, y2, radius):
        # mass
        self.m1 = m1
        self.m2 = m2
        # mass 1 position
        self.x1 = x1
        self.y1 = y1
        # mass 2 position
        self.x2 = x2
        self.y2 = y2
        # stationary point (the top of the string)
        self.stationary_x = int(WIDTH / 2)
        self.stationary_y = 50.0
        # radius of the masses
        self.radius = radius
        # angluar velocities
        self.a1_v = 0.0
        self.a2_v = 0.0
        # angular accelerations
        self.a1_a = 0.0
        self.a1_a = 0.0

    def draw(self):
        # strings
        pg.draw.lines(background, BLACK, False, [(self.stationary_x, self.stationary_y), (self.x1, self.y1)], 2)
        pg.draw.lines(background, BLACK, False, [(self.x1, self.y1), (self.x2, self.y2)], 2)
        # masses
        pg.draw.circle(background, BLACK, (int(self.x1), int(self.y1)), int(self.radius) + 2)
        pg.draw.circle(background, RED, (int(self.x1), int(self.y1)), int(self.radius))
        pg.draw.circle(background, BLACK, (int(self.x2), int(self.y2)), int(self.radius) + 2)
        pg.draw.circle(background, RED, (int(self.x2), int(self.y2)), int(self.radius))
    
    def calc_length(self):
        self.length1 = math.sqrt(math.pow(self.x1 - self.stationary_x, 2) + math.pow(self.y1 - self.stationary_y, 2))
        self.length2 = math.sqrt(math.pow(self.x2 - self.x1, 2) + math.pow(self.y2 - self.y1, 2)) 
        return self.length1, self.length2

    def calc_angle(self):
        self.a1 = math.asin((self.x1 - self.stationary_x) / self.length1)
        self.a2 = math.asin((self.x2 - self.x1) / self.length2)
        return self.a1, self.a2

    def calc_new_pos(self):
        # mass 1
        self.x1 = self.length1 * math.sin(self.a1)
        self.y1 = self.length1 * math.cos(self.a1)

        # mass 2
        self.x2 = self.x1 + (self.length2 * math.sin(self.a2))
        self.y2 = self.y1 + (self.length2 * math.cos(self.a2))

    def calc_angular_acceleration(self):
        # components for calculating the first angular acceleration
        com1 = -g * (2 * self.m1 + self.m2) * math.sin(self.a1)
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
        self.a2_a = (com1 * (com2 + com3)) / den

pendulum = Pendulum(1.0, 1.0, (WIDTH / 2) + 200.0, 200.0, (WIDTH / 2) + 100, 300.0, 10.0)
pendulum.calc_length()
pendulum.calc_angle()

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    background.fill(WHITE)
    pendulum.draw()
    pg.display.update()

    pendulum.calc_angular_acceleration()
    pendulum.calc_new_pos()

    pendulum.a1_v += pendulum.a1_a
    pendulum.a2_v += pendulum.a2_a
    pendulum.a1 = pendulum.a1_v
    pendulum.a2 = pendulum.a2_v
    print(pendulum.a1, pendulum.a2)
