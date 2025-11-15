
import random
from classes import *

def defineNumberOfObstacles(difficulty = 'hard'):
    if difficulty == 'easy':
        nbrObs = random.randint(3, 5)
    elif difficulty == 'medium':
        nbrObs = random.randint(5, 8)
    elif difficulty == 'hard':
        nbrObs = random.randint(8, 9)
    else:
        print("Unknown difficulty !")
        nbrObs = None
    return nbrObs

def generateVehicule():
    length = random.randint(2,3)
    bin = random.randint(0,1)
    if bin == 0:
        orientation = 'horizontal'
    else:
        orientation = 'vertical'

    if bin == 0:
        x = random.randint(0,5)
        while x == 2:
            x = random.randint(0,5)
        position = ( x, random.randint(0, 5-length)) 
    else:
        position = (random.randint(0,5-length), random.randint(0,5))

    return Vehicule(orientation = orientation, position = position, length =length)    

def gridRandomGenerator(screen, difficulty = 'hard', nbrObs = None):
    if not nbrObs:
        nbrObs = defineNumberOfObstacles(difficulty)
    filledSpace = []
    obstacles = []

    redCar = Vehicule((2,0), 'horizontal', 2)
    x = [pixel for pixel in redCar.getVehiculeSpace()]
    for pixel in x:
        filledSpace.append(pixel)

    print(f'will generate {nbrObs} obstacle')
    for _ in range(nbrObs):
        vhc = generateVehicule()
        y = [pixel for pixel in vhc.getVehiculeSpace()]
        if any(pixel in filledSpace for pixel in y):
            del vhc
        else:
            obstacles.append(vhc)
            for pixel in y:
                filledSpace.append(pixel)
    print(f'generated {nbrObs} obstacle')
    return Grid(redCar, obstacles, screen)