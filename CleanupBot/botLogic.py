COLUMNS = 7
ROWS = 7
RED = 5
BLUE = 2
VERBOSE = True


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
  
  def __str__(self) -> str:
    res = ""
    if VERBOSE == True:
      for i in self.area:
        print('\t'.join(map(str, i)))
    return res
  
  def isWalkablePath(self, _x, _y, x, y):
    return self.area[y][x].prime * self.area[_y][_x].prime in self.walkableEdges

  def update(self, pX, pY, fX, fY):
    self.walkableEdges.append(self.area[pY][pX].prime * self.area[fY][fX].prime)
    

  def pathFind(self, heading, currX, currY):
    l = len(self.blocks)
    for num in range(l):
      print(num)

  def addBlock(self, x, y):
    self.blocks.append(self.area[y][x])


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
    logic.addBlock(0,0)
    logic.addBlock(0,1)
    logic.pathFind(0,0,0)
    print(logic.isWalkablePath(0,0,0,1))

if __name__ == "__main__":
  main()