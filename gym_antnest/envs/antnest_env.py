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

    def step(self, action):
        reward = 1
        done = False
        observation = None
        info = None
        self.t += 1
        self.x += 1
        self.state = np.array((self.x, 0))
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

        #x = self.x
        x=100
        render_ant(self.viewer, 0, (x, 100))
        square = rendering.FilledPolygon([(10+x,10), (10+x,20), (20+x,20), (20+x,10)])
        square.set_color(0, 0, 255)
        self.viewer.add_onetime(square)

        return self.viewer.render(return_rgb_array=mode=='rgb_array')

    def close(self):
        pass

    def seed(self):
        pass

def render_ant(v, angle, pt):
    head_radius = 7
    x, y = pt
    body_pos = rendering.Transform(translation=(x, y), rotation=angle)
    ant = make_ant()
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
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path, 'ant.png')
    ant = rendering.Image(filename, 30, 30)
    ant.set_color(1,1,1)
    return ant

def make_ant1():
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

