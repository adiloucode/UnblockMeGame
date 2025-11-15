from collections import deque
from IPython.display import clear_output
from classes import *
from integrityCheckers import *

# To be added in Grid class
def displayMatrixGrid(matrix):
    for row in matrix:
        print(' '.join(str(x) for x in row))

# Usefull
def listOfMoves(solution):
    win = solution  
    finalMoves = deque()
    while solution.parent != None:
        finalMoves.appendleft(solution)
        solution = solution.parent
    finalMoves.appendleft(solution)
    return finalMoves

# To Be Rebranded
def twoGridsToMove(grid1, grid2):
    if not compareVehicules(grid1.redCar, grid2.redCar):
        move = ('redCar', (grid2.redCar.position[0] - grid1.redCar.position[0]), (grid2.redCar.position[1] - grid1.redCar.position[1]))
        if move[2] < 0:
            return('redCar', 'left', (-1)*move[2])
        elif move[2] > 0:
            return('redCar', 'right', move[2])
        else:
            print('different redCar stats, but no move ?!')
    else:
        for i in range(len(grid1.obstacles)):
            if not compareVehicules(grid1.obstacles[i], grid2.obstacles[i]):
                move = (i, grid2.obstacles[i].position[0] - grid1.obstacles[i].position[0], grid2.obstacles[i].position[1] - grid1.obstacles[i].position[1])
                # if compared vehicules are horizontal
                if move[1] == 0:
                    if move[2] < 0:
                        return(i, 'left', (-1)*move[2])
                    elif move[2] > 0:
                            return(i, 'right', move[2])
                    else:
                            print(f'different {i}th obstacle stats, but no horizontal move ... one is horizontal')
                # elif compared vehicules are vertical
                elif move[2] == 0:
                    if move[1] < 0:
                        return(i, 'up', (-1)*move[1])
                    elif move[1] > 0:
                            return(i, 'down', move[1])
                    else:
                            print(f'different {i}th obstacle stats, but no horizontal move ... one is vertical')
    print(f'No move to make !')
    return None

def display_AI_Solution(finalMoves, screen, colors):
    actual = finalMoves.popleft()
    win = finalMoves.pop()
    while finalMoves:
        next = finalMoves.popleft()
        displayMatrixGrid(next.matrix)
        vhcID, direction, step = twoGridsToMove(actual, next)
        actual.moveMyVehicule(vhcID, direction, step)
        #screen.fill(colors['BG'])
        #actual.drawGridBoard(screen, colors)
        #pg.display.flip()
        if not compareGrids(actual, next):
             print('error in move ?!')
        time.sleep(1)
        clear_output(wait = True)
    displayMatrixGrid(win.matrix)
    return True
