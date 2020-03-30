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
        self.stationary_y = 50
        # radius of the masses
        self.radius = radius
        # angluar velocities
        self.a1_v = 0
        self.a2_v = 0
        # angular accelerations
        self.a1_a = 0
        self.a1_a = 0

    def draw(self):
        # strings
        pg.draw.lines(background, BLACK, False, [(self.stationary_x, self.stationary_y), (self.x1, self.y1)], 2)
        pg.draw.lines(background, BLACK, False, [(self.x1, self.y1), (self.x2, self.y2)], 2)
        # masses
        pg.draw.circle(background, BLACK, (self.x1, self.y1), self.radius + 2)
        pg.draw.circle(background, RED, (self.x1, self.y1), self.radius)
        pg.draw.circle(background, BLACK, (self.x2, self.y2), self.radius + 2)
        pg.draw.circle(background, RED, (self.x2, self.y2), self.radius)
    
    def calc_length(self):
        self.length = math.sqrt(math.pow(self.x1 - self.stationary_x, 2) + math.pow(self.y1 - self.stationary_y, 2))
        return self.length

    def calc_angle(self):
        self.angle = math.asin((self.x1 - self.stationary_x) / self.length)
        self.angle = math.degrees(self.angle)
        return self.angle


pendulum = Pendulum(1, 1, int(WIDTH / 2) +200, 200, int(WIDTH / 2) + 100, 300, 10)
background.fill(WHITE)
pendulum.draw()
pg.display.update()
time.sleep(5)
