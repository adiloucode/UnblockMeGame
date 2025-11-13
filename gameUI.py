import pygame as pg
from RandomGenerator import gridRandomGenerator
from logicToDisplay import gridToRects, gridsToMove, displayMatrixGrid
pg.init()

pg.display.set_caption('Unbolck Me Game')
screen = pg.display.set_mode((800,800))

# Colors
colors = {
'BOARD_COLOR' : (50,50,60),
'BLOCK_COLOR' : (180,180,200),
'RED' : (200, 50, 50),
'BG' : (20,20,25),
'GREEN': (0,255,0)
}


# Grid generation and drawing
root = gridRandomGenerator()
root.updateGrid()

# Movement parameters
selected = 'redCar'
direction = None
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            selected = root.selectVehicule(event.pos)
            print(selected)

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                direction = 'right'
                root.moveMyVehicule(selected, direction)
            elif event.key == pg.K_LEFT:
                direction = 'left'
                root.moveMyVehicule(selected, direction)
            elif event.key == pg.K_UP:
                direction = 'up'
                root.moveMyVehicule(selected, direction)
            elif event.key == pg.K_DOWN:
                direction = 'down'
                root.moveMyVehicule(selected, direction)
        elif event.type == pg.KEYUP:
            direction = None  

    root.drawGridBoard(screen, colors, selected)


