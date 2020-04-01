# Double Pendulum Simulation: Inspired by The Coding Train's Double Pendulum Code Challenge

# import modules
import pygame as pg
import math
import time

# display window dimensions
WIDTH, HEIGHT = 500, 500

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)
LIGHT_GREEN = (144, 238, 144)

# gravity
g = 1.0

pg.init()
background = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Double Pendulum Simulation")

class Pendulum():
    def __init__(self, m1, m2, length1, length2, a1, a2):
        # masses
        self.m1 = m1
        self.m2 = m2
        # stationary point (the top of the string)
        self.stationary_x = int(WIDTH / 2)
        self.stationary_y = 50.0
        # string lengths
        self.length1 = length1
        self.length2 = length2
        # angles
        self.a1 = a1
        self.a2 = a2
        # radius of the masses
        self.radius = 20
        # angluar velocities
        self.a1_v = 0.0
        self.a2_v = 0.0
        # angular accelerations
        self.a1_a = 0.0
        self.a2_a = 0.0
        # allows the user to interact with the masses
        self.m1_selected = False
        self.m2_selected = False

    def draw(self):
        """ Draws the double pendulum onto the display window """
        # strings
        pg.draw.circle(background, BLACK, (int(self.stationary_x), int(self.stationary_y)), 4)
        pg.draw.lines(background, BLACK, False, [(int(self.stationary_x), int(self.stationary_y)), (int(self.x1), int(self.y1))], 2)
        pg.draw.lines(background, BLACK, False, [(int(self.x1), int(self.y1)), (int(self.x2), int(self.y2))], 2)
        
        # mass 1
        pg.draw.circle(background, BLACK, (int(self.x1), int(self.y1)), int(self.m1) + 2)
        pg.draw.circle(background, GREY, (int(self.x1), int(self.y1)), int(self.m1))
        # if the user selected mass 1
        if self.m1_selected:
           pg.draw.circle(background, LIGHT_GREEN, (int(self.x1), int(self.y1)), int(self.m1)) 

        # mass 2         
        pg.draw.circle(background, BLACK, (int(self.x2), int(self.y2)), int(self.m2) + 2)
        pg.draw.circle(background, GREY, (int(self.x2), int(self.y2)), int(self.m2))
        # if the user selected mass 2
        if self.m2_selected:
            pg.draw.circle(background, LIGHT_GREEN, (int(self.x2), int(self.y2)), int(self.m2))

    def calc_pos(self):
        """ Calculates the x, y position of both masses using trigonometry """
        # mass 1
        self.x1 = self.stationary_x + self.length1 * math.sin(self.a1)
        self.y1 = self.stationary_y + self.length1 * math.cos(self.a1)

        # mass 2
        self.x2 = self.x1 + self.length2 * math.sin(self.a2)
        self.y2 = self.y1 + self.length2 * math.cos(self.a2)

    def calc_length(self):
        """ Calculates the length of the string given new x, y coordinates """
        if self.m1_selected:
            self.length1 = math.sqrt(pow(self.x1 - self.stationary_x, 2) + pow(self.y1 - self.stationary_y, 2))
        elif self.m2_selected:
            self.length2 = math.sqrt(pow(self.x2 - self.x1, 2) + pow(self.y2 - self.y1, 2))
    
    def calc_angle(self):
        """ Calculates angle 2 given the new length and x coordinate """
        if self.m1_selected:
            self.a1 = math.asin((self.x1 - self.stationary_x) / self.length1)
        elif self.m2_selected:
            self.a2 = math.asin((self.x2 - self.x1) / self.length2)

    def apply_acc(self):
        """ Applies the calculated angular acceleration the the angular
            velocity, which determines the new angle """
        # adjust angular velocities
        self.a1_v += self.a1_a
        self.a2_v += self.a2_a

        # adjust angle
        self.a1 += self.a1_v
        self.a2 += self.a2_v

        # damping
        #self.a1_v *= 0.99
        #self.a1_v *= 0.99

    def calc_angular_acceleration(self):
        """ Calculates the angular accelerations using the equations of motion 
        (view: https://www.myphysicslab.com/pendulum/double-pendulum-en.html) """
        # components for calculating the first angular acceleration
        com1 = -g * (2 * self.m1 + self.m2) * math.sin(self.a1)
        com2 = -self.m2 * g * math.sin(self.a1 - (2 * self.a2))
        com3 = -2 * math.sin(self.a1 - self.a2) * self.m2
        com4 = (math.pow(self.a2_v, 2) * self.length2 + math.pow(self.a1_v, 2) * self.length1 * math.cos(self.a1 - self.a2))
        den = self.length1 * (2 * self.m1 + self.m2 - self.m2 * math.cos((2 * self.a1) - (2 * self.a2)))
        # combining all the components to calculate the first angular acceleration
        self.a1_a = (com1 + com2 + (com3 * com4))  / den

        # componenets for calculating the second angular acceleration
        com1 = 2 * math.sin(self.a1 - self.a2)
        com2 = math.pow(self.a1_v, 2) * self.length1 * (self.m1 + self.m2)
        com3 = g * (self.m1 + self.m2) * math.cos(self.a1)
        com4 = math.pow(self.a2_v, 2) * self.length2 * self.m2 * math.cos(self.a1 - self.a2)
        den = self.length2 * ((2 * self.m1) + self.m2 - (self.m2 * math.cos((2 * self.a1) - (2 * self.a2))))
        # combining all the componenets to calculate the second angular acceleration
        self.a2_a = (com1 * (com2 + com3 + com4)) / den

# creates a pendulum object
pendulum = Pendulum(10.0, 10.0, 150.0, 150.0, 0, 0)
# calculates its initial position
pendulum.calc_pos()

running = True
while running:
    # mouse x, y coordinates
    x, y = pg.mouse.get_pos() 
    # checks if the user wants to quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            # moves mass 1
            if pendulum.m1_selected:
                pendulum.x1, pendulum.y1 = x, y
                pendulum.calc_length()
                pendulum.calc_angle()
                pendulum.m1_selected = False
            # moves mass 2
            elif pendulum.m2_selected:
                pendulum.x2, pendulum.y2 = x, y
                pendulum.calc_length()
                pendulum.calc_angle()
                pendulum.m2_selected = False
            # selects a mass
            else:
                # selects mass 1
                if x < pendulum.x1 + pendulum.m1 and x > pendulum.x1 - pendulum.m1:
                    if y > pendulum.y1 - pendulum.m1 and y < pendulum.y1 + pendulum.m1:
                        pendulum.m1_selected = True
                # selects mass 2
                if x < pendulum.x2 + pendulum.m2 and x > pendulum.x2 - pendulum.m2:
                    if y > pendulum.y2 - pendulum.m2 and y < pendulum.y2 + pendulum.m2:
                        pendulum.m2_selected = True

    # draws the pendulum
    background.fill(WHITE)
    pendulum.draw()
    pg.display.update()

    pendulum.calc_angular_acceleration()
    pendulum.apply_acc()
    pendulum.calc_pos()
    # stops the programs for a small duration of time
    time.sleep(0.01)