COLUMNS = 7
ROWS = 7
RED = 5
BLUE = 2
VERBOSE = True

'''
helper class to be used for coloring the printed output. only needed for dev/testing
'''
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

'''
only class that's needed
goalR, goalB, start need to be updated before compiling 
intended behavior is:
object gets instantiated.
every time the bot scans and doesn't find a wall, call the update method as such update(currX, currY, freeX, freeY)
after scans are done, call the pathFind method, if it returns an empty string stay in random movement. else follow returned path string
if the bot ever finds a block, call addBlock(blockX, blockY, COLOR) where COLOR matches either BLUE or RED
'''
class botLogic:
  def __init__(self) -> None:
    self.goalR = (0,6) 
    self.goalB = (6,0)
    self.start = (1,3)
    self.primes = [[2, 3, 5, 7, 11, 13, 17], [19, 23, 29, 31, 37, 41, 43], [47, 53, 59, 61, 67, 71, 73], [79, 83, 89, 97, 101, 103, 107], [109, 113, 127, 131, 137, 139, 149], [151, 157, 163, 167, 173, 179, 181], [191, 193, 197, 199, 211, 223, 227]]
    self.area = [[self.Tile(j,i, self.primes[i][j]) for j in range(COLUMNS)] for i in range(ROWS)]
    self.area[self.goalR[1]][self.goalR[0]].isGoal = RED
    self.area[self.goalB[1]][self.goalB[0]].isGoal = BLUE
    self.area[self.start[1]][self.start[0]].isCurrent = True
    self.walkableEdges = []
    self.heading = 'N'
    self.blocks = []
    self.toBePropagated = []

  '''
  this method is used to add walkable edges to the list of possible edges.
  preverification of a valid path between (pX, pY) and (fX, fY) existing must be done
  '''
  def update(self, pX, pY, fX, fY):
    if self.area[pY][pX].prime * self.area[fY][fX].prime not in self.walkableEdges:
      self.walkableEdges.append(self.area[pY][pX].prime * self.area[fY][fX].prime)
    
  '''
  intended behavior:
  for every block in the self.blocks list:
    try to find a path between the bot and itself, if that is found then save the path and then:
      find a path between the block and the respective goal.
      return complete path from current bot location, to block location, and from block location to goal location
      if path was successfully found then delete that block's entry 
    if any of the above conditions fail then leave block in queue and test next block
  '''
  def pathFind(self, heading, currX, currY):
    l = len(self.blocks)
    for num in range(l):
      print(num)


  def findPathBetweenPoints(self, fromX, fromY, toX, toY):
    self.resetState()
    self.area[toY][toX].value = 0;
    self.toBePropagated.append((toX,toY))


  def addBlock(self, x, y, color):
    if self.area[y][x] not in self.blocks:
      self.area[y][x].isBlock = color
      self.blocks.append(self.area[y][x])

  '''
  helper method used to set the value of all cells to 1000 to reset the pathfinding algorithm
  '''
  def resetState(self):
    for row in self.area:
      for tile in row:
        tile.value = 1000

  '''
  returns true if there is a known walkable path between (_x,_y) and (x,y)
  returns false otherwise
  '''
  def isWalkablePath(self, _x, _y, x, y):
    return self.area[y][x].prime * self.area[_y][_x].prime in self.walkableEdges

  '''
  helper method to declare the string representation of the whole 7x7 matrix
  does not print anything if the VERBOSE constant is not True
  '''
  def __str__(self) -> str:
    res = ""
    if VERBOSE == True:
      for i in self.area:
        print('\t'.join(map(str, i)))
    return res

  class Tile:
    def __init__(self, x, y, prime) -> None:
      self.x = x
      self.y = y
      self.isGoal = 0
      self.isCurrent = False
      self.isBlock = 0
      self.value = 1000
      self.prime = prime

    def __str__(self):
      return "(" + bcolors.WARNING + str(self.x) + ", " + str(self.y) + " " + str(self.prime) + bcolors.ENDC + ")" if self.isCurrent == True else "(" + bcolors.OKBLUE + str(self.x) + ", " + str(self.y) + " " + str(self.prime) + bcolors.ENDC + ")" if self.isGoal == BLUE else "(" + bcolors.FAIL + str(self.x) + ", " + str(self.y) + " " + str(self.prime) + bcolors.ENDC + ")" if self.isGoal == RED else "(" + str(self.x) + ", " + str(self.y) + " " + str(self.prime) + ")"




def main():
    logic = botLogic()
    print(logic)
    logic.update(0,0,0,1)
    logic.addBlock(0,0, RED)
    logic.addBlock(1,1, BLUE)
    logic.pathFind(0,0,0)
    print(logic.isWalkablePath(0,0,0,1))
    print(logic)
    logic.resetState()

if __name__ == "__main__":
  main()