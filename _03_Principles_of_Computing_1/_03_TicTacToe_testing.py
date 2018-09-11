# -*- encoding: utf-8 -*-
""" Template testing suite for TIc Tac Toe - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # this imports our testing engine
import _03_TicTacToe as tictac  # this imports the algorithms we are going to test
import poc_ttt_provided as provided


def run_suite(board_class):  # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    suite = poc_simpletest.TestSuite()  # create a TestSuite object
    board = board_class(3)  # here we create an object of the class, which functionality we want to test

    # 1. test the initial configuration of the board using the '__str__' method
    print(board)  # should print an empty board

    # 2. check the basic methods of the BOARD CLASS
    suite.run_test(board.check_win(), None, "Test #2a: check_win")  # this should return 'None' as the game is in play and there is no winner
    board.move(0, 0, 2); board.move(0, 2, 3); board.move(1, 1, 2); board.move(1, 2, 3); board.move(2, 2, 2)  # this simulates the whole game, where 'X' wins
    print(board)
    suite.run_test(board.square(1, 1), 2, "Test #2b: square value")
    suite.run_test(board.get_empty_squares(), [(0, 1), (1, 0), (2, 0), (2, 1)], "Test #2c: get_empty_squares")
    suite.run_test(board.check_win(), 2, "Test #2d: check_win")  # now this should return '2' as 'X' won the game
        # [[2, 1, 3], [1, 2, 3], [1, 1, 2]] - this is the list of list we are checking (only rows)
        # [[2, 1, 3], [1, 2, 3], [1, 1, 2], [2, 1, 1], [1, 2, 1], [3, 3, 2]] - this is now rows plus columns
        # [[2, 1, 3], [1, 2, 3], [1, 1, 2], [2, 1, 1], [1, 2, 1], [3, 3, 2], [2, 2, 2], [3, 2, 1]] - this now contains also diagonals, here the [2, 2, 2] list is a win of 'PLAYERX'
    suite.run_test(provided.switch_player(2), 3, "Test #2e: switch_player")  # this switches between 2 and 3

    # 3. check the main functions directly: 'mc_trial'
    board = board_class(3)
    board.move(0, 0, 2); board.move(0, 2, 3); board.move(1, 1, 2); board.move(1, 2, 3)  # should return: [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]
    print("Test #3a: mc_trial: ")
    tictac.mc_trial(board, 2)
    suite.run_test_in_range(board.check_win(), [2, 3, 4], "Test #3a: mc_trial")  # the 'mc_trial' function should return the winner (2 or 3) or a draw situation
    print(board)

    # 4. check the main functions directly: 'mc_update_scores'
    dim = board.get_dim()
    scores = [[0 for dummycol in range(dim)] for dummyrow in range(dim)]  # Create empty score board
    tictac.mc_update_scores(scores, board, 2)
    print(scores)

    scores = [[0 for dummycol in range(dim)] for dummyrow in range(dim)]
    board = board_class(3)
    board.move(0, 0, 2); board.move(0, 1, 3); board.move(0, 2, 2); board.move(1, 0, 2); board.move(1, 1, 3); board.move(1, 2, 2); board.move(2, 0, 3); board.move(2, 1, 2); board.move(2, 2, 3) # DRAW
    suite.run_test(scores, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "Test #4: mc_update_scores")  # this is a draw, so it
    print(board)

    # 5. check the main functions directly: 'get_best_move'
    board = board_class(3); board.move(0, 0, 2); board.move(0, 1, 3); board.move(0, 2, 2)
    scores = [[200, 0, 105], [90, 50, 99], [100, 100, 50]]  # here the first row should win, but it is already filled therefore it will be the ones with value '100'
    suite.run_test_in_range(tictac.get_best_move(board, scores), [(2, 0), (2, 1)], "Test #5: get_best_move")

    # 6. check the main functions directly: 'mc_move'
    print("Test 6:")
    board = board_class(3); board.move(0, 0, 2); board.move(0, 2, 3); board.move(1, 1, 2); board.move(1, 2, 3)  # this simulates situation, where 'X' wins, and there is only one good next step
    print(board)
    suite.run_test(tictac.mc_move(board, 2, 100), (2, 2), "Test #6: mc_move")

    # 7. report number of tests and failures
    suite.report_results()


# we run the test with a local 'run_suite' method, to which we pass the CLASS REFERENCE which we are going to test
run_suite(provided.TTTBoard)  # here we import the board class for testing
