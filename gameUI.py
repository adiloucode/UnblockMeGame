import pygame as pg
from RandomGenerator import gridRandomGenerator
from AI_Solvers import BFSsolver, DFSsolver, Astar
from logicToDisplay import display_AI_Solution, twoGridsToMove
import time
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
root = gridRandomGenerator(screen)
root.updateGrid()

# Movement parameters
selected = 'redCar'
direction = None
clock = pg.time.Clock()
running = True
AI_display_on = False
AI_solver = None
timer = None
timer_text = None

# Buttons

# AI solve button
button = pg.Rect(0,0,200,50)
button.centerx = root.board.centerx
button.top = root.board.bottom + 15
BUTTON_COLOR = (70,130,180)
BUTTON_HOVER = (100,160,210)
BUTTON_TEXT_COLOR = (255,255,255)
# pre-rendering
font = pg.font.Font(None,32)
button_text_surf = font.render('Solve with AI', True, BUTTON_COLOR)
button_text_rect = button_text_surf.get_rect(center = button.center)

# Algorithm options buttons
BFSButton = pg.Rect(screen.get_rect().centerx - 150, screen.get_rect().centery - 210,300,100)
BFS_text_surf = font.render('BFS Solver', True, BUTTON_COLOR)
BFS_text_rect = BFS_text_surf.get_rect(center = BFSButton.center)
DFSButton = pg.Rect(screen.get_rect().centerx - 150, screen.get_rect().centery - 50,300,100)
DFS_text_surf = font.render('DFS Solver', True, BUTTON_COLOR)
DFS_text_rect = DFS_text_surf.get_rect(center = DFSButton.center)
ASTARButton = pg.Rect(screen.get_rect().centerx - 150, screen.get_rect().centery + 110,300,100)
ASTAR_text_surf = font.render('ASTAR Solver', True, BUTTON_COLOR)
ASTAR_text_rect = ASTAR_text_surf.get_rect(center = ASTARButton.center)
separation = 10

""" BFSButton.centerx = screen.get_rect().centerx 
DFSButton.centerx = screen.get_rect().centerx
ASTARButton.centerx = screen.get_rect().centerx

BFSButton.centery = screen.get_rect().centery - DFSButton.height - separation
DFSButton.centery = screen.get_rect().centery
ASTARButton.centery = screen.get_rect().centery + DFSButton.height + separation """

BFS_COLOR   = (255, 90, 40)     # warm orange-red
DFS_COLOR   = (30, 60, 150)     # deep blue
ASTAR_COLOR = (150, 50, 200)    # royal purple
GREEN = (0,255,0) 
while running:
    screen.fill(colors['BG'])
    if AI_display_on:
        if not AI_solver:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if BFSButton.collidepoint(event.pos):
                        AI_solver = 'BFS'
                        start = time.time()
                        solution = BFSsolver(root)
                        end = time.time()
                        timer = end - start
                    elif DFSButton.collidepoint(event.pos):
                        AI_solver = 'DFS'
                        start = time.time()
                        solution = DFSsolver(root)
                        end = time.time()
                        timer = end - start
                    elif ASTARButton.collidepoint(event.pos):
                        AI_solver = 'A*'
                        start = time.time()
                        solution = Astar(root)
                        end = time.time()
                        timer = end - start
            buttons = [(BFSButton, BFS_COLOR), (DFSButton, DFS_COLOR), (ASTARButton, ASTAR_COLOR)]
            for i in range(len(buttons)):
                if buttons[i][0].collidepoint(pg.mouse.get_pos()):
                    buttons[i] = (buttons[i][0], GREEN)
            screen.fill(colors['BG'])
            for but, color in buttons:
                pg.draw.rect(screen, color, but, border_radius = 8)
            screen.blit(BFS_text_surf, BFS_text_rect)
            screen.blit(DFS_text_surf, DFS_text_rect)
            screen.blit(ASTAR_text_surf, ASTAR_text_rect)
            pg.display.flip()
            continue
        else:
            print(f'AIsolver = {AI_solver}')             
            if solution:
                timer_text = font.render(f'{AI_solver} Execution time : {timer:.4f} s', True, (255,255,255))
                next = solution.popleft()
                if twoGridsToMove(root, next):
                    vhcID, direction, step = twoGridsToMove(root, next)
                    print(f'solution length remaining: {len(solution)}')
                    print(f'move: {vhcID}, {direction}, {step}')
                    time.sleep(1)
                    root.moveMyVehicule(vhcID, direction, step)
            else:
                AI_solver = None
                AI_display_on = False
            
    else:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                selected = root.selectVehicule(event.pos)
                print(selected)
                if button.collidepoint(event.pos):
                    #AI Solution
                    AI_display_on = True
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

        mouse_pos = pg.mouse.get_pos()
        if button.collidepoint(mouse_pos):
            btn_color = BUTTON_HOVER
        else:
            btn_color = BUTTON_COLOR
        pg.draw.rect(screen, btn_color, button, border_radius = 8)
        screen.blit(button_text_surf,button_text_rect)
        if timer_text:
            screen.blit(timer_text, (root.board.left, root.board.top - 50))

    root.drawGridBoard(screen, colors, selected)
    pg.display.flip()

