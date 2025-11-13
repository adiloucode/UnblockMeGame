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
    
    def vehiculeToRect(self, board, margin = 5):
        print(f'board: {board} / board.x = {board.x} / board.y = {board.y}')
        if self.orientation == 'horizontal':
            rect = pg.Rect(board.x + self.position[1]*100 + (self.position[1] + 1)*margin, board.y + self.position[0]*100 + (self.position[0] + 1)*margin, self.length*100,100)
        elif self.orientation == 'vertical':
            rect = pg.Rect(board.x + self.position[1]*100 + (self.position[1] + 1)*margin, board.y + self.position[0]*100 + (self.position[0] + 1)*margin, 100, self.length*100)
        else:
            print(f'Vehicule has broken orientation')
        print('vehiculeToRect executed !')
        return rect

    def moveVehiculeByMove(self, move):
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
    def __init__(self, redCar, obstacles, margin = 5):
        self.redCar = redCar
        self.obstacles = obstacles
        self.matrix = gridToMatrixDrawer(self)
        self.parent = None
        self.objectiveValue = None
        self.rectRedCar = None
        self.rectObstacles = []
        # Board rectangle
        self.margin = margin
        self.board = pg.Rect(100,100, 600 + 7*margin, 600 + 7*margin)

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
        
    def allowedVehiculeMove(self, vhc, direction, step):
        max_steps = self.spaceAroundVehicule(vhc)
        if direction == 'up' or  direction == 'left':
            if step <= max_steps[1]:
                return True
            else:
                print('conflictual Move ...')
                return False
        elif direction == 'down' or  direction == 'right':
            if step <= max_steps[2]:
                return True
            else:
                print('conflictual Move ...')
                return False
    
    def moveMyVehicule(self, selected, direction, step=1):

        if selected == 'redCar':
            if self.allowedVehiculeMove(self.redCar, direction, step):
                self.redCar.moveVehicule(direction, step)
                self.rectRedCar = self.redCar.vehiculeToRect(self.board, self.margin)
        else:
            if self.allowedVehiculeMove(self.obstacles[selected], direction, step):
                self.obstacles[selected].moveVehicule(direction, step)
                self.rectObstacles[selected] = self.obstacles[selected].vehiculeToRect(self.board, self.margin)
        self.gridToMatrixDrawer()

    
    def gridToRects(self, board= None, margin = 5):
        if not board:
            board = self.board
        self.rectRedCar = self.redCar.vehiculeToRect(board, margin)
        for obstacle in self.obstacles:
            rectObstacle = obstacle.vehiculeToRect(board, margin)
            self.rectObstacles.append(rectObstacle)
        if len(self.rectObstacles) == len (self.obstacles):
            print('Dimensions are matching !')
        else:
            print('Dimensions error !')
    
    def updateGrid(self):
        self.gridToMatrixDrawer()
        self.gridToRects()     
    
    def selectVehicule(self, pos):
        selected = 'redCar'
        if self.rectRedCar.collidepoint(pos):
                selected = 'redCar'
        else:
            for i, obstacle in enumerate(self.rectObstacles):
                if obstacle.collidepoint(pos):
                    selected = i
                    break
        return selected
    
    def drawGridBoard(self, screen, colors, selected):
        screen.fill(colors['BG'])
    
        # Main Board
        pg.draw.rect(screen, colors['BOARD_COLOR'], self.board, border_radius = 10)

        # Red car
        pg.draw.rect(screen, colors['RED'], self.rectRedCar, border_radius = 10)

        # Obstacles
        if selected == 'redCar':
            for rect in self.rectObstacles:
                pg.draw.rect(screen, colors['BLOCK_COLOR'], rect, border_radius = 10)
        else:
            for i, rect in enumerate(self.rectObstacles):
                if i == selected:
                    pg.draw.rect(screen, colors['GREEN'], rect, border_radius = 10)
                else:
                    pg.draw.rect(screen, colors['BLOCK_COLOR'], rect, border_radius = 10)
        pg.display.flip()
    

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