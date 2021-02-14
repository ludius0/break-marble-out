# libs
import pygame

class Entity():
    def __init__(self, x, y, width, height, color):
        # Parameters
        self.rect = pygame.Rect(x, y, width, height) # init rect parameters
        self._color = color
        # delta values for updating its movement
        self._dx = 0 
        self._dy = 0
    
    def __repr__(self):
        return f"Entity: '{type(self).__name__}'; Rect: color{self.color}, params(x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height})"
    
    def get_deltas(self):
        return (self.dx, self.dy)
    
    def get_color(self):
        return self.color
    
    def get_pos(self, center=False):
        if center: return (self.x - self.width // 2, self.y - self.height // 2)
        return (self.x, self.y)
    
    def get_params(self):
        return (self.x, self.y, self.width, self.height)
    
    def get_rect(self):
        return self.rect
    
    def update_deltas(self, dx, dy):
        self.dx, self.dy = dx, dy
    
    def update_rect(self, *args):
        """Update coordinations and form of Entity"""
        if len(args) == 1: # pygame.Rect
            self.rect = args[0]
        elif len(args) == 4: # [x, y, width, height]
            self.rect.update(args[0], args[1], args[2], args[3])
        else: 
            raise Exception(f"Error with input -> want: pygame.Rect or [x, y, width, height], but got {args}")
    
    def detect_collision(self, entity):
        """Collision with another Entity. Return bool."""
        if not isinstance(entity, type(Entity)):
            return self.rect.colliderect(entity)
        return self.rect.colliderect(entity.get_rect())

    ### coords
    @property
    def x(self): return self.rect.left
    
    @x.setter
    def x(self, value): self.rect.update(value, y, width, height)

    @property
    def y(self): return self.rect.top
    
    @y.setter
    def y(self, value): self.rect.update(x, value, width, height)

    @property
    def width(self): return self.rect.width
    
    @width.setter
    def width(self, value): self.rect.update(x, y, value, height)

    @property
    def height(self): return self.rect.height
    
    @height.setter
    def height(self, value): self.rect.update(x, y, width, value)

    ### params
    @property
    def color(self): return self._color
    
    @color.setter
    def color(self, value): self._color = value

    @property
    def dx(self): return self._dx
    
    @dx.setter
    def dx(self, value): self._dx = value

    @property
    def dy(self): return self._dy
    
    @dy.setter
    def dy(self, value): self._dy = value
