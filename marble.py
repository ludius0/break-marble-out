# libs
import pygame

# scripts
from entity import Entity

class Marble(Entity):
    """Note: when bouncing of paddle; use paddle delta values to project them to Marble"""
    def __init__(self, x, y, width, height, color=(0, 0, 255)):
        super().__init__(x, y, width, height, color)
        self.dx = 0.1
        self.dy = 0.1
        self.bounce_of = None
        self.velocity = 1
        self.mass = 1
    
    def get_deltas(self):
        return (self.dx, self.dy)
    
    def update_deltas(self, dx, dy):
        self.dx, self.dy = dx, dy
    
    def get_paddle_deltas(self, paddle):
        self.update_deltas(*paddle.get_deltas())

    def entity_coords(self, entity):
        """Record params of entity from collision"""
        self.collis_entity = entity.get_params(from_rect=True)

    def check_collision(self, *entities):
        """Return bool if collision with another entity. With 'Paddle' get also its deltas"""
        for entity in entities:
            if self.detect_collision(entity):
                if entity.__class__.__name__ == "Paddle":
                    self.get_paddle_deltas(entity)
                self.bounce_of = entity.__class__.__name__
                self.entity_coords(entity)
                return True
        return False
    
    def bounce_from_paddle(self):
        # get entities to find Paddle and based on abs(x, y) determine if update delta or bounce
        # return boolean
        pass
    
    def bounce(self):
        # get direction
        ex, ey, w, h = self.collis_entity
        dx, dy = self.get_deltas()
        if ex > self.x or ex+w < self.x: dx = -dx # left & right side
        if ey > self.y or ey+h < self.y: dy = -dy # up & down
        self.update_deltas(dx, dy)
    
    def update_pos(self):
        x = self.x + (self.dx * self.velocity)
        y = self.y + (self.dy * self.velocity)#**mass
        self.update_rect(x, y, self.width, self.height)

    def update(self, *entities):
        if self.check_collision(*entities):
            if not self.bounce_of == "Paddle":
                # if bounce_from_paddle: self.bounce
                self.bounce()
        self.update_pos()
            
        
