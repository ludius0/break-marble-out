# libs
import pygame

# scripts
from .vector import Vec2
from .material import Material
from .entity import RectEntity

class Block(RectEntity):
    def __init__(self, width: int, height: int, pos=Vec2(100, 100)):
        super().__init__(width, height, position=pos)
        self.destroyed = False

    @property
    def status(self) -> float:
        return self.destroyed
    
    @status.setter
    def status(self, value: bool) -> None:
        assert isinstance(value, bool)
        self.destroyed = value
    
    def speciality(self, *args, **kwargs):
        """Each type of block will perform own attribute to the game."""
        pass
