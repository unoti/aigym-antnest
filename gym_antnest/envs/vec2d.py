import numpy as np

def vec_dir(v0, v1):
    """Returns a normalized vector pointing from v0 towards v1"""
    delta = v1 - v0
    norm = np.linalg.norm(delta)
    return delta / norm

def random_dir():
    """Returns a random direction in the form of a normalized vector."""
    x, y = np.random.uniform(-1,1), np.random.uniform(-1, 1)
    pt = np.array((x,y))
    return pt / np.linalg.norm(pt)

def random_angle():
    return np.random.uniform(-np.pi, np.pi)

def angle_from(p0, p1):
    """Returns the angle from p0 to p1"""
    delta = p1 - p0
    x, y = delta
    return np.arctan2(y, x)

def polar_from_pt(pt, a, r):
    """Given a starting point, returns another point at
    a given distance and angle from the starting point.
    pt: a starting point.
    a: an angle
    r: a radius 
    """
    x0,y0 = pt
    x1 = r * np.cos(a) + x0
    y1 = r * np.sin(a) + y0
    return np.array((x1, y1))

def to_deg(a):
    return a / np.pi * 180

def relative_angle(p0, dir0, p1):
    """
    p0: A vector with the position of an object.
    dir0: A normalized vector indicating the direction the object at p0 is facing.
    p1: The position of a target object.
    Returns the relative angle left/right that point p1 lies in the field of view of p0.
    Returns a positive number if the target is to the left, and negative if it is to the right.
    """
    x0, y0 = dir0
    angle0 = np.arctan2(y0, x0)
    angle1 = angle_from(p0, p1)
    delta_angle = angle1 - angle0
    #print('relang p0=%s dir0=%s p1=%s' % (p0, dir0, p1))
    #print('angle0=%s angle1=%s delta=%s' % (to_deg(angle0), to_deg(angle1), to_deg(delta_angle)))
    return delta_angle

def test_relative_angle():
    p0 = np.array((1,1))
    p0_facing = np.array((20, 100)) # Looking a little to the right of the top left corner.
    p0_dir = vec_dir(p0, p0_facing) # Mostly up and a little right. [0.18847945 0.98207713]
    targets = [(100,100), (70,2), (50,12), (16, 80)]
    for t in targets:
        print('From %s to %s' % (p0, t))
        a = relative_angle(p0, p0_dir, t)
        print('t=%s a=%s' % (t, to_deg(a)))

def test_relative_angle2():
    def offset(pt, a, r): # Returns a point at the given angle and distance
        x0,y0 = pt
        x1 = r * np.cos(a) + x0
        y1 = r * np.sin(a) + y0
        return np.array((x1, y1))
    p0 = np.array([20,20])
    a = 0
    r = 5
    # For several points around a circle, select a target point and face that point.
    # Then place a target a little to the left of that.
    for i in range(8):
        p0_dir = vec_dir(p0, offset(p0, a, r))
        target_a = a + np.pi/12 # Target is a little to the left
        p1 = offset(p0, target_a, r)
        ra = relative_angle(p0, p0_dir, p1)
        assert (ra  - np.pi/12) < 0.0001, 'expected angle to be equal'
        a += np.pi / 8
