# -*- encoding: utf-8 -*-
""" Template testing suite for TIc Tac Toe - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # this imports our testing engine
import _03_TicTacToe_Minimax as tictac  # this imports the algorithms we are going to test
import poc_ttt_provided as provided


def run_suite(TTTBoard): # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    suite = poc_simpletest.TestSuite()  # create a TestSuite object
    board = TTTBoard(3)  # here we create an object of the class, which functionality we want to test


    # 1. check the basic methods of the BOARD CLASS on the 'Math Notes on Minimax' example
    board.move(0, 0, 2); board.move(0, 2, 3); board.move(1, 1, 2); board.move(1, 2, 3); board.move(2, 2, 2)  # this simulates the whole game, where 'X' wins
    suite.run_test(board.square(1, 1), 2, "Test #1a: square value")
    suite.run_test(board.get_empty_squares(), [(0, 1), (1, 0), (2, 0), (2, 1)], "Test #1c: get_empty_squares")
    suite.run_test(provided.switch_player(2), 3, "Test #1b: switch_player")  # this switches between 2 and 3

    suite.run_test(board.check_win(), 2, "Test #1c: check_win")  # now this should return '2' as 'X' won the game
    suite.run_test(tictac.SCORES[board.check_win()], 1, "Test #1d: 'SCORES dictionary")  # 'SCORES returns '1' if player X wins
    suite.run_test(tictac.SCORES[3], -1, "Test #1e: 'SCORES dictionary")  # 'SCORES returns '-1' if player Y wins


    # 2. check the basic methods of the BOARD CLASS on the 'Math Notes on Minimax' example
    board = TTTBoard(3); board.move(1, 1, 2); board.move(2, 1, 3); board.move(2, 2, 2); board.move(0, 0, 3); board.move(0, 1, 2); board.move(1, 0, 3)  # this simulates the example from 'Math Notes on Minimax'
    #print(board) # this will print the board thanks to the '__str__' method
    suite.run_test(board.get_empty_squares(), [(0, 2), (1, 2), (2, 0)], "Test #2a: get_empty_squares")
    suite.run_test(board.check_win(), None, "Test #2b: check_win")  # this should return 'None' as the game is in play and there is no winner
    suite.run_test(provided.switch_player(2), 3, "Test #2c: switch_player")  # this switches between 2 and 3


    # 3. check the main functions directly: 'mm_move' on the 'Math Notes on Minimax' example
    board = TTTBoard(3); board.move(1, 1, 2); board.move(2, 1, 3); board.move(2, 2, 2); board.move(0, 0, 3); board.move(0, 1, 2); board.move(1, 0, 3); board.move(0, 2, 2); print(board)
    suite.run_test(tictac.mm_move(board, 3), (-1, (2, 0)), "Test #3a: mm_move - left part of the tree")  # note that here we start from player '3' (playerO)
    board = TTTBoard(3); board.move(1, 1, 2); board.move(2, 1, 3); board.move(2, 2, 2); board.move(0, 0, 3); board.move(0, 1, 2); board.move(1, 0, 3); board.move(1, 2, 2); print(board)
    suite.run_test(tictac.mm_move(board, 3), (-1, (2, 0)), "Test #3b: mm_move - middle part of the tree")
    board = TTTBoard(3); board.move(1, 1, 2); board.move(2, 1, 3); board.move(2, 2, 2); board.move(0, 0, 3); board.move(0, 1, 2); board.move(1, 0, 3); board.move(2, 0, 2); print(board)
    suite.run_test(tictac.mm_move(board, 3), (0, (0, 2)), "Test #3c: mm_move - right part of the tree")

    board = TTTBoard(3); board.move(1, 1, 2); board.move(2, 1, 3); board.move(2, 2, 2); board.move(0, 0, 3); board.move(0, 1, 2); board.move(1, 0, 3); print(board)
    suite.run_test(tictac.mm_move(board, 2), (0, (2, 0)), "Test #3d: mm_move - the whole tree")  # note that here we start from player '2' (playerX) as we are one level higher up

    # 4. check the main functions directly: 'mm_move' on the OwlTest example showing the last line of code -> return SCORES[player] correction
    board = TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]])
    suite.run_test(tictac.mm_move(board, provided.PLAYERX), (0, (1, 2)), "Test #4a: mm_move")
    board = TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]])
    suite.run_test(tictac.mm_move(board, provided.PLAYERX), (1, (0, 0)), "Test #4b: mm_move")

    # 5. report number of tests and failures
    suite.report_results()


# we run the test with a local 'run_suite' method, to which we pass the CLASS REFERENCE which we are going to test
run_suite(provided.TTTBoard)  # here we import the board class for testing
