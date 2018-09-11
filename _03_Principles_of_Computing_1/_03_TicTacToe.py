# -*- encoding: utf-8 -*-
""" Tic-Tac-Toe Solver with Monte Carlo method"""
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_UZWKJJH3a5_6.py

import random
import poc_ttt_gui
import poc_ttt_provided as provided


# Constants for Monte Carlo simulator - You may change the values of these constants as desired, but do not change their names.
NTRIALS = 100  # Number of trials to run for MONTE CARLO
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0  # Score for squares played by the other player
DIMENSION = 3


# Add your functions here.
def mc_trial(board, player):
    """ This function takes a current board and the next player to move. It should play a game starting with the given player by making random moves, alternating between players. It return when the game is over.
    The modified board will contain the state of the game, so the function does not return anything. In other words, the function should modify the board input. """
    while board.check_win() == None: # we keep playing until there is no winner
        possible_moves = board.get_empty_squares()
        if len(possible_moves) == 0:
            return
        random_pick = random.choice(possible_moves)
        row = random_pick[0]
        col = random_pick[1]
        board.move(row, col, player)
        player = provided.switch_player(player)

		
def mc_update_scores(scores, board, player):
    """ This function takes a grid of scores (a list of lists) with the same dimensions as the Tic-Tac-Toe board, a board from a completed game, and which player the machine player is.
    The function should score the completed board and update the scores grid. As the function updates the scores grid directly, it does not return anything. """
    dim = board.get_dim()
    opponent = provided.switch_player(player)
    winner = board.check_win()

    if winner == provided.DRAW:  # if there is a DRAW we don't do anything as there are zeroes in the 'score' table already
        return

    for col in range(dim):
        for row in range(dim):
            square_value = board.square(row, col)
            if winner == player:  # When you win one of these random games, you want to favor the squares in which you played (in hope of choosing a winning move) and avoid the squares in which your opponent played
                if square_value == player:
                    scores[row][col] += SCORE_CURRENT
                if square_value == opponent:
                    scores[row][col] -= SCORE_OTHER
            else:  # Conversely, when you lose one of these random games, you want to favor the squares in which your opponent played (to block your opponent) and avoid the squares in which you played.
                if square_value == player:
                    scores[row][col] -= SCORE_CURRENT
                if square_value == opponent:
                    scores[row][col] += SCORE_OTHER

					
def get_best_move(board, scores):
    """ This function takes a current board and a grid of scores. The function should find all of the empty squares with the maximum score and randomly return one of them as a (row, column) tuple.
    It is an error to call this function with a board that has no empty squares (no possible next move), so your function may do whatever it wants in that case. The case where the board is full will not be tested. """
    possible_moves = board.get_empty_squares()

    highest_score = -10000
    highest_scores = []
    for row, col in possible_moves:  # we are going to look for the highest score, if there are many of them we randomly choose one
        score = scores[row][col]
        if score > highest_score:  # if we find a bigger value we start from scratch
            highest_score = score
            highest_scores = []
            highest_scores.append((row, col))
        elif score == highest_score:  # if the next value is the same as the highest we simply appen it
            highest_scores.append((row, col))

    random_pick = random.choice(highest_scores)
    row = random_pick[0]
    col = random_pick[1]
    return (row, col)

	
def mc_move(board, player, trials):
    """ This function takes a current board, which player the machine player is, and the number of trials to run. The function should use the Monte Carlo simulation described above to
    return a move for the machine player in the form of a (row, column) tuple. Be sure to use the other functions you have written! """
    dim = board.get_dim()
    scores = [[0 for dummycol in range(dim)] for dummyrow in range(dim)]  # Create empty score board

    for dummy_trial in range(trials):
        completed_board = board.clone()
        mc_trial(completed_board, player)
        mc_update_scores(scores, completed_board, player)

    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever you prefer.  Both should be commented out when you submit for testing to save time.
# provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(DIMENSION, provided.PLAYERX, mc_move, NTRIALS, False)  # change between 'PLAYERX' and 'PLAYERO' to decide who is going to start
# poc_ttt_gui.run_gui(board dimension, which is the machine player, move function, number of trials per move, reverse argument indicating if you want to play the normal (False) or reverse (True) game.)
