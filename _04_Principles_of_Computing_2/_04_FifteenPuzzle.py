# -*- encoding: utf-8 -*-
""" Loyd's Fifteen puzzle - solver and visualizer. Note that solved configuration has the blank (zero) tile in upper left. Use the arrows key to swap this tile with its neighbors """
# http://www.codeskulptor.org/#user44_XxMMGBT0V1_9.py
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_XxMMGBT0V1_11.py

import poc_fifteen_gui


class Puzzle:
    """ Class representation for the Fifteen puzzle """
    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """ Initialize puzzle with default height and width. Returns a Puzzle object """

        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row for col in range(self._width)] for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """ Generate string representaion for puzzle. Returns a string """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans


    # 1. GUI methods
    def get_height(self):
        """ Getter for puzzle height. Returns an integer """
        return self._height

    def get_width(self):
        """ Getter for puzzle width. Returns an integer """
        return self._width

    def get_number(self, row, col):
        """ Getter for the number at tile position pos. Returns an integer """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """ Setter for the number at tile position pos """
        self._grid[row][col] = value

    def clone(self):
        """ Make a copy of the puzzle to update during solving. Returns a Puzzle object """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle


    # 2. Core puzzle methods
    def current_position(self, solved_row, solved_col):
        """ Locate the current position of the tile that will be at position (solved_row, solved_col) when the puzzle is solved. Returns a tuple of two integers """
        solved_value = (solved_col + self._width * solved_row)  # This is the computed value of the solved position - whatever column we have plus the amount od rows to get there

        for row in range(self._height):  # these two loops scan the whole grid for a solved value
            for col in range(self._width):
                if self._grid[row][col] == solved_value:  # if we find it, we then return it
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """ Updates the puzzle state based on the provided move string """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction


    # 3. Helper functions
    def position_tile(self, target_row, target_col, row, col):
        """ Solving function for common cases. This function will allow us to look for a different value than the one we are starting from """
        delta_height = target_row - row
        delta_width = target_col - col

        total_move = "u" * delta_height  # the appropriate move upwards must be appended first
        default_move_down = "druld"  # this is the method of bringing the target down to its position, we are going to put the cursor to the left of the target to be able to use it

        if delta_width == 0:  # Case 1: the target is in the same column as the solved position
            total_move += "ld" + default_move_down * (delta_height - 1)  # we first set up tile 0 to the left of target, then by the use of 'druld' with 'd' at the start and end we bring the target down, ending up to its left again
        else:  # Case 2: the target is either to left or to the right of the solved position
            default_move_left = "drrul" if row == 0 else "urrdl"  # if we are on the first row then we move the tiles by going below it, in other cases, we go above it in order not to disturb the already solved positions
            if delta_width > 0:  # the target tile is to the left of the cursor
                total_move += "l" * delta_width + default_move_left * (delta_width - 1)  # this will place the cursor to the left of the target (it will move it to by one already) and then move the target to the left
            else:  # the target tile is to the right of the cursor
                total_move += "r" * abs(delta_width) + "dllu" + "rdllu" * (abs(delta_width) - 1)  # same as going to left, but here we have to use an extra "dllu" move to get to the left of the target
            total_move += default_move_down * (delta_height)  # in both cases, we put the cursor to the left of the target and then bring it down
        return total_move


    # 4. Phase one methods
    def lower_row_invariant(self, target_row, target_col):
        """ Check whether the puzzle satisfies the specified invariant at the given position in the bottom rows of the puzzle (target_row > 1). Returns a boolean """
        if self.get_number(target_row, target_col) != 0:  # Condition no 1: Tile zero is positioned at (i,j).
            return False

        for row in range(target_row + 1, self._height):  # Condition no 2: All tiles in rows i+1 or below are positioned at their solved location.
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    return False

        for col in range(target_col + 1, self._width):  # Condition no 3: All tiles in row i to the right of position (i,j) are positioned at their solved location.
            if self.current_position(target_row, col) != (target_row, col):
                return False

        return True  # if none of the false cases happen then we return true

    def solve_interior_tile(self, target_row, target_col):
        """ Place correct tile at target position. Updates puzzle and returns a move string """
        assert self.lower_row_invariant(target_row, target_col)  # this is the assertion for the current position that has to be true before we even begin

        row, col = self.current_position(target_row, target_col)  # 'row' and 'col' will tell us where the target file actually is, while target_row is the target tile we want to solve
        total_move = self.position_tile(target_row, target_col, row, col)

        self.update_puzzle(total_move)
        assert self.lower_row_invariant(target_row, target_col - 1)  # now we can check the invariant of a tile to the left
        return total_move

    def solve_col0_tile(self, target_row):
        """ Solve tile in column zero on specified row (> 1). Updates puzzle and returns a move string """
        assert self.lower_row_invariant(target_row, 0)  # this is the assertion for the current position that has to be true before we even begin

        total_move = "ur"  # we will try to get lucky and see if the tile we are looking for is directly above us
        self.update_puzzle(total_move)
        row, col = self.current_position(target_row, 0)  # 'row' and 'col' will tell us where the target file actually is, while target_row is the target tile we want to solve
        if target_row == row:  # This is the lucky case, where the right tile was just above the target row
            current_move = "r" * (self.get_width() - 2)
            total_move += current_move
        else:  # this is the unlucky case where we have to use something similar to 'solve_interior_tile' except that the 'target_row' is going to be in the mid-temporary position
            mid_row, mid_col = self.current_position(0, 0)  # "Reposition the target tile to position (i−1,1) and the zero tile to position (i−1,0) using a process similar to that of solve_interior_tile.."
            current_move = self.position_tile(mid_row, mid_col, row, col)  # this is where the helper function becomes handy, as we can keep the original 'row' and 'col' and change the starting position

            current_move += "ruldrdlurdluurddlur" + (self.get_width() - 2) * 'r'  # now we just have to add the solver for the 3x2 grid (exercise 9)
            total_move += current_move

        self.update_puzzle(current_move)
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)  # now we can check the invariant of a row above
        return total_move


    # 4. Phase two methods
    def row0_invariant(self, target_col):
        """ Check whether the puzzle satisfies the row zero invariant at the given column (col > 1). Returns a boolean """
        if self.get_number(0, target_col) != 0 or (1, target_col) != self.current_position(1, target_col):  # Condition no 1: Tile zero is positioned at (0,j) and tile at (1,j) is solved
            return False

        for row in range(0, 2):  # Condition no 2: All tiles in rows 1 and 2 are positioned at their solved location (we already checked the tile below 0 so we can start with 'target_col' + 1
            for col in range(target_col + 1, self._width):
                if self.current_position(row, col) != (row, col):
                    return False

        for row in range(2, self._height):  # Condition no 3: All tiles in rows 3 or below are positioned at their solved location
            for col in range(0, self._width):
                if self.current_position(row, col) != (row, col):
                    return False

        return True  # if none of the false cases happen then we return true

    def row1_invariant(self, target_col):
        """ Check whether the puzzle satisfies the row one invariant at the given column (col > 1). Returns a boolean """
        for col in range(target_col + 1, self._width):  # Condition no 1: check if all the columns in row 0 to the right are solved
            if self.current_position(0, col) != (0, col):
                return False

        if not self.lower_row_invariant(1, target_col):  # Condition no 2: check all the tiles below as normal, using the already made procedure
            return False

        return True  # if none of the false cases happen then we return true

    def solve_row0_tile(self, target_col):
        """ Solve the tile in row zero at the specified column. Updates puzzle and returns a move string """
        assert self.row0_invariant(target_col)

        total_move = "ld"  # we will try to get lucky and see if the tile we are looking for is directly to the left
        self.update_puzzle(total_move)
        row, col = self.current_position(0, target_col)  # 'row' and 'col' will tell us where the target file actually is, while target_row is the target tile we want to solve
        if target_col != col:  # This is the unlucky case, where the right tile was somewhere else than just above the target row
            mid_row, mid_col = self.current_position(0, 0)  # " If not, reposition the target tile to position (1,j−1) with tile zero in position(1,j−2)"
            current_move = self.position_tile(mid_row, mid_col, row, col) + "urdlurrdluldrruld"  # this is the combination of moves to get from the mid to solve position
            self.update_puzzle(current_move)
            total_move += current_move

        assert self.row1_invariant(target_col - 1)  # we have moved the '0' tile down to row 1
        return total_move  # the lucky case is pretty much here, where we just return 'total_move'

    def solve_row1_tile(self, target_col):
        """ Solve the tile in row one at the specified column. Updates puzzle and returns a move string """
        assert self.row1_invariant(target_col)

        row, col = self.current_position(1, target_col)
        total_move = self.position_tile(1, target_col, row, col)
        total_move += 'ur'

        self.update_puzzle(total_move)
        assert self.row0_invariant(target_col)
        return total_move


    # 5. Phase 3 methods
    def solve_2x2(self):
        """ Solve the upper left 2x2 part of the puzzle. Updates the puzzle and returns a move string """
        assert self.row1_invariant(1)  # The method 'solve_2x2()' solves the final upper left 2×2 portion of the puzzle under the assumption that the remainder of the puzzle is solved (i.e, 'row1_invariant(1)' is true)

        total_move = "ul"  # this is an assumption that the tile'0' will be at (1, 1) position
        self.update_puzzle(total_move)

        default_move = "rdlu" if self.get_number(0, 1) < self.get_number(1, 0) else 'drul'  # depending on which side the bigger number is, we either go clockwise or counterclockwise

        while self.current_position(0, 0) != (0, 0) or self.current_position(1, 1) != (1, 1):  # we know from the Quiz, that we can do "rdlu' max 3 times, so its ok just to try
            self.update_puzzle(default_move)
            total_move += default_move

        assert self.lower_row_invariant(0, 0)
        return total_move

    def solve_puzzle(self):
        """ Generate a solution string for a puzzle. Updates the puzzle and returns a move string """
        end_row = self.get_height() - 1  # first we need to find the distance between tile '0' and the lower end of our board
        end_col = self.get_width() - 1
        current_row, current_col = self.current_position(0, 0)
        total_move = "r" * (end_col - current_col) + "d" * (end_row - current_row)  # this is the move that we are going to use for placing the '0' tile
        self.update_puzzle(total_move)

        for row in range(end_row, 1, -1):  # this part is for solving the bottom rows
            for col in range(end_col, 0, -1):
                total_move += self.solve_interior_tile(row, col)
            total_move += self.solve_col0_tile(row)

        for col in range(end_col, 1, -1):  # this part is for solving the top two rows
            total_move += self.solve_row1_tile(col)
            total_move += self.solve_row0_tile(col)

        total_move += self.solve_2x2()  # this part is solving the remaining 2x2 upper-left grid

        return total_move


# Start interactive simulation
gui = poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
