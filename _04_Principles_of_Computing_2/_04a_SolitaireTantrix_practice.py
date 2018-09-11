# -*- encoding: utf-8 -*-
"""
Student facing code for Tantrix Solitaire: http://www.jaapsch.net/puzzles/tantrix.htm
Game is played on a grid of hexagonal tiles. All ten tiles for Tantrix Solitaire and place in a corner of the grid. Click on a tile to rotate it.  Click and drag to move a tile.
Goal is to position the 10 provided tiles to form a yellow, red or  blue loop of length 10

Core modeling idea - a triangular grid of hexagonal tiles are model by integer tuples of the form (i, j, k) where i + j + k == size and i, j, k >= 0.
Each hexagon has a neighbor in one of six directions. These directions are modeled by the differences between the tuples of these adjacent tiles
"""
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_W7YorbP0sG_2.py


# run GUI for Tantrix
import poc_tantrix_gui

# Numbered directions for hexagonal grid, ordered clockwise at 60 degree intervals
DIRECTIONS = {0: (-1, 0, 1), 1: (-1, 1, 0), 2: (0, 1, -1), 3: (1, 0, -1), 4: (1, -1, 0), 5: (0, -1, 1)}  # these are coded from the lower - left side and go clockwise

# Color codes for ten tiles in Tantrix Solitaire: "B" denotes "Blue", "R" denotes "Red", "Y" denotes "Yellow"
SOLITAIRE_CODES = ["BBRRYY", "BBRYYR", "BBYRRY", "BRYBYR", "RBYRYB", "YBRYRB", "BBRYRY", "BBYRYR", "YYBRBR", "YYRBRB"]  # these are compatible with DIRECTIONS, ex: for "BRYBYR" straight down is "R"

# Minimal size of grid to allow placement of 10 tiles
MINIMAL_GRID_SIZE = 4


def reverse_direction(direction):
    """ Helper function that returns opposite direction on hexagonal grid """
    num_directions = len(DIRECTIONS)  # we pick the amount of edges we have, as we are going to find the opposite side
    return (direction + num_directions / 2) % num_directions  # this will add half to the current direction and make sure we don't go beyond the edge count


