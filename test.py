# libs
import pygame
import time
import sys

# scripts
from parameters import Parameter
from render import Render
from paddle import Paddle
from block import *
from marble import Marble
from miscellaneous import *

p = Parameter()
w = Render(p.window_size()) # window
player = Paddle(500, 500, 100, 50)
ball = Marble(450, 450, 14, 14)

wh, hg = p.window_size()
wall1 = UnbrekableBlock(0, 0, wh, 20, color=(200, 200, 200)) # top
wall2 = UnbrekableBlock(wh-20, 0, 20, hg, color=(200, 200, 200)) # right
wall3 =  UnbrekableBlock(0, hg-20, wh, 20, color=(200, 200, 200)) # bottom
wall4 = UnbrekableBlock(0, 0, 20, hg, color=(200, 200, 200)) # left
walls = [wall1, wall2, wall3, wall4]

pygame.init()

pygame.display.set_mode(p.window_size())
#pygame.mouse.set_visible(False)

# generate level
blocks = []
for i in range(0+50, p.width-100+50, 120):
    blocks.append(Block(i, 40, 100, 50, color=(255, 0, 0)))
print("N of blocks:", len(blocks))


print("-"*20)

FPS = 100
clock = pygame.time.Clock() # Create a clock object

# main loop
running = True
while running:
    #time.sleep(0.01)
    clock.tick(FPS)

    # draw objects and screen
    w.draw_bg()
    w.draw_entity(player, ball, *blocks, *walls)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        # NOTE: get mouse pos from here
    
    # update objects (their pos) and screen
    player.update(*blocks, *walls)
    ball.update(player, *blocks, *walls)
    w.update()

    new_blocks = []
    for idx, b in enumerate(blocks):
        if not b.status(): new_blocks.append(b)
    blocks = new_blocks

pygame.quit()
sys.exit()