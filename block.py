# libs
import pygame

# scripts
from entity import Entity

class Block(Entity):
    def __init__(self, x, y, width, height, color=(255, 0, 0), **kwargs):
        super().__init__(x, y, width, height, color, **kwargs)
        self.destroyed = False
    
    def destroy(self): 
        self.destroyed = True
    
    def update(self): 
        return True if self.destroyed else False