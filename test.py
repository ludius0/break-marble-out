# scripts
from game import *

pygame.init()

# init game structure
dtime = 10
win = Render((1000, 800))
player = Paddle(100, 50)
ball = Marble(12, 12)

# generate level
blocks = []
for i in range(0+50, 1000-100+50, 130):
        blocks.append(Block(100, 50, pos=Vec2(i, 40)))
blocks.append(Block(100, 50, pos=Vec2(300, 120)))
blocks.append(Block(100, 50, pos=Vec2(400, 200)))
blocks.append(Block(100, 50, pos=Vec2(420, 290)))
print("N of blocks:", len(blocks))
wall1 = Block(1000, 10, pos=Vec2(0, 0))
wall2 = Block(1000, 10, pos=Vec2(0, 800-10))
wall3 = Block(10, 800, pos=Vec2(0, 0))
wall4 = Block(10, 800, pos=Vec2(1000-10, 0))
walls = [wall1, wall2, wall3, wall4]

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
    ball.update(player, *blocks, *walls, dtime=1)
    player.update(ball, *blocks, *walls, dtime=dtime)

"""    new_blocks = []
    for idx, b in enumerate(blocks):
        if not b.status: new_blocks.append(b)
    blocks = new_blocks"""

pygame.quit()
sys.exit()