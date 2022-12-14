from main import * 
from botLogic import *
import random 

'''
|---|---|---|---|---|---|
|---|---|---|---|---|---|
|---|---|---|---|---|---|
|---|---|---|---|---|---|

'''


class Localization:
    def __init__(self, starting_pos, starting_orientation) -> None:
        self.current_coordinate = starting_pos
        self.current_orientation = starting_orientation
        self.tank_controls = TankControls()
        self.traveled_coordinates = set()

    def count_tiles(self, distance):
        if(distance >= 2550 or distance <= 250):
            return 0
        elif (distance > 250 and distance < 305):
            return 1
        else: 
            return int(distance / 305)

    def get_forward_coordinate(self, coordinate, orientation):
        #get forward coordinate w/r to oreinctation
        if orientation == 'N':
            return (coordinate[0], coordinate[1]-1)
        elif orientation == 'W':
            return (coordinate[0]-1, coordinate[1])
        elif orientation == 'E':
            return (coordinate[0]+1, coordinate[1])
        elif orientation == 'S':
            return (coordinate[0], coordinate[1]+1)
        
    def get_left_coordinate(self, coordinate, orientation):
        #get forward coordinate w/r to oreinctation
        if orientation == 'N':
            return(coordinate[0]-1, coordinate[1])
        elif orientation == 'W':
            return(coordinate[0], coordinate[1]+1)
        elif orientation == 'E':
            return(coordinate[0], coordinate[1]-1)
        elif orientation == 'S':
            return(coordinate[0]+1, coordinate[1])
     
    def get_right_coordinate(self, coordinate, orientation):
        #get forward coordinate w/r to oreinctation
        if orientation == 'N':
            return (coordinate[0]+1, coordinate[1])
        elif orientation == 'W':
            return (coordinate[0], coordinate[1]-1)
        elif orientation == 'E':
            return (coordinate[0], coordinate[1]+1)
        elif orientation == 'S':
            return (coordinate[0]-1, coordinate[1])
    '''
    ChatGPT's analysis:
    The method first calculates the forward, left, and right coordinates relative to the 
    current coordinate, using the get_forward_coordinate() and get_right_coordinate() methods.
    Next, the method defines an empty list called directions that will be used to store the 
    valid directions that the object can move in. The code then checks if the path in the forward 
    direction is walkable (using the isWalkablePath() method), and if the forward coordinate has not 
    already been visited (using the traveled_coordinates attribute). If both of these conditions are true, 
    the code appends the string 'F' to the directions list.
    The code then repeats this process for the left and right directions, appending 'LF' and 'RF' 
    to the directions list if the corresponding paths are walkable and have not been visited.
    Finally, if the directions list is not empty, the code uses the random.choice() function to choose a 
    random direction from the list. If the list is empty, the code chooses a random direction from the list ('LF', 'RF', 'F') 
    using the random.choice() function. The chosen direction is then returned by the getNextDirection() method. 
    '''
    def get_next_direction(self):

        bot_left = self.tank_controls.scan_left()
        bot_forward = self.tank_controls.scan_forward()
        bot_right = self.tank_controls.scan_right()
        
        self.tank_controls.returnToPosition()
        
        print(bot_left)
        print(bot_forward)
        print(bot_right)

        forward_tile_count = self.count_tiles(bot_forward)
        left_tile_count = self.count_tiles(bot_left)
        right_tile_count = self.count_tiles(bot_right)


        forward_coordinate = self.get_forward_coordinate(self.current_coordinate, self.current_orientation)
        left_coordinate = self.get_left_coordinate(self.current_coordinate, self.current_orientation)
        right_coordinate = self.get_right_coordinate(self.current_coordinate, self.current_orientation)

        directions = []
        if forward_coordinate not in self.traveled_coordinates and forward_tile_count > 0:
            directions.append('F')

        if left_coordinate not in self.traveled_coordinates and left_tile_count > 0:
           directions.append('LF')

        if right_coordinate not in self.traveled_coordinates and right_tile_count > 0:
            directions.append('RF')
        

        if directions:
            direction = random.choice(directions)
        else:
            if forward_tile_count > 0:
                directions.append('F')

            if left_tile_count > 0:
                directions.append('LF')

            if right_tile_count > 0:
                directions.append('RF')

            if directions:
                direction = random.choice(directions)
            else:
                direction = random.choice(('RRRR', 'LLLL'))

        print(direction)
        return direction

    def get_direction_orientation_coordinate(self, direction):

        temp_coordinate = self.current_coordinate
        orientations = ['N', 'E', 'S', 'W']
        command_to_rotation = {
            'R': 1,
            'L': -1,
        }
        # find the initial index of the orientation in the list of orientations
        initial_index = orientations.index(self.current_orientation)
    
        # iterate over the commands and apply the corresponding rotation
        for command in direction:
            # skip 'F' commands
            if command == 'F':
                temp_coordinate = self.get_forward_coordinate(temp_coordinate, orientations[initial_index])
            else:
                #apply the rotation, using the modulo operator to wrap around the end of the list
                initial_index = (initial_index + command_to_rotation[command]) % len(orientations)
    
        # return the final orientation and coordinate
        return (temp_coordinate, orientations[initial_index])


    #takes in the current coordinate, scans for all the possible moves, adds the coordinate to 
    #the pathFinder class and returns a cordinate to move into next at random
    def localize_coordinate(self):
        bot_left = self.tank_controls.scan_left()
        bot_forward = self.tank_controls.scan_forward()
        bot_right = self.tank_controls.scan_right()
        
        self.tank_controls.returnToPosition()
        
        print(bot_left)
        print(bot_forward)
        print(bot_right)

        forward_tile_count = self.count_tiles(bot_forward)
        left_tile_count = self.count_tiles(bot_left)
        right_tile_count = self.count_tiles(bot_right)
    
        print(forward_tile_count)
        print(left_tile_count)
        print(right_tile_count)

        temp_coordinate = self.current_coordinate
        while(forward_tile_count > 0):
            forward_coordinate = self.get_forward_coordinate( temp_coordinate, self.current_orientation)
            temp_coordinate = forward_coordinate
            forward_tile_count = forward_tile_count - 1
        
        temp_coordinate = self.current_coordinate
        while(left_tile_count > 0):
            forward_coordinate = self.get_left_coordinate( temp_coordinate, self.current_orientation)
            if not self.pathFinder.update(temp_coordinate[0], temp_coordinate[1], forward_coordinate[0], forward_coordinate[1]):
                break
            temp_coordinate = forward_coordinate
            left_tile_count = left_tile_count - 1
        
        temp_coordinate = self.current_coordinate
        while(right_tile_count > 0):
            right_coordinate = self.get_right_coordinate(temp_coordinate, self.current_orientation)
            if not self.pathFinder.update(temp_coordinate[0], temp_coordinate[1], right_coordinate[0], right_coordinate[1]):
                break
            temp_coordinate = right_coordinate
            right_tile_count = right_tile_count - 1

    def explore(self):
        while True:
            if self.current_coordinate not in self.traveled_coordinates:
                self.traveled_coordinates.add(self.current_coordinate)

            Direction_command = self.get_next_direction()
            Direction_command = self.tank_controls.execute_commands(Direction_command)
            self.current_coordinate, self.current_orientation = self.get_direction_orientation_coordinate(Direction_command)
            
            if self.tank_controls.sense_color("red") or self.tank_controls.sense_color("blue") or self.tank_controls.sense_color("green") :
                break
            
            
    def printCurrentCoordinate(self):
        print(self.current_coordinate)

    
    

    
    