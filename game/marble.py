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
        self.acceleration = Vec2(-0.009, -0.009)
    
    def restrict_speed(self, limit=0.1):
        accelx, accely = self.acceleration.totuple
        if accelx > limit: self.acceleration = Vec2(limit, self.acceleration.y)
        elif accelx < -limit: self.acceleration = Vec2(-limit, self.acceleration.y)
        if accely > limit: self.acceleration = Vec2(self.acceleration.x, limit)
        elif accely < -limit: self.acceleration = Vec2(self.acceleration.x, -limit)

    def simulate_motion(self, dtime: float) -> None:
        #self.velocity = self.position - self.prev_pos
        self.restrict_speed()
        self.position += self.acceleration #* dtime**2.
    
    def _bounce_of(self, collis_ent) -> None:
        x, y = collis_ent.position
        w, h = collis_ent.width, collis_ent.height
        mx, my = self.position.totuple
        mw, mh = self.width, self.height

        if (mx==x and my==y) or (mx+mw==x+w and my==y) or (mx==x and my+mh==y+h) or (mx+mw==x+w and my+mh==y+h):
            self.acceleration = Vec2(-self.acceleration.x, -self.acceleration.y)
        elif self.position.x<=x+w and self.position.x+self.width>=x\
            and (self.position.y+self.height>=y+h or self.position.y<y):
            self.acceleration = Vec2(self.acceleration.x, -self.acceleration.y)
        else:
            self.acceleration = Vec2(-self.acceleration.x, self.acceleration.y)
    
    def _move(self, dtime):
        self.simulate_motion(dtime)
        self.update_rect()
    
    def _out_of(self, *entities):
        while 1:
            if self.check_collision(*entities) == None:
                break
            else:
                self._move(1)

    def _collision(self, *entities, dtime=1):
        collis = self.check_collision(*entities)
        if collis != None:
            if collis.__class__.__name__ == "Paddle":
                paddle_vel = (collis.position - collis.prev_pos).neg()
                print(paddle_vel, self.acceleration)
                self.acceleration += paddle_vel / 1000000 if paddle_vel != Vec2(0., 0.) else 0
            self._bounce_of(collis)
            self._move(dtime)
            self._out_of(*entities)
            #self._collision(*entities, dtime=1)
        return
    
    def _steps(self, *entities, dtime=1) -> None:
        for step in range(1, 1+dtime):
            self._move(step)
            self._collision(*entities, dtime=step)


    def update(self, *entities, dtime=1) -> None:
        assert isinstance(dtime, int) and dtime != 0
        self._steps(*entities, dtime=dtime)