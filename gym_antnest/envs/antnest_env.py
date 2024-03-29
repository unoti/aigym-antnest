from .antworld import AntWorld, CELL_FOOD
from .spritesheet import SpriteSheet
from .vec2d import lerp_3d

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from gym.envs.classic_control import rendering
import os

COLOR_FOOD = np.array((0.376, 0.871, 0.165))
COLOR_SCENT = np.array((0.667, 0.286, 0.902))
COLOR_WHITE = np.array((1,1,1))

ANT_TURN_RATE = 0.2 # Ant turn speed in radians per step

class AntNestEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.reset()
        self.t = 0
        self.viewer = None
        self.ant_seq = 0
        self.world = AntWorld()
        self.pixels_width = 600
        self.pixels_height = self.pixels_width
        self.scale = np.array([self.pixels_width / self.world.width, self.pixels_height / self.world.height])
        self.action_methods = [
            self._action_left,
            self._action_right,
            self._action_forward,
            self._action_pause
        ]
        self.active_ant = 0 # We will cycle through the ants giving each one a turn.

    def step(self, action):
        assert action < len(self.action_methods)
        # Invoke the chosen action
        self.action_methods[action]()

        self.world.update()

        reward = 1
        done = False
        observation = None
        info = None
        self.t += 1
        self.x += 1
        self.state = np.array((self.x, 0))
        self.active_ant = (self.active_ant + 1) % len(self.world.ants)
        return [self.state, reward, done, info]

    def reset(self):
        self.x = 0
        self.state = np.zeros(2)

    def render(self, mode='human', close=False):
        # https://github.com/openai/gym/blob/master/gym/envs/classic_control/rendering.py
        if self.viewer is None:
            self.viewer = rendering.Viewer(self.pixels_width, self.pixels_height)

        # Scent trails
        for pt, strength in self.world.scent_cells():
            color = lerp_3d(COLOR_WHITE, COLOR_SCENT, strength)
            circle(self.viewer, pt * self.scale, 4, color)

        # Foods
        for pt in self.world.foods:
            circle(self.viewer, pt * self.scale, 7, COLOR_FOOD)

        # Ants
        for ant in self.world.ants:
            render_ant(self.viewer, ant.angle, ant.pos * self.scale)

        return self.viewer.render(return_rgb_array=mode=='rgb_array')

    def close(self):
        pass

    def seed(self):
        pass

    def _action_left(self):
        self.world.ants[self.active_ant].turn(ANT_TURN_RATE)
    
    def _action_right(self):
        self.world.ants[self.active_ant].turn(-ANT_TURN_RATE)
    
    def _action_forward(self):
        self.world.ants[self.active_ant].forward()
    
    def _action_pause(self):
        pass

def render_ant(v, angle, pt):
    head_radius = 7
    x, y = pt
    body_pos = rendering.Transform(translation=(x, y), rotation=angle)
    ant = make_ant()
    ant.select_sprite(0) # Later' we'll cycle multiple sprites to animate the ant legs as they walk.
    ant.add_attr(body_pos)
    v.add_onetime(ant)

    # body
    #v.draw_circle(head_radius, 20, color=ant_color).add_attr(body_pos)
    #circle(v, pt, head_radius * 0.7, color=ant_color)

    # thorax (middle)
    #head_pt = (x + 10, y) 
    #circle(v, head_pt, head_radius, color=ant_color)

    # abdomen (back)
    #back_pt = (x - 10, y) 
    #circle(v, back_pt, head_radius * 1.1, color=ant_color)

def make_ant():
    # Ant using an animated spritesheet
    path = os.path.dirname(os.path.abspath(__file__))
    #filename = os.path.join(path, 'ant.png')
    filename = os.path.join(path, 'antspritesheet.png')
    ant = SpriteSheet(filename, 40, 40, rows=2, cols=2)
    ant.set_color(1,1,1)
    return ant

def make_ant2():
    # Ant using a single bitmap
    path = os.path.dirname(os.path.abspath(__file__))
    #filename = os.path.join(path, 'ant.png')
    filename = os.path.join(path, 'antspritesheet.png')
    ant = rendering.Image(filename, 30, 30)
    ant.set_color(1,1,1)
    return ant

def make_ant1():
    # Ant using polygons
    ant_color = (0.5, 0.4, 0.9)
    body_radius = 7
    
    # thorax (middle)
    body = rendering.make_circle(radius=body_radius, res=20, filled=True)
    
    # head
    head_pos = rendering.Transform(translation=(body_radius,0))
    head = rendering.make_circle(radius=body_radius * 0.9, res=20, filled=True)
    head.add_attr(head_pos)

    # abdomen (back)
    parts = [body]
    ant = rendering.Compound(parts)
    ant.set_color(*ant_color)
    return ant

def circle(v, pt, r, color):
    pos = rendering.Transform(translation=pt)
    v.draw_circle(r, 15, color=color).add_attr(pos)

