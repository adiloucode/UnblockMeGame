import pygame as pg
from RandomGenerator import gridRandomGenerator
from logicToDisplay import gridToRects, gridsToMove, displayMatrixGrid
pg.init()

pg.display.set_caption('Unbolck Me Game')
screen = pg.display.set_mode((800,800))

# Colors
BOARD_COLOR = (50,50,60)
BLOCK_COLOR = (180,180,200)
RED = (200, 50, 50)
BG = (20,20,25)

# Board rectangle
margin = 5
board = pg.Rect(100,100, 600 + 7*margin, 600 + 7*margin)

# Grid generation and drawing
root = gridRandomGenerator()
print('====================================================================================')
root.displayGridInfo()
print('====================================================================================')
print(displayMatrixGrid(root.matrix))
print('====================================================================================')
rootRects = gridToRects(root, board, margin)
red_block = pg.Rect(board.x + margin, board.y + 3*margin + 200,200,100) 

""" # verticals
obstacles_v = []
obstacles_v.append(pg.Rect(board.x + 3*margin + 300, board.y + margin + 100, 100,200))


# horizontals
obstacles_h = []
for i in range(6):
    if i == 2:
        i+=1
    else:
        obstacles_h.append(pg.Rect(board.x + margin, board.y + (i+1)*margin + i*100, 200,100)) """


speed = 4
direction = 0
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                direction += 1
            elif event.key == pg.K_LEFT:
                direction -= 1
        elif event.type == pg.KEYUP:
            direction = 0  
    # update
    red_block.x += direction * speed

    # Clamp inside board horizontally
    left_bound = board.x
    right_bound = board.right - red_block.width
    red_block.x = max(left_bound + margin, min(red_block.x, right_bound - margin))
    
    screen.fill(BG)

    # Main Board
    pg.draw.rect(screen, BOARD_COLOR, board, border_radius = 10)
    # Red Vehicule
    pg.draw.rect(screen, RED, red_block, border_radius = 10)

    # Obstacles
    for rect in rootRects:
        pg.draw.rect(screen, BLOCK_COLOR, rect, border_radius = 10)

    """ # Horizontal Vehicules
    for rect in obstacles_h:
        pg.draw.rect(screen, BLOCK_COLOR, rect, border_radius= 10)

    # Vertical Vehicules
    for rect in obstacles_v:
        pg.draw.rect(screen, BLOCK_COLOR, rect, border_radius= 10)"""
    pg.draw.rect(screen, BLOCK_COLOR, rect, border_radius = 10)  
    pg.display.flip()