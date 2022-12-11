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
    self.area = [[self.Tile(j,i) for j in range(COLUMNS)] for i in range(ROWS)]
    self.area[self.goalR[1]][self.goalR[0]].isGoal = RED
    self.area[self.goalB[1]][self.goalB[0]].isGoal = BLUE
    self.area[self.start[1]][self.start[0]].isCurrent = True
  
  def __str__(self) -> str:
    res = ""
    if VERBOSE == True:
      for i in self.area:
        print('\t'.join(map(str, i)))
    return res
    



  class Tile:
    def __init__(self, x, y) -> None:
      self.x = x
      self.y = y
      self.isGoal = 0
      self.isCurrent = False
      self.value = 1000

    def __str__(self):
      return "(" + bcolors.WARNING + str(self.x) + ", " + str(self.y) + bcolors.ENDC + ")" if self.isCurrent == True else "(" + bcolors.OKBLUE + str(self.x) + ", " + str(self.y) + bcolors.ENDC + ")" if self.isGoal == BLUE else "(" + bcolors.FAIL + str(self.x) + ", " + str(self.y) + bcolors.ENDC + ")" if self.isGoal == RED else "(" + str(self.x) + ", " + str(self.y) + ")"


def main():
    logic = botLogic()
    print(logic)
    while True:
      _botInput = input("user input:")
      if _botInput == "quit":
        break

if __name__ == "__main__":
  main()