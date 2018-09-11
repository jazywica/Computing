# -*- encoding: utf-8 -*-
""" Provided Code for Tic-Tac-Toe """
# http://www.codeskulptor.org/#poc_ttt_provided.py

# Constants - these go together with the dictionary below. We use names such as 'EMPTY' etc. but in fact we are using: 1,2,3 and 4
EMPTY = 1
PLAYERX = 2
PLAYERO = 3
DRAW = 4

# Map player constants to letters for printing
STRMAP = {EMPTY: " ", PLAYERX: "X", PLAYERO: "O"}

class TTTBoard:
    """ Class to represent a Tic-Tac-Toe board. """
    def __init__(self, dim, reverse=False, board=None):
        """ Initialize the TTTBoard object with the given dimension and whether or not the game should be reversed. """
        self._dim = dim
        self._reverse = reverse
        if board == None:
            self._board = [[EMPTY for dummycol in range(dim)] for dummyrow in range(dim)] # Create empty board
        else:
            self._board = [[board[row][col] for col in range(dim)] for row in range(dim)] # Copy board grid

    def __str__(self):
        """ Human readable representation of the board. """
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                rep += STRMAP[self._board[row][col]]
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (4 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        """ Return the dimension of the board. """
        return self._dim

    def square(self, row, col):
        """ Returns one of the three constants EMPTY, PLAYERX, or PLAYERO that correspond to the contents of the board at position (row, col). """
        return self._board[row][col]

    def get_empty_squares(self):
        """ Return a list of (row, col) tuples for all empty squares """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        """ Place player on the board at position (row, col). player should be either the constant PLAYERX or PLAYERO. Does nothing if board square is not empty. """
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player

    def check_win(self):
        """ Returns a constant associated with the state of the game:
            If PLAYERX wins, returns PLAYERX. If PLAYERO (2) wins, returns PLAYERO (3). If game is drawn, returns DRAW (4). If game is in progress, returns None. """
        board = self._board
        dim = self._dim
        dimrng = range(dim)
        lines = [] # this is where we are going to store the lines (up-down, left-right, across) for a win

        # rows - this is an example of an empty board: [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        lines.extend(board) # here it is enough to add the existing board, as it is stored as rows

        # cols - this is an example of an empty board: [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]
        cols = [[board[rowidx][colidx] for rowidx in dimrng] for colidx in dimrng] # here we increment the 'rowidx' all the way to the end first, then 'colidx' by one etc..
        lines.extend(cols)

        # diags
        diag1 = [board[idx][idx] for idx in dimrng] # this is diagonal of type '\' which scans rows and columns equally +1
        diag2 = [board[idx][dim - idx - 1] for idx in dimrng] # this is diagonal of type '/' where the column index starts from the end and moves towards the beginning
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines: # here we check all the lists inside the selected lines
            if len(set(line)) == 1 and line[0] != EMPTY: # we make a set of each line and if it is shrinked to one element we assume one of the players won
                if self._reverse:
                    return switch_player(line[0]) # so we return
                else:
                    return line[0]

        # no winner, check for draw
        if len(self.get_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None

    def clone(self):
        """ Return a copy of the board. """
        return TTTBoard(self._dim, self._reverse, self._board)


def switch_player(player):
    """ Convenience function to switch players. Returns other player. """
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX


def play_game(mc_move_function, ntrials, reverse=False):
    """ Function to play a game with two MC players. """
    # Setup game
    board = TTTBoard(3, reverse)
    curplayer = PLAYERX # here we automatically start from player 'X'
    winner = None

    # Run game
    while winner == None: # this loops until the game ends
        # Move
        row, col = mc_move_function(board, curplayer, ntrials)
        board.move(row, col, curplayer)

        # Update state
        winner = board.check_win() # here we check if there is a winner..
        curplayer = switch_player(curplayer) # then we switch to the other player

        # Display board
        print board
        print

    # Print winner
    if winner == PLAYERX:
        print "X wins!"
    elif winner == PLAYERO:
        print "O wins!"
    elif winner == DRAW:
        print "Tie!"
    else:
        print "Error: unknown winner"
