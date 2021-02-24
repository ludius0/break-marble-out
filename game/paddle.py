# libs
import pygame

# scripts
from .vector import Vec2
from .material import Material
from .entity import RectEntity

class Paddle(RectEntity):
    """
    Player that is controled by the computer mouse. 
    If it (will) hit a wall or a 'Block', 
    than it won't update until the mouse move away to some free space.
    """
    def __init__(self, width: int, height: int, pos=Vec2(600, 600), color=(0, 0, 255)) -> None:
        super().__init__(width, height, position=pos, color=color)
    
    def get_mouse_pos(self) -> Vec2:
        """Get mouse position from pygame and create new Vec2, where it will slightly adjust it based on width and height of 'Paddle'"""
        x, y = pygame.mouse.get_pos()
        xw, yh = self.get_middle()
        return Vec2(x-xw, y-yh)
    
    def _steps(self, delta_pos, dtime, *entities) -> None:
        """
        This function is creatings steps from start position (self.position) to end position (self.position+(delta_pos*dtime) ->
        where delta_pos is self.position-'destination_pos'). In every step it will create same rectangle, check for collision and update self.rect.
        If collision is True, than it will try to slide acros X or Y dimension by calling this function (with new final position, which is different at X or Y from self.position).
        If it can't slide, than it will break from iterations of steps. The size of steps is determined by dtime, which is its lenght.
        """
        _pos = self.position # remember starting position
        for step in range(1, 1+dtime):
            new_pos = _pos + (delta_pos*step) # new pos based on step (to final destination)
            testing_rect = pygame.Rect(*new_pos, self.width, self.height) # create rect on new pos to check if collision occure
            # check if in new position is some collision
            collis = self.check_collision(*entities, rect=testing_rect)
            if collis != None:
                # Try slide across Y
                new_pos_y = Vec2(self.position.x, new_pos.y) # pos along new Y
                rect_y = pygame.Rect(*new_pos_y, self.width, self.height)   # rect from new Y to check collision
                if self.check_collision(*entities, rect=rect_y) == None: # if any collision on new Y pos, than call present function with new parameters (as destination)
                    distance = new_pos_y - self.position
                    delta_pos = distance / dtime
                    self._steps(delta_pos, dtime, *entities)
                    break

                # Try slide across X (same like Y)
                new_pos_x = Vec2(new_pos.x, self.position.y)
                rect_x = pygame.Rect(*new_pos_x, self.width, self.height)
                if self.check_collision(*entities, rect=rect_x) == None:
                    distance = new_pos_x - self.position
                    delta_pos = distance / dtime
                    self._steps(delta_pos, dtime, *entities)
                    break
                break
            # update position and rectangle (pygame)
            self.position = new_pos
            self.update_rect()



    def update(self, *entities, dtime=1) -> None:
        assert isinstance(dtime, int) and dtime != 0

        # coordinations
        mouse_pos = self.get_mouse_pos()
        distance = mouse_pos - self.position
        delta_pos = distance / dtime

        self._steps(delta_pos, dtime, *entities)