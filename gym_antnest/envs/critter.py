from .vec2d import random_angle, polar_from_pt, vec_dir, clamp


class Critter:
    """A mobile object that can move around the world.
    """
    def __init__(self, pt, world):
        self.pos = pt
        self.angle = 0 # Angle in radians that we're facing.
        self.dir = None # Normalized vector in the direction we're facing. Will be set below.
        self.world = world
        self.set_angle(random_angle())
    
    def turn(self, a):
        """Turn left or right by the given angle."""
        self.set_angle(self.angle + a)

    def set_angle(self, a):
        self.angle = a
        facing = polar_from_pt(self.pos, self.angle, 1)
        self.dir = vec_dir(self.pos, facing)
    
    def forward(self, distance=1):
        """Move forward in the direction we're facing."""
        delta = self.dir * distance
        self.pos = clamp(self.pos + delta, self.world.width, self.world.height)
