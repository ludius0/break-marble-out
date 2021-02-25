# libs
import pygame

# scripts
from .vector import Vec2
from .material import Material

class Entity():
    """
    Basic backbone of all game interactive elements. It stores its position or velocity or acceleration as vector (Vec2) and additional information as 'Material',
    which is for computing 'Marble' velocity, speed and bouncness.
    """

    _velocity = Vec2.zeros() # delta x and delta y
    _acceleration = Vec2.zeros() # like gravity

    def __init__(self, position=Vec2.zeros(), material=Material(mass=0), color=(255, 0, 0)) -> None:
        assert isinstance(position, Vec2) and isinstance(material, Material)
        assert isinstance(color, tuple) and len(color) == 3
        self._position = position
        self._prev_pos = position
        self._material = material
        self.color = color
    
    def __repr__(self) -> str:
        return f"Entity: '{type(self).__name__}'; Pos: {self.position}); Mat: {self.material}"
    
    def accelerate(self, rate: float, dtime: float) -> None:
        self.acceleration += rate * dtime
    
    def reset_forces(self) -> None:
        self.acceleration = Vec2.zeros()

    @property
    def position(self) -> Vec2:
        return self._position
    
    @position.setter
    def position(self, new_vec: Vec2) -> None:
        assert isinstance(new_vec, Vec2)
        self.prev_pos = self._position
        self._position = new_vec
        self.velocity = self.position - self.prev_pos
    
    @property
    def prev_pos(self) -> Vec2:
        return self._prev_pos
    
    @prev_pos.setter
    def prev_pos(self, new_vec: Vec2) -> None:
        assert isinstance(new_vec, Vec2) 
        self._prev_pos = new_vec

    @property
    def velocity(self) -> Vec2:
        return self._velocity
    
    @velocity.setter
    def velocity(self, new_vec: Vec2) -> None:
        assert isinstance(new_vec, Vec2) 
        self._velocity = new_vec
    
    @property
    def acceleration(self) -> Vec2:
        return self._acceleration
    
    @acceleration.setter
    def acceleration(self, new_vec: Vec2) -> None:
        assert isinstance(new_vec, Vec2) 
        self._acceleration = new_vec

    @property
    def material(self) -> Material:
        return self._material
    
    @material.setter
    def material(self, new_mat: Material) -> None:
        assert isinstance(new_mat, Material) 
        self._material = new_mat


class RectEntity(Entity):
    """On top of 'Entity' class. Holds parameters for pygame libs."""
    def __init__(self, width: int, height: int, **kwargs) -> None:
        assert isinstance(width, (int, float)) and isinstance(height, (int, float))
        super().__init__(**kwargs)
        self.width, self.height = width, height
        self.update_rect()
    
    def update_rect(self):
        self._rect = pygame.Rect(*self.position, self.width, self.height)

    def detect_collision(self, entity, rect) -> bool:
        """Collision with another 'RectEntity'. Return bool."""
        assert isinstance(entity, RectEntity)
        return rect.colliderect(entity.rect)
    
    def check_collision(self, *entities, rect=None) -> None or "RectEntity":
        """Check if one from all entities (as 'RectEntity') provided as argument is colliding with this 'RectEntity'. Return None or RectEntity."""
        if rect == None: rect = self.rect
        for entity in entities:
            if self.detect_collision(entity, rect):
                return entity
        return None
    
    def get_color(self):
        return self.color
  
    def get_middle(self):
        return self.width//2, self.height//2
    
    @property
    def rect(self) -> pygame.Rect:
        return self._rect
    
    @rect.setter
    def rect(self, *args) -> None:
        """Update coordinations and form of Entity"""
        if len(args) == 1: # pygame.Rect
            self.rect = args[0]
        elif len(args) == 4: # [x, y, width, height]
            self.rect.update(args[0], args[1], args[2], args[3])
        else: 
            raise Exception(f"Error with input -> want: pygame.Rect or [x, y, width, height], but got {args}")