
import pyglet
from gym.envs.classic_control import rendering

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
        self.img = self.sub_images[n]
        self.last_sprite = n
    
    def next_sprite(self):
        self.last_sprite = (self.last_sprite + 1) % len(self.sub_images)
