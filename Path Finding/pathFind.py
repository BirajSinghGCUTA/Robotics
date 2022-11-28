ROWS = 10
COLUMNS = 16

# constants provided at the time of compilation by the professor
# these constants are the constraints the code uses to generate 
# the path to the goal from the start
obstacles = [
    (0.915, 0.305), (0.915, 0.610), (0.915, 0.915), (0.915, 1.220),
    (1.829, 0.915), (1.829, 1.220), (1.829, 1.525), (1.829, 1.829),
    (1.829, 2.134), (1.829, 2.439), (1.829, 2.743),
    (3.048, 1.220), (3.048, 1.525), (3.048, 1.829),
    (3.353, 0.915), (3.353, 1.220), (3.658, 0.915), (3.658, 1.220)
]

start = [(0.305, 0.610)]
goal = [(3.658, 1.829)]

# Tile is an object which is meant to represent each of the tiles the robot is meant to traverse
# The parameters for a tile are its x and y coordinates in a row major sequence. indexed starting at 0
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walkable = True
        self.value = 1000
        self.isGoal = False

    def setWalkable(self):
        self.walkable = False

    def setGoal(self):
        self.isGoal = True
        self.value = 0

    # returns the string representation of a tile with all pertinent information
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + " " + ("W" if self.walkable else "") + str(self.value) + ("G" if self.isGoal else "") + ")"

