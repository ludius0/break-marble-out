# libs
import pygame
import sys

# scripts
from parameters import Parameter
from render import Render
from paddle import Paddle
from block import Block
from marble import Marble
from miscellaneous import *

p = Parameter()
w = Render(p.window_size()) # window
player = Paddle(500, 500, 100, 50)
ball = Marble(450, 450, 10, 10)
wh, hg = p.window_size()

wall1 = Wall(0, 0, wh, 10, color=(200, 200, 200)) # top
wall2 = Wall(wh-10, 0, 10, hg, color=(200, 200, 200)) # right
wall3 =  Wall(0, hg-10, wh, 10, color=(200, 200, 200)) # bottom
wall4 = Wall(0, 0, 10, hg, color=(200, 200, 200)) # left
walls = [wall1, wall2, wall3, wall4]

pygame.init()

pygame.display.set_mode(p.window_size())
#pygame.mouse.set_visible(False)

# generate level
blocks = []
for i in range(0+50, p.width-100+50, 120):
    blocks.append(Block(i, 40, 100, 50, color=(255, 0, 0), center=True))
print(len(blocks))


print("-"*20)

# main loop
running = True
while running:
    ## FPS delay ##

    # draw objects and screen
    w.draw_bg()
    w.draw_entity(player, ball, *blocks, *walls)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    
    ## loop for destroying blocks
    
    # update objects (their pos) and screen
    player.update(*blocks, *walls)
    ball.update(player, *blocks, *walls)
    w.update()

pygame.quit()
sys.exit()