from .critter import Critter

import numpy as np
import random
import math

WORLD_WIDTH = 100
WORLD_HEIGHT = 100
FOODS_PER_CLUSTER = 15
FOOD_CLUSTER_RADIUS = 18

CELL_EMPTY = ' '
CELL_FOOD = 'F'

class AntWorld:
    def __init__(self):
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.objects = [] # [(object_type, (x, y))] where object_type is CELL_FOOD, etc.
        self._contents = [CELL_EMPTY] * self.height * self.width
        self.make_food_cluster()
        self.ant = Critter(self._random_pt(), self)

    def make_food_cluster(self):
        center = self._random_pt()
        for _ in range(FOODS_PER_CLUSTER):
            pt = self._random_offset(center, FOOD_CLUSTER_RADIUS)
            if not self._in_bounds(pt) or self._cell(pt) != CELL_EMPTY:
                continue
            self._put(pt, CELL_FOOD)

    def _put(self, pt, object_type):
        """Put an object into a spot in the world."""
        self._contents[int(self._index(pt))] = object_type
        self.objects.append((object_type, pt))

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
