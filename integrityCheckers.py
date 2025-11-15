
def compareVehicules(vhc, vhc2):
    if vhc.position == vhc2.position and vhc.orientation == vhc2.orientation and vhc.length == vhc2.length:
        return True
    else:
        return False

def compareGrids(grid, grid2):
    indicator = False
    if compareVehicules(grid.redCar, grid2.redCar) and len(grid.obstacles) == len(grid2.obstacles):
        for i in range(len(grid.obstacles)):
            if not compareVehicules(grid.obstacles[i], grid2.obstacles[i]):
                return False
        return True
    else:
        return False
    
def gridInGridsList(grid, list1):
    if list1:
        for grid1 in list1:
            if compareGrids(grid, grid1):
                return True
        return False
    else:
        print('empty list !')

def movesInAllMoves(list1, list2):
    indicator = False
    for i, grid in enumerate(list1):
        for grid2 in list2:
            if compareGrids(grid, grid2):
                indicator = True
                break
        if indicator:
            indicator = False
        else:
            return False

    return True

def finalState(grid):
    if grid.redCar.position[1]+ 1 + grid.spaceAroundVehicule(grid.redCar)[2] == 5:
        return True
    else:
        return False
