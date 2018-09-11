# -*- encoding: utf-8 -*-
""" Mini-max Tic-Tac-Toe Player """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_xLTuSJObMu_8.py

import poc_ttt_gui
import poc_ttt_provided as provided
try:
    import codeskulptor
    codeskulptor.set_timeout(60)  # Set timeout, as mini-max can take a long time
except ImportError:
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor


# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1, provided.DRAW: 0, provided.PLAYERO: -1}  # this uses the constance numbers from the TTTBoard class, so it operates on '2' for 'provided.PLAYERX' or '3' for 'provided.PLAYERY' etc.


def mm_move(board, player):
    """ Make a move on the board. Returns a tuple with two elements.  The first element is the score of the given board and the second element is the desired move as a tuple, (row, col). """
    if board.check_win() is not None:  # this is our base case, where we get to the bottom of each subtree
        return SCORES[board.check_win()], (-1, -1)  # the '(-1,-1)' is an illegal move, it should only be returned in cases where there is no move that can be made

    result = (-1, (-1, -1))  # since we are going to look for a max, we start with the worse case possible

    for next_move in board.get_empty_squares():  # we first run through all possible choices X (or Y) player has at this level and we compare them by use of result(left-right) and score (below)
        board_clone = board.clone()  # we have to work on the copy, as we are going to have to go back up the tree and use the original board
        board_clone.move(next_move[0], next_move[1], player)  # here we execute the move on our
        score, dummy_move = mm_move(board_clone, provided.switch_player(player))  # here we call recursively depth-first search all the way down to each leaf, we then will compare the results at each level on the way back
        # print(board_clone)  # this will show us the board as we go up
        if score * SCORES[player] == 1:  # Case 1: the board was scored to be either 1 for X ( * 1) or -1 for Y ( * -1) so someone has won and it is the best choice for that player and we immediately come back
            return score, next_move  # note that here we return the actual score, not the ABSOLUTE VALUE which is only used to same space by using only 'max' instead of both 'max' and 'min'
        elif score * SCORES[player] > result[0]:  # Case 2: the board was scored higher than the score before or the base score, ex: we get '0' score so its greater than what we start with -> (-1, (-1, -1))
            result = score, next_move  # in this case we keep the result as it is and we don't return anything as there maay be other boards on this level to investigate (
        # else: result = result  # we don't have to write this, but it is good to know that we are passing the 'result' unchanged

    return result[0] * SCORES[player], result[1]  # this happens when we finished scanning the whole level and we did not find the winner on this level, we then either return '0' or the other's player winning number (-1 or 1)


def move_wrapper(board, player, trials):
    """ Wrapper to allow the use of the same infrastructure that was used for Monte Carlo Tic-Tac-Toe. """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]


# Test game with the console or the GUI. Uncomment whichever you prefer. Both should be commented out when you submit for testing to save time.
# provided.play_game(move_wrapper, 1, False)
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)  # here we can choose the player
