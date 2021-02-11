# libs
import pygame
import sys

# scripts
from parameters import Parameter
from render import Render
from paddle import Paddle
from miscellaneous import *

p = Parameter()
w = Render(p.window_size()) # window
player = Paddle(0, 0, 100, 50)
box1 = Box(500, 500, 100, 50, (255, 0, 0))
box2 = Box(520, 400, 100, 50, (100, 100, 0))

pygame.init()

pygame.display.set_mode(p.window_size())
#pygame.mouse.set_visible(False)

print("-"*20)

# main loop
running = True
while running:
    # draw objects and screen
    w.draw_bg()
    w.draw_entity(player, box1, box2)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    
    # update objects and screen
    player.update_pos(box1, box2)
    w.update()

pygame.quit()
sys.exit()