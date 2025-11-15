from RandomGenerator import *
from AI_Solvers import *
from logicToDisplay import solvePuzzle

root = gridRandomGenerator()
root.updateGrid()
moves = BFSsolver(root)
solvePuzzle(moves)