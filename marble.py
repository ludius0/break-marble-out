# libs
import pygame
from math import e

# scripts
from entity import Entity

class Marble(Entity):
    """Note: when bouncing of paddle; use paddle delta values to project them to Marble"""
    def __init__(self, x, y, width, height, color=(0, 0, 255)):
        super().__init__(x, y, width, height, color)
        self.dx = 0
        self.dy = 0
        self.bounce_of = None
        self.velocity = 1
        self.mass = 1
        self.top_speed = 2
        # for accuracy
        self.collision_cooldown = 1000
        self.refresh_collision_cooldown()
    
    def refresh_collision_cooldown(self):
        self.collis_coold = self.collision_cooldown
    
    def regulate_speed(self, delta):
        """Regulate max speed of delta values, which updates positions (x, y)"""
        if abs(delta) > self.top_speed: 
            return abs(delta) / delta * self.top_speed
        return delta
    
    def update_deltas(self, dx, dy, add_velocity=False):
        """Replace current deltas with new ones"""
        self.prev_speed = (self.dx, self.dy)
        # regulate speed
        dx, dy = self.regulate_speed(dx), self.regulate_speed(dy)
        if not add_velocity: self.dx, self.dy = dx, dy
        else: # increase speed (in case of bounce_from_paddle())
            self.dx, self.dy = self.dx+dx, self.dx+dy # increase speed
            self.dx, self.dy = self.regulate_speed(self.dx), self.regulate_speed(self.dy)
    
    def get_paddle_deltas(self, paddle):
        """Save deltas from 'Paddle' class and update own if some movement"""
        dx, dy = paddle.get_deltas()
        if abs(dx)+abs(dy) > 0: self.update_deltas(dx, dy) ; return

    def entity_coords(self, entity):
        """Record params of entity from collision"""
        self.collis_entity = entity.get_params(from_rect=True)

    def check_collision(self, *entities):
        """Return bool if collision with another entity. With 'Paddle' get also its deltas"""
        for entity in entities:
            if self.detect_collision(entity):
                if entity.__class__.__name__ != "Paddle":
                    entity.destroy() # destroy blocks if not 'Paddle'
                else: self.get_paddle_deltas(entity)
                self.bounce_of = entity.__class__.__name__
                self.entity_coords(entity)
                self.refresh_collision_cooldown()
                return True
        return False
    
    def bounce_from_paddle(self):
        # get entities to find Paddle and based on abs(x, y) determine if update delta or bounce
        # return boolean
        dx, dy = self.prev_speed
        new_dx, new_dy = self.dx, self.dy
        # increse delta speed if 'Paddle' hit it with negative or non-negative x, y
        if (dx < 0 and self.dx < 0) or (dx > 0 and self.dx > 0): new_dx = dx
        if (dy < 0 and self.dy < 0) or (dy > 0 and self.dy > 0): new_dy = dy
        if not (new_dx == self.dx and new_dy == self.dy):
            self.update_deltas(new_dx, new_dy, add_velocity=True)
        else: self.bounce()
        
    def bounce(self):
        """Bounce from 'Blocks' entities (or from 'Paddle') by flipping to negative or positive deltas"""
        ex, ey, w, h = self.collis_entity
        dx, dy = self.get_deltas()
        #print(ex, ex+ew, ex+ew//2 < self.x)
        # left and right
        if ex > self.x: dx = dx *-1; print("ya")
        elif ex+w <= self.x+2: dx = dx *-1; print("yes")
        # top and bottom
        if ey > self.y: dy = dy *-1; print("duh")
        elif ey+h <= self.y+2: dy = dy *-1; print("no")
        self.update_deltas(dx, dy)
    
    def update_pos(self):
        x = self.x + (self.dx * self.velocity)
        y = self.y + (self.dy * self.velocity)#**mass
        self.update_rect(x, y, self.width, self.height)

    def update(self, *entities):
        if self.collis_coold > 0:
            if self.check_collision(*entities):
                if not self.bounce_of == "Paddle":
                    self.bounce()
                else: self.bounce_from_paddle()
            self.update_pos()
            return
        self.collision_cooldown -= 1