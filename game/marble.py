# libs
import pygame

# scripts
from .vector import Vec2
from .material import Material
from .entity import RectEntity

class Marble(RectEntity):
    def __init__(self, width: int, height: int, pos=Vec2(600, 600), color=(0, 255, 0)) -> None:
        super().__init__(width, height, position=pos, color=color)
        self.acceleration = Vec2(-0.01, -0.01)
    
    def update(self, dtime=1) -> None:
        assert isinstance(dtime, int) and dtime != 0

        self.simulate_motion(dtime)
        self.update_rect()