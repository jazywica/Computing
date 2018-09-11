""" Grid class """
#http://www.codeskulptor.org/#poc_grid.py

EMPTY = 0
FULL = 1


class Grid:
    """ Implementation of 2D grid of cells. Includes boundary handling """
    def __init__(self, grid_height, grid_width):
        """ Initializes grid to be empty, take height and width of grid as parameters. Indexed by rows (left to right), then by columns (top to bottom) """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)] # initializes empty cells: [[0, 0, 0, ...,  0], [0, 0, 0, ..., 0], ... ,[0, 0, 0, ..., 0]]

    def __str__(self):
        """ Return multi-line string representation for grid """
        ans = ""
        for row in range(self._grid_height):
            ans += str(self._cells[row])
            ans += "\n"
        return ans

    def get_grid_height(self):
        """ Return the height of the grid for use in the GUI """
        return self._grid_height

    def get_grid_width(self):
        """ Return the width of the grid for use in the GUI """
        return self._grid_width

    def clear(self):
        """ Clears grid to be empty """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]

    def set_empty(self, row, col):
        """ Set cell with index (row, col) to be empty """
        self._cells[row][col] = EMPTY

    def set_full(self, row, col):
        """ Set cell with index (row, col) to be full """
        self._cells[row][col] = FULL

    def is_empty(self, row, col):
        """ Checks whether cell with index (row, col) is empty """
        return self._cells[row][col] == EMPTY

    def four_neighbors(self, row, col):
        """ Returns horiz/vert neighbors of cell (row, col) """
        ans = []
        if row > 0:
            ans.append((row - 1, col)) # cell above
        if row < self._grid_height - 1:
            ans.append((row + 1, col)) # cell below
        if col > 0:
            ans.append((row, col - 1)) # cell to left
        if col < self._grid_width - 1:
            ans.append((row, col + 1)) # cell to right
        return ans

    def eight_neighbors(self, row, col):
        """ Returns horiz/vert neighbors of cell (row, col) as well as diagonal neighbors """
        ans = []
        if row > 0:
            ans.append((row - 1, col)) # cell above
        if row < self._grid_height - 1:
            ans.append((row + 1, col)) # cell below
        if col > 0:
            ans.append((row, col - 1)) # cell to left
        if col < self._grid_width - 1:
            ans.append((row, col + 1)) # cell to right
        if (row > 0) and (col > 0):
            ans.append((row - 1, col - 1)) # upper left
        if (row > 0) and (col < self._grid_width - 1):
            ans.append((row - 1, col + 1)) # upper right
        if (row < self._grid_height - 1) and (col > 0):
            ans.append((row + 1, col - 1)) # lower left
        if (row < self._grid_height - 1) and (col < self._grid_width - 1):
            ans.append((row + 1, col + 1)) # lower right
        return ans

    def get_index(self, point, cell_size): # the cell size is defined in the gui, this is just so the squares are of reasonable size (not just a dot)
        """ Takes point in screen coordinates and returns index of containing cell """
        return (point[1] // cell_size, point[0] // cell_size) # depending on the 'cell_size' we will output an integer of within which cell the cursor is
