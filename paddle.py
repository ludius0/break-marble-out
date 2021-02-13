# libs
import pygame
from math import e # euler number

# scripts
from entity import Entity

class Paddle(Entity):
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        """Entity which is controled by player's mouse."""
        super().__init__(x, y, width, height, color)
        self.lock_pos = False
        self.top_speed = 11
    
    def delta_new_pos(self):
        """Calculate delta coordinations to get to mouse coordinations."""
        x, y = pygame.mouse.get_pos()
        x, y = x - self.width // 2, y - self.height // 2 # get center
        self.dx, self.dy = x - self.x, y - self.y   # difference between new coordination and old
        ## regulate speed
        if abs(self.dx) > e*self.top_speed: self.dx = abs(self.dx) / self.dx * e*self.top_speed # setting top speed limit for dx
        if abs(self.dy) > e*self.top_speed: self.dy = abs(self.dy) / self.dy * e*self.top_speed # setting top speed limit for dy
        return (self.dx, self.dy)
    
    def check_collision(self, *entities):
        """Entity collision. Return bool and save data about collision for '(un)locking' paddle movement"""
        self.shadow_rect = pygame.Rect(self.x+self.dx, self.y+self.dy, self.width, self.height) # w+1, h+1 for small accuracy
        for entity in entities:
            if entity.detect_collision(self.shadow_rect):
                self.record_ent_pos = entity.get_pos(center=True)
                return True
        return False
    
    def try_unlocked(self):
        """If position is locked (because of incoming collision). Unlock, when mouse get to correct position"""
        x, y = pygame.mouse.get_pos() # current x, y
        lx, ly = self.lock_coord
        ex, ey = self.record_ent_pos
        #print((x, y), (ex, ey), (lx, ly))
        if ex > lx and x <= lx: self.lock_pos = False; return
        if ex < lx and x >= lx: self.lock_pos = False; return
        if ey > ly and y <= ly: self.lock_pos = False; return
        if ey < ly and y >= ly: self.lock_pos = False; return

    
    def update(self, *entities):
        """Movemement of paddle (based on collisions with entities). Moving by mouse movement"""
        if not self.lock_pos:
            self.delta_new_pos()
            if not all(entities): # if any entities, than only move there
                self.update_rect(self.x + self.dx, self.y + self.dy, self.width, self.height)
                return
            if not self.check_collision(*entities): # if entities in input, check collisions with them
                self.update_rect(self.shadow_rect)
                return
            self.lock_coord = (self.x - self.width // 2, self.y - self.height // 2) # get center
            self.lock_pos = True # if get stuck
        self.try_unlocked()