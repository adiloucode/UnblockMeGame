import copy
import time
import pygame as pg


def gridToMatrixDrawer(grid):
    #       0 1 2 3 4 5
    mat = [[0,0,0,0,0,0], #0
           [0,0,0,0,0,0], #1
           [0,0,0,0,0,0], #2
           [0,0,0,0,0,0], #3
           [0,0,0,0,0,0], #4
           [0,0,0,0,0,0]] #5

    for pixel in grid.redCar.getVehiculeSpace():
        mat[pixel[0]][pixel[1]] = 'x'

    for i, vhc in enumerate(grid.obstacles):
        for pixel in vhc.getVehiculeSpace():
            if mat[pixel[0]][pixel[1]] != 0:
                print(f"Conflict spotted at: ({pixel[0]},{pixel[1]})")
            mat[pixel[0]][pixel[1]] = i+1
    return mat

class Vehicule:
    def __init__(self, position, orientation,length):
        self.position = position
        self.orientation = orientation
        self.length = length


    def displayVehiculeInfo(self):
        print(f"Vehicule stats: \nPosition: {self.position}\nOrientation: {self.orientation}\nLength {self.length}")

    def getVehiculeSpace(self):
        occupiedPixels = []
        if self.orientation == 'horizontal':
            for i in range(0, self.length):
                occupiedPixels.append((self.position[0], self.position[1]+i))
        else:
            for i in range(0, self.length):
                occupiedPixels.append((self.position[0]+i, self.position[1]))   
        return occupiedPixels

    def moveVehiculeByCoords(self, move):
        self.position[0] += move[0]
        self.position[1] += move[1]

    def moveVehicule(self, direction, step):
        if self.orientation == 'vertical':
            if direction.lower() == 'up':
                x = self.position[0] - step
                if x >= 0:
                    newPosition = (x, self.position[1])
                    self.position = newPosition
                else:
                    print('Position out of bound')

            elif direction.lower() == 'down':
                x = self.position[0] + step
                if x + self.length - 1 <= 5:
                    newPosition = (x, self.position[1])
                    self.position = newPosition
                else:
                    print('Position out of bound')

        elif self.orientation == 'horizontal':

            if direction.lower() == 'left':
                    y = self.position[1] - step
                    if y >= 0:
                        newPosition = (self.position[0], y)
                        self.position = newPosition
                    else:
                        print('Position out of bound') 

            elif direction.lower() == 'right':
                y = self.position[1] + step
                if y + self.length - 1 <= 5:
                    newPosition = (self.position[0], y)
                    self.position = newPosition
                else:
                    print('Position out of bound')

        else:
            print('Vehicule has broken Orientation !')

class Grid:
    def __init__(self, redCar, obstacles):
        self.redCar = redCar
        self.obstacles = obstacles
        self.matrix = gridToMatrixDrawer(self)
        self.parent = None
        self.objectiveValue = None

    def setParent(self, parent):
        self.parent = parent

    def gridToMatrixDrawer(self):
        #       0 1 2 3 4 5
        mat = [[0,0,0,0,0,0], #0
               [0,0,0,0,0,0], #1
               [0,0,0,0,0,0], #2
               [0,0,0,0,0,0], #3
               [0,0,0,0,0,0], #4
               [0,0,0,0,0,0]] #5

        for pixel in self.redCar.getVehiculeSpace():
            mat[pixel[0]][pixel[1]] = 'x'

        for i, vhc in enumerate(self.obstacles):
            for pixel in vhc.getVehiculeSpace():
                if mat[pixel[0]][pixel[1]] != 0:
                    print(f"Conflict spotted at: ({pixel[0]},{pixel[1]})")
                mat[pixel[0]][pixel[1]] = i+1
        self.matrix = mat

    def displayGridInfo(self):
        print(f"Grid Stats: \n")
        print('================================')
        self.redCar.displayVehiculeInfo()
        print(f'Red Car: \n')
        print('================================')
        print(f'Obstacles: {len(self.obstacles)}\n')
        for vhc in self.obstacles:
            vhc.displayVehiculeInfo()
        print('================================')
        print(f'Matrix: \n')
        print(self.matrix)

    def showMatrix(self):
        print(self.matrix)

    def spaceAroundVehicule(self, vhc):
        occupiedPixels = vhc.getVehiculeSpace()
        start = occupiedPixels[0]
        end = occupiedPixels[len(occupiedPixels)-1]
        if vhc.orientation == 'horizontal':
            i = start[0]
            j = start[1] - 1
            left = 0
            right = 0
            while j >= 0 and self.matrix[i][j] == 0 :
                left +=1
                j -= 1
            i = end[0]
            j = end[1] + 1
            while j <= 5 and self.matrix[i][j] == 0:
                right +=1
                j += 1
            return vhc.orientation ,left, right
        elif vhc.orientation == 'vertical':
            i = start[0] - 1
            j = start[1] 
            up = 0
            down = 0
            while i >= 0 and self.matrix[i][j] == 0 :
                up +=1
                i -= 1
            i = end[0] + 1
            j = end[1] 
            while i <= 5 and self.matrix[i][j] == 0 :
                down +=1
                i += 1
            return vhc.orientation ,up, down

        else:
            print('Vehicule has Broken orientation')
            return None

    def makeChildsFromVehicule(self, vhc, idx = None):
        children = []
        orientation, before, after = self.spaceAroundVehicule(vhc)
        if orientation == 'horizontal':
            for i in range(before):
                vhc2 = Vehicule(vhc.position, vhc.orientation, vhc.length)
                vhc2.moveVehicule('left', i+1)
                if idx == None:
                    children.append(Grid(vhc2, self.obstacles))
                else:
                    obstacles2 = copy.deepcopy(self.obstacles)
                    obstacles2[idx] = vhc2
                    children.append(Grid(self.redCar,obstacles2))
                vhc2 = None

            for i in range(after):
                vhc2 = Vehicule(vhc.position, vhc.orientation, vhc.length)
                vhc2.moveVehicule('right', i+1)
                if idx == None:
                    children.append(Grid(vhc2, self.obstacles))
                else:
                    obstacles2 = copy.deepcopy(self.obstacles)
                    obstacles2[idx] = vhc2
                    children.append(Grid(self.redCar,obstacles2))
                vhc2 = None
        elif orientation == 'vertical':
            for i in range(before):
                vhc2 = Vehicule(vhc.position, vhc.orientation, vhc.length)
                vhc2.moveVehicule('up', i+1)
                if idx == None:
                    children.append(Grid(vhc2, self.obstacles))
                else:
                    obstacles2 = copy.deepcopy(self.obstacles)
                    obstacles2[idx] = vhc2
                    children.append(Grid(self.redCar,obstacles2))
                vhc2 = None
            for i in range(after):
                vhc2 = Vehicule(vhc.position, vhc.orientation, vhc.length)
                vhc2.moveVehicule('down', i+1)
                if idx == None:
                    children.append(Grid(vhc2, self.obstacles))
                else:
                    obstacles2 = copy.deepcopy(self.obstacles)
                    obstacles2[idx] = vhc2
                    children.append(Grid(self.redCar,obstacles2))
                vhc2 = None
        return children   

    def allPossibleMoves(self):
        redCarMoves = self.makeChildsFromVehicule(self.redCar)
        obstaclesMoves = []
        for i, vhc in enumerate(self.obstacles):
            obstaclesMoves.extend(self.makeChildsFromVehicule(vhc, idx = i))
        return redCarMoves + obstaclesMoves