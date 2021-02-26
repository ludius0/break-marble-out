# libs
import pygame

# scripts
from .vector import Vec2
from .material import Material
from .entity import RectEntity

class Marble(RectEntity):
    """
    Pong ball that check for collision and calculate, where to go and how to bounce.
    """
    def __init__(self, width: int, height: int, pos=Vec2(600, 600), color=(0, 255, 0)) -> None:
        super().__init__(width, height, position=pos, color=color)
        self.acceleration += Vec2(-0.09, -0.09)
        self._last_bounce = [None, None]
    
    #def restrict_speed(self, limit=0.1):
    #    accelx, accely = self.acceleration.totuple
    #    if accelx > limit: self.acceleration = Vec2(limit, self.acceleration.y)
    #    elif accelx < -limit: self.acceleration = Vec2(-limit, self.acceleration.y)
    #    if accely > limit: self.acceleration = Vec2(self.acceleration.x, limit)
    #    elif accely < -limit: self.acceleration = Vec2(self.acceleration.x, -limit)

    def simulate_motion(self) -> None:
        """
        Move position with acceleration.
        """
        self.update_prev_pos()
        self.position += self.acceleration
    
    def _bounce_from(self, entity):
        self._last_bounce.append(entity)
        if len(self._last_bounce) > 2:
            self._last_bounce.pop(0)
    
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
            if collis != None and collis.__class__.__name__ != "Paddle":
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

        if (self.prev_pos.x<=x+w and self.prev_pos.x+self.width>=x and (self.prev_pos.y+self.height-1>=y+h or self.prev_pos.y+1<=y)) and \
            (self.position.x<=x+w and self.position.x+self.width>=x and (self.position.y+self.height-1>=y+h or self.position.y+1<=y)): # bounce from top and bottom
            self.acceleration = Vec2(self.acceleration.x, self.acceleration.y * -1)
        elif (self.prev_pos.y<=y+h and self.prev_pos.y+self.height>=y and (self.prev_pos.x+self.width>=x+w or self.prev_pos.x<=x)) and \
            (self.position.y<=y+h and self.position.y+self.height>=y and (self.position.x+self.width>=x+w or self.position.x<=x)):   # bounce from left and right sides
            self.acceleration = Vec2(self.acceleration.x * -1, self.acceleration.y)
        else:   # bounce from corners
            self.acceleration = Vec2(self.acceleration.x * -1, self.acceleration.y * -1)

    def update(self, *entities, dtime=1) -> None:
        """
        Backbone calculation for updating position of 'Marble'.
        """
        assert isinstance(dtime, int) and dtime != 0
        collis = self.check_collision(*entities)
        if collis != None:
            self._bounce(collis)

            if collis.__class__.__name__ == "Paddle":
                print(collis.velocity)
            #self._get_out(*entities)

        self._move()