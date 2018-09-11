# -*- encoding: utf-8 -*-
""" The full version of the 2048 game """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_sjIvkLBYSh_2.py

import poc_2048_gui
import random


# Directions, *DO NOT MODIFY - these go together with the dictionary below. We use names such as 'UP' and 'DOWN' but in fact we are using: 1,2,3 and 4
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction, *DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0), DOWN: (-1, 0), LEFT: (0, 1), RIGHT: (0, -1)}


def merge(line):
    """ Helper function that merges a single row or column in 2048 """
    merged_list = list(line)  # create a copy of the list that is going to be modified

    for zero_num in line:  # move all zero's to the end of the list
        if zero_num == 0:
            merged_list.append(0)  # we need to keep the same amount of 'append' and 'remove' so the total amount of elements remain the same
            merged_list.remove(0)

    for number in range(len(merged_list) - 1):  # merge numbers in merged_list
        if merged_list[number] != 0:
            if merged_list[number] == merged_list[number + 1]:
                merged_list[number] *= 2
                merged_list.pop(number + 1)
                merged_list.append(0)

    return merged_list


class TwentyFortyEight:
    """ Class to run the game logic. """
    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        # this is the adaptive list of initial values for scanning the whole matrix:
        self._directions = {UP: [[0, i] for i in range(self._grid_width)],  # UP: [[0, 0], [0, 1], [0, 2], [0, 3]]
                            DOWN: [[(self._grid_height - 1), i] for i in range(self._grid_width)],  # DOWN: [[3, 0], [3, 1], [3, 2], [3, 3]]
                            LEFT: [[i, 0] for i in range(self._grid_height)],  # LEFT: [[0, 0], [1, 0], [2, 0], [3, 0]]
                            RIGHT: [[i, (self._grid_width - 1)] for i in range(self._grid_height)]}  # RIGHT: [[0, 3], [1, 3], [2, 3], [3, 3]]
        self.reset()

    def reset(self):
        """ Reset the game so the grid is empty except for two initial tiles. """
        self._grid = [[0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]  # Inner comprehension is commenced first and creates a single row of a matrix at a time
        for dummy_tile in range(2):  # we call this method twice as each time we reset the game with an empty board and two new tiles
            self.new_tile()

    def __str__(self):
        """ Return a string representation of the grid for debugging. """
        grid_plot = ""
        for row in list(self._grid):
            grid_plot += str(row) + "\n"
        return grid_plot

    def get_grid_height(self):
        """ Get the height of the board. """
        return self._grid_height

    def get_grid_width(self):
        """ Get the width of the board. """
        return self._grid_width

    def move(self, direction):  # the 'direction' variable comes as 1, 2, 3, 4 as per 'Directions'
        """ Move all tiles in the given direction and add a new tile if any tiles moved. """
        range_along = len(self._directions[direction])
        range_across = self._grid_height if self._grid_height != range_along else self._grid_width  # this is to get the other dimension, since there are oonly two, we can get the other one
        tiles_moved = False  # this is for determining if anything changed within all lists in a given direction, we put it here because we have to check this condition each time we call 'move'

        for element in range(range_along):  # the main loop scans through the entire matrinx in the ALONG DIRECTION
            start_cell = self._directions[direction][element]
            temp_list = []
            for step in range(range_across):  # this loop goes across and picks up a value to a list
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                temp_list.append(self._grid[row][col])

            merged_list = merge(temp_list)  # then we run the 'merge' procedure on that list

            for step in range(range_across): # here we put the merged items into the matrix again
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                self.set_tile(row, col, merged_list[step])
                if temp_list != merged_list:  # this is where we check if any of the lists changed
                    tiles_moved = True

        if tiles_moved:  # if any of the lists changed, then we add a new tile
            self.new_tile()

    def new_tile(self):
        """ Create a new tile in a randomly selected empty square. The tile should be 2 90% of the time and 4 10% of the time. """
        tile_choice = random.choice([2] * 9 + [4])  # same as : random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
        while True:
            row = random.randrange(0, self._grid_height)
            col = random.randrange(0, self._grid_width)
            if self.get_tile(row, col) == 0:
                break
        self.set_tile(row, col, tile_choice)

    def set_tile(self, row, col, value):
        """ Set the tile at position row, col to have the given value. """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """ Return the value of the tile at position row, col. """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