class Tantrix:
    """ Basic Tantrix game class """
    def __init__(self, size):
        """ Create a triangular grid of hexagons with size + 1 tiles on each side. """
        assert size >= MINIMAL_GRID_SIZE  # the size can not be smaller than the MIN_SIZE for ten starting tiles
        self._tiling_size = size

        # Initialize dictionary tile_value to contain codes for ten tiles in Solitaire Tantrix in one 4x4 corner of grid
        self._tile_value = {}
        counter = 0  # this is for iterating over the 'SOLITAIRE_CODES' dictionary

        # placement of 10 elements in the left side of the grid - we start with (0,0,6) and we move left-down to (0,3,3), then on level up to (1,0,5) and left again until we reach (3,0,3):
        for index_i in range(MINIMAL_GRID_SIZE):  # in 1st dimension we take 4 elements once
            for index_j in range(MINIMAL_GRID_SIZE - index_i):  # in the 2nd dimension we start with 4 elements but we end with one, so this is dependent on the first index
                index_k = self._tiling_size - (index_i + index_j)  # in 3rd dimension there is only one element for every second dimension, so it is dependent on both first and second index
                grid_index = (index_i, index_j, index_k)
                self.place_tile(grid_index, SOLITAIRE_CODES[counter])
                counter += 1

    def __str__(self):
        """ Return string of dictionary of tile positions and values """
        return str(self._tile_value)

    def get_tiling_size(self):
        """ Return size of board for GUI """
        return self._tiling_size

    def tile_exists(self, index):
        """ Return whether a tile with given index exists """
        return self._tile_value.has_key(index)

    def place_tile(self, index, code):
        """ Place a tile with code at cell with given index """
        self._tile_value[index] = code

    def remove_tile(self, index):
        """ Remove a tile at cell with given index and return the code value for that tile """
        return self._tile_value.pop(index)

    def rotate_tile(self, index):
        """ Rotate a tile clockwise at cell with given index """
        value = self._tile_value[index]
        new_value = value[-1] + value[:-1]  # this will change the order of codes for a given tile: BBRRYY to YBBRRY, which effecively willrotate the tile clockwise
        self._tile_value[index] = new_value

    def get_code(self, index):
        """ Return the code of the tile at cell with given index """
        return self._tile_value[index]

    def get_neighbor(self, index, direction):
        """ Return the index of the tile neighboring the tile with given index in given direction """
        offset = DIRECTIONS[direction]
        neighbour_index = tuple([index[dim] + offset[dim] for dim in range(3)])
        return neighbour_index

    def is_legal(self):
        """ Check whether a tile configuration obeys color matching rules for adjacent tiles """
        for tile_index in self._tile_value.keys():  # for each tile
            tile_code = self._tile_value[tile_index]
            for direction in DIRECTIONS.keys():  # we check each direction for existing tiles
                neighbour_index = self.get_neighbor(tile_index, direction)
                if self.tile_exists(neighbour_index):
                    neighbour_code = self.get_code(neighbour_index)
                    if tile_code[direction] != neighbour_code[reverse_direction(direction)]:  # by the use of 'reverse_direction' we can compare the main tile's direction with the neighbour's opposite direction
                        return False  # if the codes are not the same then we return 'False' as one false result is enough to call it illegal
        return True

    def has_loop(self, color):
        """ Check whether a tile configuration has a loop of size 10 of given color """

        # check if the board has a legal configuration to start with
        if not self.is_legal():
            return False

        # choose arbitrary starting point
        indices = self._tile_value.keys()
        start_index = indices[0]  # these are '(0, 3, 3)' etc.
        start_code = self._tile_value[start_index]  # these are 'BRYBYR' etc.
        next_direction = start_code.find(color)  # this will return the index (direction) of the first color we came across
        next_index = self.get_neighbor(start_index, next_direction)  # this will get the index of the next tile, along the given color
        current_length = 1  # we start counting the elements in the chain

        # loop through neighboring tiles that match given color
        while start_index != next_index:  # we keep going until we are back at the same tile
            current_index = next_index
            if not self.tile_exists(current_index):  # if the current tile to which the previous color direction pointed does not exist, then it is enough to break
                return False
            current_code = self._tile_value[current_index]
            if current_code.find(color) == reverse_direction(next_direction):  # Case 1: the first color we came across with 'find()' is the one that matches the direction it came across
                next_direction = current_code.rfind(color)  # if true, then the new direction is the last (other) collor in the code, by using 'rfind()'
            else:
                next_direction = current_code.find(color)  # Case 2:
            next_index = self.get_neighbor(current_index, next_direction)
            current_length += 1

        return current_length == len(SOLITAIRE_CODES)


poc_tantrix_gui.TantrixGUI(Tantrix(6))


def testing_Tantrix():
    """ Function for testing of class's methods """
    tan = Tantrix(6)

    print(tan.get_neighbor((2, 2, 2), 0)) # we can see here that the directions start from the lower-right and go clockwise
    print(tan.get_neighbor((2, 2, 2), 1))
    print(tan.get_neighbor((2, 2, 2), 2))
    print(tan.get_neighbor((2, 2, 2), 3))
    print(tan.get_neighbor((2, 2, 2), 4))
    print(tan.get_neighbor((2, 2, 2), 5))

    print(tan.is_legal())

    tan._tile_value = {(2, 2, 2): 'YRRYBB', (3, 2, 1): 'YRBBYR', (2, 1, 3): 'YBBRYR', (1, 1, 4): 'BYRYBR', (4, 1, 1): 'BYRBRY', (3, 1, 2): 'RBRBYY', (3, 0, 3): 'RYYRBB', (4, 0, 2): 'RYYBRB', (1, 2, 3): 'YRBYBR', (0, 2, 4): 'BRRYYB'}
    print(tan.has_loop("Y"))  # this is a winning configuration of yellow "Y" for debugging


#testing_Tantrix()
