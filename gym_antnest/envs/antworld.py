from .critter import Critter

import numpy as np
import random
import math

WORLD_WIDTH = 100
WORLD_HEIGHT = 100
FOODS_PER_CLUSTER = 15
FOOD_CLUSTER_RADIUS = 18
NUM_ANTS = 5

SCENT_STRENGTH = 0.3 # How strong scent is when an ant drops a trail
SCENT_DECAY = 1 / 1500 # Number of steps it takes for a scent to fully decay.
SCENT_MAX = 1 # Strongest a scent can be within a cell.

CELL_FOOD = 'F'

class AntWorld:
    def __init__(self):
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.foods = [] # [(x, y)] locations of foods.
        self._contents = [None] * self.height * self.width
        self.make_food_cluster()
        self.ants = [Critter(self._random_pt(), self) for _ in range(NUM_ANTS)]
        self._scent_trails = np.zeros((self.height, self.width))

    def update(self):
        self._update_scent_trail()

    def make_food_cluster(self):
        center = self._random_pt()
        for _ in range(FOODS_PER_CLUSTER):
            pt = self._random_offset(center, FOOD_CLUSTER_RADIUS)
            if not self._in_bounds(pt) or self._cell(pt) != None:
                continue
            self.place_food(pt)

    def place_food(self, pt):
        pt = np.array(pt)
        self._put(pt, CELL_FOOD)
        self.foods.append(pt)
    
    def scent_cells(self):
        """Returns a list of cells that contain scents, like [((x,y), magnitude)]"""
        non_zero_cells = np.argwhere(self._scent_trails)
        s = self._scent_trails
        return [((pt[1], pt[0]), s[pt[0]][pt[1]]) for pt in np.argwhere(s)]
    
    def _update_scent_trail(self):
        for ant in self.ants:
            self._increase_scent(ant.pos)
        # Decay the scents linearly.  If any go below zero, make them zero.
        self._scent_trails = np.maximum(0, self._scent_trails - SCENT_DECAY)

    def _increase_scent(self, pt):
        # Increase scent marker where the ant currently is.
        row, col = int(pt[1]), int(pt[0])
        row = max(0, row)
        col = max(0, col)
        row = min(row, self.height - 1)
        col = min(col, self.width - 1)
        self._scent_trails[row][col] = min(self._scent_trails[row][col] + SCENT_STRENGTH, SCENT_MAX)

    def _put(self, pt, object_type):
        """Put an object into a spot in the world."""
        self._contents[int(self._index(pt))] = object_type

    def _cell(self, pt):
        """Returns the contents of the given world coordinates."""
        return self._contents[int(self._index(pt))]
    
    def _index(self, pt):
        x, y = pt
        return y * self.width + x

    def _random_pt(self):
        return np.array((random.randint(0, self.width), random.randint(0, self.height)))

    def _random_offset(self, pt, radius):
        cx, cy = pt
        angle = random.uniform(0, np.pi * 2)
        r = random.uniform(0, radius)
        x = round(r * np.cos(angle) + cx)
        y = round(r * np.sin(angle) + cy)
        return x, y

    def _in_bounds(self, pt):
        """Returns True if the given point is within the world."""
        x, y = pt
        return x >=0 and x < self.width and y >= 0 and y < self.height
