import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from gym.envs.classic_control import rendering
import os

class AntNestEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.reset()
        self.t = 0
        self.viewer = None
        self.world_x = 40
        self.world_y = 40
        #self.ant = make_ant()
        self.ant_seq = 0

    def step(self, action):
        reward = 1
        done = False
        observation = None
        info = None
        self.t += 1
        self.x += 1
        self.state = np.array((self.x, 0))

        #self.ant_seq = (self.ant_seq + 1) % 4
        return [self.state, reward, done, info]

    def reset(self):
        self.x = 0
        self.state = np.zeros(2)

    def render(self, mode='human', close=False):
        # https://github.com/openai/gym/blob/master/gym/envs/classic_control/rendering.py
        print("render %s" % self.x)
        width = 600
        height = width
        scale_x = width / self.world_x
        scale_y = height / self.world_y

        if self.viewer is None:
            self.viewer = rendering.Viewer(width, height)

        x = self.x
        angle = self.t / 100
        #x=100

        render_ant(self.viewer, self.ant_seq, angle, (x, 100))
        square = rendering.FilledPolygon([(10+x,10), (10+x,20), (20+x,20), (20+x,10)])
        square.set_color(0, 0, 255)
        self.viewer.add_onetime(square)

        return self.viewer.render(return_rgb_array=mode=='rgb_array')

    def close(self):
        pass

    def seed(self):
        pass

def render_ant(v, seq, angle, pt):
    head_radius = 7
    x, y = pt
    body_pos = rendering.Transform(translation=(x, y), rotation=angle)
    ant = make_ant()
    ant.select_sprite(seq)
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

import pyglet

class SpriteSheet(rendering.Image):
    # Source to base class:
    #   https://github.com/openai/gym/blob/master/gym/envs/classic_control/rendering.py
    # About sprite sheets:
    #   https://pyglet.readthedocs.io/en/stable/programming_guide/image.html
    def __init__(self, fname, width, height, rows, cols):
        """
        rows, cols: rows and columns of sub-images in the spritesheet.
        width, height: target size for image.
        """
        rendering.Image.__init__(self, fname, width, height)
        self.sprite_sheet = self.img # set during Image.__init__
        self.sub_images = pyglet.image.ImageGrid(self.sprite_sheet, rows, cols)
        self.last_sprite = 0 # index of last sprite
        self.select_sprite(0)
    
    def select_sprite(self, n):
        """
        Select one of the sprites from the sprite sheet.
        n: A number between 0 and (rows * cols)
        """
        print('subimages',len(self.sub_images))
        self.img = self.sub_images[n]
        self.last_sprite = n
    
    def next_sprite(self):
        self.last_sprite = (self.last_sprite + 1) % len(self.sub_images)

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


def circle(pt, r, color):
    pos = rendering.Transform(translation=pt)
    v.draw_circle(r, 20, color=color).add_attr(pos)

