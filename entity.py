# import libs
import pygame

class Entity():
    def __init__(self, x, y, width, height, color):
        """        if not isinstance(color, tuple) or not len(color) == 3:
            raise Exception(f"Color should be tuple of lenght RGB colors. Got {type(color)} of lenght {len(color)}!")
        if not isinstance(size, tuple) or not len(size) == 4:
            raise Exception(f"Size should be tuple of lenght (x, y, width, height). Got {type(size)} of lenght {len(size)}!")"""
        # Parameters
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height) # init rect parameters
        self.color = color
    
    def __repr__(self):
        return f"Entity: '{type(self).__name__}'; Rect: color{self.color}, params(x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height})"
    
    def get_color(self):
        return self.color
    
    def get_pos(self, center=False):
        if center: return (self.x - self.width // 2, self.y - self.height // 2)
        return (self.x, self.y)
    
    def get_rect(self):
        return self.rect
    
    def update_params(self, x, y, width, height):
        """Update parameters in Entity class"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def update_rect(self, *args):
        """Update coordinations and form of Entity"""
        if len(args) == 1: # pygame.Rect
            self.rect = args[0]
        elif len(args) == 4: # [x, y, width, height]
            self.rect.update(args[0], args[1], args[2], args[3])
        else: 
            raise Exception(f"Error with input -> want: pygame.Rect or [x, y, width, height], but got {args}")
        self.update_params(self.rect.left, self.rect.top, self.rect.width, self.rect.height) # update params
    
    def detect_collision(self, entity):
        """Collision with another Entity. Return bool."""
        if not isinstance(entity, type(Entity)):
            return self.rect.colliderect(entity)
        return self.rect.colliderect(entity.get_rect())