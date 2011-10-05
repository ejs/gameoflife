#!/usr/bin/env python

import time
from itertools import count
from turtle import *


class TurtleVisualiser(object):

    margin = 75

    def __init__(self, world):
        self.setup()
        self.world = world
        self.scale = min((getscreen().window_width() - self.margin) / float(world.width), (getscreen().window_height() - self.margin) / float(world.height))
        self.x_shift, self.y_shift = (world.width - 1) / 2. * -self.scale, (world.height / 2. - 1) * self.scale

    def setup(self):
        """Initialise turtle."""
        tracer(0, 0)
        hideturtle()
        getscreen().bgcolor('black')
        color('green')
        width(1)

    def plot(self, dot, x, y):
        """Plot cell at x, y coord."""
        penup()
        goto(x * self.scale + self.x_shift, -y * self.scale + self.y_shift)
        pendown()
        fill(dot == '*')
        circle(self.scale / 2)

    def heading(self, text):
        """Print heading on canvas."""
        penup()
        goto(-getscreen().window_width() / 2 + 10, getscreen().window_height() / 2 - 25)
        pendown()
        write(text, font=("Arial", 16, "normal"))

    def visualise(self):
        """Start visualisation."""
        step = count()
        while len(self.world):
            clear()
            for lineno, line in enumerate(self.world.display()):
                for colno, col in enumerate(line):
                    self.plot(col, colno, lineno)
            self.heading('Step {0}'.format(next(step)))
            update()
            self.world.tick()
            time.sleep(0.1)
        raw_input('Press any key ...')

