from collections import deque
from classes import *
from integrityCheckers import *
from RandomGenerator import gridRandomGenerator

# Blind Search

def BFSsolver(rootGrid):
    queue = deque()
    visited = []
    queue.append(rootGrid)
    cpt = 0
    while queue:
        head = queue.popleft()
        print(f' visited so far:           {len(visited)}')
        if finalState(head):
            print('End of search, Puzzle solved !')
            return(head)
        elif not movesInAllMoves([head], visited):
            visited.append(head)
            sons = head.allPossibleMoves()
            for son in sons:
                son.setParent(head)
                queue.append(son)
            print(f'Sons of head {cpt} : {len(sons)}')
        else:
            print('No win, already visited !')
    print('Broke out of the loop, no solution')
    return None

def DFSsolver(rootGrid):
    queue = deque()
    visited = []
    queue.append(rootGrid)
    cpt = 0
    while queue:
        head = queue.pop()
        print(f' visited so far:           {len(visited)}')
        if finalState(head):
            print('End of search, Puzzle solved !')
            return(head)
        elif not movesInAllMoves([head], visited):
            visited.append(head)
            sons = head.allPossibleMoves()
            for son in sons:
                son.setParent(head)
                queue.append(son)
            print(f'Sons of head {cpt} : {len(sons)}')
        else:
            print('No win, already visited !')
    print('Broke out of the loop, no solution')
    return None

# Informed Search

def weight(root, grid):
    if compareGrids(root,grid):
        return 0
    else:
        cpt = 0
        for i in range(len(grid.obstacles)):
            if not compareVehicules(root.obstacles[i], grid.obstacles[i]):
                cpt += 1
        if not compareVehicules(root.redCar, grid.redCar):
            cpt += 1
        return cpt

def heuristic(grid):
    values = []
    if grid.redCar.position[1] == 4:
        return 0
    for j in range(grid.redCar.position[1]+2 ,6):
        values.append(grid.matrix[2][j])
    vals = set(values)
    if 0 in vals:
        vals.remove(0)
    return len(vals)

def setObjectiveValue(root, grid):
    grid.objectiveValue = weight(root, grid) + heuristic(grid)
    return grid

def reorder(movesList):
    for i in range(len(movesList)):
        for j in range(i+1, len(movesList)):
            if movesList[i].objectiveValue < movesList[j].objectiveValue:
                x = movesList[j].objectiveValue
                movesList[j].objectiveValue = movesList[i].objectiveValue
                movesList[i].objectiveValue = x
    return movesList

def Astar(rootGrid):
    queue = []
    visited = []
    setObjectiveValue(rootGrid, rootGrid)
    queue.append(rootGrid)
    cpt = 0
    while queue:
        reorder(queue)
        head = queue[0]
        queue.remove(head)
        print(f' visited so far:           {len(visited)}')
        if finalState(head):
            print('End of search, Puzzle solved !')
            return(head)
        elif not movesInAllMoves([head], visited):
            visited.append(head)
            sons = head.allPossibleMoves()
            for son in sons:
                son.setParent(head)
                setObjectiveValue(rootGrid, son)
                queue.append(son)
            print(f'Sons of head {cpt} : {len(sons)}')
        else:
            print('No win, already visited !')
    print('Broke out of the loop, no solution')
    return None

