# libs
import pygame

# scripts
from entity import Entity

class BaseBlock(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destroyed = False
    
    def destroy(self): 
        self.destroyed = True
    
    def status(self):
        return self.destroyed


class Block(BaseBlock):
    def __init__(self, x, y, width, height, color=(255, 0, 0), **kwargs):
        super().__init__(x, y, width, height, color=color, **kwargs)


class UnbrekableBlock(BaseBlock): # use it as wall
    def __init__(self, x, y, width, height, color=(255, 0, 0), **kwargs):
        super().__init__(x, y, width, height, color=color, **kwargs)
    def destroy(self): pass