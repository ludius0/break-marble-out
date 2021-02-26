# libs
import pygame
from math import pi

# scripts
from .vector import Vec2
from .material import Material
from .entity import RectEntity

class Marble(RectEntity):
    """
    Pong ball that check for collision and calculate, where to go and how to bounce.
    """
    def __init__(self, width: int, height: int, pos=Vec2(600, 550), color=(0, 255, 0)) -> None:
        super().__init__(width, height, position=pos, color=color)
        self.acceleration += Vec2(-0.1, -0.1)
    
    def restrict_speed(self, limit=1.2):
        """
        Restrict speed of acceleratin, which is later used in simulate_motion() to update position.
        """
        accelx, accely = self.acceleration.totuple
        if accelx > limit: self.acceleration = Vec2(limit, self.acceleration.y)
        elif accelx < -limit: self.acceleration = Vec2(-limit, self.acceleration.y)
        if accely > limit: self.acceleration = Vec2(self.acceleration.x, limit)
        elif accely < -limit: self.acceleration = Vec2(self.acceleration.x, -limit)

    def simulate_motion(self) -> None:
        """
        Move position with acceleration. Update previous position and restrict speed of acceleration.
        """
        self.update_prev_pos()
        self.restrict_speed()
        self.position += self.acceleration * (self.dtime**-1)
    
    def _move(self) -> None:
        """
        Update position based on acceleration and update pygame.Rect in 'RectEntity'
        """
        self.simulate_motion()
        self.update_rect()
    
    def _get_out(self, *entities) -> None:
        """
        If stuck in some entities than update way out.
        """
        while 1:
            collis = self.check_collision(*entities)
            if collis != None:
                self._bounce(collis)
                self._move()
            else:
                break
    
    def _bounce(self, entity: RectEntity) -> None:
        """
        Change acceleration direction based on entity position and 'Marble' position.
        It is changing direction like bouncing of without any friction.
        """
        x, y = entity.position.totuple
        w, h = entity.width, entity.height

        # overwhelmingly accurate way to find
        if (self.prev_pos.x<=x+w-1 and self.prev_pos.x+self.width>=x+1 and (self.prev_pos.y+self.height//2>=y+h or self.prev_pos.y<=y)) and \
            (self.position.x<=x+w-1 and self.position.x+self.width>=x+1 and (self.position.y+self.height//2>=y+h or self.position.y<=y)): # bounce from top and bottom
            self.acceleration = self.acceleration.neg_y()
        elif (self.prev_pos.y<=y+h-1 and self.prev_pos.y+self.height>=y+1 and (self.prev_pos.x+self.width>=x+w or self.prev_pos.x<=x)) and \
            (self.position.y<=y+h-1 and self.position.y+self.height>=y+1 and (self.position.x+self.width>=x+w or self.position.x<=x)):   # bounce from left and right sides
            self.acceleration = self.acceleration.neg_x()
        else:   # bounce from corners
            self.acceleration = self.acceleration.rotated_degrees(180)

    def update(self, *entities, dtime=1) -> None:
        """
        Backbone calculation for updating position of 'Marble'.
        """
        assert isinstance(dtime, int) and dtime != 0
        self.dtime = dtime
        for step in range(1, 1+dtime):
            collis = self.check_collision(*entities)
            if collis != None:
                self._bounce(collis)

                # depending on velocity of paddle and so on. It will 
                if collis.__class__.__name__ == "Paddle":
                    """Notes:
                    1. if paddle is coming from same direction than really slow down
                    2. if paddle is coming from opposite direction than add velocity
                    3. bounce to direction based on place of paddle (use rotate vector)
                    """
                    self.acceleration += collis.velocity #* collis.material.bounce
            self._move()