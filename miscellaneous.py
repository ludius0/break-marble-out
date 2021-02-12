# libs
import pygame

# scripts
from entity import Entity

class Wall(Entity):
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        super().__init__(x, y, width, height, color)