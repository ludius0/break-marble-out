# scripts
from game import *

pygame.init()

# init game structure
dtime = 10
win = Render((1000, 800))
player = Paddle(100, 25)
ball = Marble(10, 10)

# generate level
blocks = []
for i in range(0+50, 1000-100+50, 130):
        blocks.append(Block(100, 50, pos=Vec2(i, 40)))
blocks.append(Block(100, 50, pos=Vec2(300, 120)))
blocks.append(Block(100, 50, pos=Vec2(400, 200)))
blocks.append(Block(100, 50, pos=Vec2(420, 290)))
print("N of blocks:", len(blocks))

while 1:
    # draw game
    win.draw_bg()
    win.draw_entity(player, ball, *blocks)
    win.update()

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    
    # update game
    player.update(*blocks, dtime=dtime)
    ball.update(dtime=10)

"""    new_blocks = []
    for idx, b in enumerate(blocks):
        if not b.status: new_blocks.append(b)
    blocks = new_blocks"""

pygame.quit()
sys.exit()