# Workspace is the class that manages all the dataflow and logic of the robot
# once a Workspace object is instantiated, the only method that needs to be called is autoPath()
# the autopath method will then return a string representation of all the stets the bot needs to take to get to the goal
# there are no inputs needed to instantiate Workspace
class Workspace:
    # initializes all internal variables to their initial values. as well as generates a 2d array of Tile objects
    def __init__(self):
        self.area = [[Tile(i, j) for j in range(COLUMNS)] for i in range(ROWS)]
        self.heading = ''
        self.resultingPath = ""
        self.toBePropagated = []
        self.chosenStart = [1000, (-1, -1), ""]

    # prints to console a representation of the whole array structure by calling print on each Tile object in the correct sequence
    def printWorld(self):
        for i in self.area:
            print('\t'.join(map(str, i)))

    # this function is originally called with the normalized obstacles array coordinates provided by the professor.
    # this function will transpose the coordinates into their respective places in the 2d array structure
    # Note: no bound checking done at this step for simplicity
    def setObstacles(self, _obstacles):
        for obs in _obstacles:
            self.obstacle(8 - obs[1], obs[0])
            self.obstacle(8 - obs[1], obs[0] + 1)
            self.obstacle(9 - obs[1], obs[0])
            self.obstacle(9 - obs[1], obs[0] + 1)

    # this function is originally called with the normalized goals array coordinates provided by the professor.
    # this function will transpose the coordinates into their respective places in the 2d array structure
    # those same transposed coordinates then get added to the toBePropagated stack so as to be propagated later
    # Note: no bound checking done at this step for simplicity
    def setGoals(self, _goals):
        for goa in _goals:
            self.goa(8 - goa[1], goa[0])
            self.goa(8 - goa[1], goa[0] + 1)
            self.goa(9 - goa[1], goa[0])
            self.goa(9 - goa[1], goa[0] + 1)
        self.toBePropagated.append((8 - goa[1], goa[0]))
        self.toBePropagated.append((8 - goa[1], goa[0] + 1))
        self.toBePropagated.append((9 - goa[1], goa[0]))
        self.toBePropagated.append((9 - goa[1], goa[0] + 1))

    # this is the function that sets the walkable flag as false for the objects. 
    # this function is only needed so bounds checking can be done in a single point
    # inputs: x, y coordinates of the cells to be changed
    def obstacle(self, x, y):
        if y < 0 or y >= COLUMNS or x < 0 or x >= ROWS:
            return
        self.area[x][y].setWalkable()

    # this is the function that sets the goal flag as true for the goal cells in the array
    # this funcion is only needed so bounds checking can be done at a single point
    # inputs: x, y coordinates of the cells to be changed
    def goa(self, x, y):
        if y < 0 or y >= COLUMNS or x < 0 or x >= ROWS:
            return
        self.area[x][y].setGoal()

    # this function returns an array of the values of all connected cells to the one located at (x,y)
    # this is done for the purposes of checking that the cells are correctly valued based on their neighbor's values
    # this is done as a way of optimizing the number of calls needed to the propagation sequence
    def getVecinity(self, x, y):
        res = []
        if y - 1 > 0:
            res.append(self.area[x][y - 1].value)
        if x - 1 > 0:
            res.append(self.area[x - 1][y].value)
        if y + 1 < COLUMNS:
            res.append(self.area[x][y + 1].value)
        if x + 1 < ROWS:
            res.append(self.area[x + 1][y].value)
        return res

    # this function will call the update cell on all neighboring cells to (x,y) if 
    # the values of any of the neighbors is not exacly 1 off of the value of the current cell
    # if even one neighbor is not correct this method will call updateCell on all neighbors
    def propagate(self, x, y):
        if self.area[x][y].walkable == False:
            return

        neighVals = self.getVecinity(x, y)
        currValue = self.area[x][y].value
        if all(v != currValue - 1 or v != currValue + 1 for v in neighVals):
            if y - 1 >= 0:
                self.updateCell(x, y - 1)
            if x - 1 >= 0:
                self.updateCell(x - 1, y)
            if y + 1 < COLUMNS:
                self.updateCell(x, y + 1)
            if x + 1 < ROWS:
                self.updateCell(x + 1, y)

    # this method takes in a x and y pair which it will then test to make sure it's not a goal or an obstacle
    # after that it gets the values of all its neighbors using the getVecinity() method. it then checks its own 
    # value to see if it need to be changed. if it does need to be changed the method will set the value of the 
    # cell at (x,y) to 1 more the minimum of all its neighbors
    def updateCell(self, x, y):
        if self.area[x][y].walkable == False or self.area[x][y].isGoal == True:
            return
        minNeigh = min(self.getVecinity(x, y))
        if minNeigh + 1 < self.area[x][y].value:
            self.area[x][y].value = minNeigh + 1
            self.toBePropagated.append((x, y))

    # this function is originally called with the normalized start array coordinates provided by the professor.
    # this function will transpose the coordinates into their respective places in the 2d array structure.
    # it will then call the verStart method with those new coordinates in order to set an initial start cell.
    # a custom final path start is chosen based on the direction that the bot will need to move to to position itself at that coordinate
    # the chosen initial string then gets added to the resulting path
    # Note: no bound checking done at this step for simplicity as all cells are assumed to be accessible
    def findStart(self, _start):
        for str in _start:
            self.verStart(8 - str[1], str[0], "fLf")
            self.verStart(8 - str[1], str[0] + 1, "fRf")
            self.verStart(9 - str[1], str[0], "LfLf")
            self.verStart(9 - str[1], str[0] + 1, "RfRf")
        self.resultingPath += self.chosenStart[2]

    # bounds checking is done at this step to make sure that the cell at (x,y) is a valid cell
    # this function is used to determine the optimal initial offset from starting location to 
    # the middle of the tile closest to the goal. using a class wide variable to hold the currrrent minimum
    def verStart(self, x, y, str):
        if y < 0 or y >= COLUMNS or x < 0 or x >= ROWS:
            return
        curr = self.area[x][y]
        if curr.walkable:
            if curr.value < self.chosenStart[0]:
                self.chosenStart[0] = curr.value
                self.chosenStart[1] = (curr.x, curr.y)
                self.chosenStart[2] = str
                self.heading = 'E' if str == "fRf" else 'W' if str == "fLf" else 'S'

    # this recursive function is called to generate the final path once the 2d array has been 
    # populated with the needed proximity values. it looks at the neighbors of the cell at (x.y)
    # and uses the current heading and the value of the current neighbors to determine how the bot should move
    # it also calls the center() method once it finds itself at the goal so as to center itself in the goal.
    # since movement sequences are influenced by both rotation and transaltions this function takes into accaount both
    def findClosest(self, x, y):
        curr = self.area[x][y]
        if curr.value == 0:
            self.center(x, y)
        if self.heading == 'N':
            if self.getCellValue(x - 1, y) < curr.value:
                self.resultingPath += "F"
                self.findClosest(x-1, y)
                return
            if self.getCellValue(x, y - 1) < curr.value:
                self.resultingPath += "LF"
                self.heading = 'W'
                self.findClosest(x, y - 1)
                return
            if self.getCellValue(x, y + 1) < curr.value:
                self.resultingPath += "RF"
                self.heading = 'E'
                self.findClosest(x, y + 1)
                return
            if self.getCellValue(x + 1, y) < curr.value:
                self.resultingPath += "LLF"
                self.heading = 'S'
                self.findClosest(x + 1, y)
                return

        if self.heading == 'E':
            if self.getCellValue(x, y + 1) < curr.value:
                self.resultingPath += "F"
                self.findClosest(x, y + 1)
                return
            if self.getCellValue(x + 1, y) < curr.value:
                self.resultingPath += "RF"
                self.heading = 'S'
                self.findClosest(x + 1, y)
                return
            if self.getCellValue(x - 1, y) < curr.value:
                self.resultingPath += "LF"
                self.heading = 'N'
                self.findClosest(x - 1, y)
                return
            if self.getCellValue(x, y - 1) < curr.value:
                self.resultingPath += "LLF"
                self.heading = 'W'
                self.findClosest(x, y - 1)
                return

        if self.heading == 'S':
            if self.getCellValue(x + 1, y) < curr.value:
                self.resultingPath += "F"
                self.findClosest(x + 1, y)
                return
            if self.getCellValue(x, y + 1) < curr.value:
                self.resultingPath += "LF"
                self.heading = 'E'
                self.findClosest(x, y + 1)
                return
            if self.getCellValue(x, y - 1) < curr.value:
                self.resultingPath += "RF"
                self.heading = 'W'
                self.findClosest(x, y - 1)
                return
            if self.getCellValue(x - 1, y) < curr.value:
                self.resultingPath += "LLF"
                self.heading = 'N'
                self.findClosest(x - 1, y)
                return

        if self.heading == 'W':
            if self.getCellValue(x, y - 1) < curr.value:
                self.resultingPath += "F"
                self.findClosest(x, y - 1)
                return
            if self.getCellValue(x - 1, y) < curr.value:
                self.resultingPath += "RF"
                self.heading = 'N'
                self.findClosest(x - 1, y)
                return
            if self.getCellValue(x + 1, y) < curr.value:
                self.resultingPath += "LF"
                self.heading = 'S'
                self.findClosest(x + 1, y)
                return
            if self.getCellValue(x, y + 1) < curr.value:
                self.resultingPath += "LLF"
                self.heading = 'E'
                self.findClosest(x, y + 1)
                return

    # this function is meant to be called when the bot has already arrived into a cell that 
    # is a goal. at that point the function takes into account the current heanding and the value of 
    # one of its neighbors to get the correct last steps to center itself in the goal
    def center(self, x, y):
        curr = self.area[x][y]
        self.resultingPath += "f"
        if self.heading == 'N':
            if self.getCellValue(x, y - 1) == 0:
                self.resultingPath += "Lf"
                return
            else:
                self.resultingPath += "Rf"
                return
        if self.heading == 'E':
            if self.getCellValue(x - 1, y) == 0:
                self.resultingPath += "Lf"
                return
            else:
                self.resultingPath += "Rf"
                return
        if self.heading == 'S':
            if self.getCellValue(x, y - 1) == 0:
                self.resultingPath += "Rf"
                return
            else:
                self.resultingPath += "Lf"
                return
        if self.heading == 'W':
            if self.getCellValue(x - 1, y) == 0:
                self.resultingPath += "Rf"
                return
            else:
                self.resultingPath += "Lf"
                return

    # bound checks and then returns the value of the cell at (x.y)
    def getCellValue(self, x, y):
        if y < 0 or y >= COLUMNS or x < 0 or x >= ROWS:
            return 1000
        return self.area[x][y].value

    # function intended for the automatic execution of the pathfinding algorithm
    # makes use of all the other methods and executes them in the correct order.
    # it returns the complete path string where:
    # F = 1 tile length forward translation
    # f = half the length of a tile forward translation
    # R = 90 degrees rotation in place to the right
    # L = 90 degrees rotation in place to the left
    def autoPath(self):
        self.resultingPath = ""
        self.chosenStart = [1000, (-1, -1), ""]
        _obstacles = self.normalize(obstacles)
        _goal = self.normalize(goal)
        _start = self.normalize(start)
        self.setObstacles(_obstacles)
        self.setGoals(_goal)
        while (len(self.toBePropagated) > 0):
            curr = self.toBePropagated.pop()
            self.propagate(curr[0], curr[1])
        self.findStart(_start)
        self.findClosest(self.chosenStart[1][0], self.chosenStart[1][1])
        return self.resultingPath

    def normalize(self, input):
        res = []
        for dups in input:
            if dups[0] >= 0 and dups[1] >= 0:
                res.append([round(dups[0]/0.305)-1, round(dups[1]/0.305)-1])
        return res

#main method used for standalone testing and development
def main():
    world = Workspace()
    print(world.autoPath())


if __name__ == "__main__":
    main()
