from collections import deque
from IPython.display import clear_output
from classes import *
from integrityCheckers import *

def displayMatrixGrid(matrix):
    for row in matrix:
        print(' '.join(str(x) for x in row))

def solvePuzzle(solution):  
    win = solution  
    finalMoves = deque()
    while solution.parent != None:
        finalMoves.appendleft(solution)
        solution = solution.parent
    while finalMoves:
        move = finalMoves.popleft()
        displayMatrixGrid(move.matrix)
        time.sleep(1)
        clear_output(wait = True)
    displayMatrixGrid(win.matrix)

def gridToRects(grid, board = None, margin = 5):
    if board:
        x = board.x
        y = board.y
    else:
        x = 100
        y = 100

    obstacles = []
    for i, obstacle in enumerate(grid.obstacles):
        if obstacle.orientation == 'horizontal':
            obstacles.append(pg.Rect(x + obstacle.position[1]*100 + (obstacle.position[1] + 1)*margin, y + obstacle.position[0]*100 + (obstacle.position[0] + 1)*margin, obstacle.length*100,100))
        elif obstacle.orientation == 'vertical':
            obstacles.append(pg.Rect(x + obstacle.position[1]*100 + (obstacle.position[1] + 1)*margin, y + obstacle.position[0]*100 + (obstacle.position[0] + 1)*margin, 100, obstacle.length*100))
        else:
            print(f'Vehicule {i} has broken orientation')
    return(obstacles)

def gridsToMove(grid1, grid2):
    if not compareVehicules(grid1.redCar, grid2.redCar):
        return ('redCar',100 * (grid2.redCar.position[0] - grid1.redCar.position[0]), 100 * (grid2.redCar.position[1] - grid1.redCar.position[1]))
    else:
        for i in range(len(grid1.obstacles)):
            if not compareVehicules(grid1.obstacles[i], grid2.obstacles[i]):
                return (i, grid2.obstacles[i].position[0] - grid1.obstacles[i].position[0], grid2.obstacles[i].position[1] - grid1.obstacles[i].position[1])
        print(f'No move to make !')
        return None

def moveVehiculeByCoords(vehicule, move):
    vehicule.position[0] += move[0]
    vehicule.position[1] += move[1]

def displayGame(solution, disRedCar, disSolution):
    actual = solution[0]
    for i in range(1, len(solution)):
        move = gridsToMove(actual, solution[i])
        if move[0] == 'redCar':
            actual.redCar.moveVehiculeByCoords((move[1],move[2]))
            disRedCar.x += move[1]*100
            disRedCar.y += move[2]*100
        else:
            actual.obstacles[i].moveVehiculeByCoords((move[1],move[2]))
            disSolution[i].x += move[1]*100
            disSolution[i].y += move[2]*100  