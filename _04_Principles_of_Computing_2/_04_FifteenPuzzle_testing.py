# -*- encoding: utf-8 -*-
""" Template testing suite for Fifteen puzzle - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # this imports our testing engine
import _04_FifteenPuzzle as puzzle  # this imports the algorithms we are going to test

TILE_SIZE = 60

def run_suite(Puzzle):  # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    print("\nSTARTING TESTS:")
    suite = poc_simpletest.TestSuite() # create a TestSuite object


    # 1. check the basic methods of the PUZZLE CLASS
    puz = Puzzle(3, 4); print(puz)
    suite.run_test(puz.get_height(), 3, "Test #1a: 'get_height' method")  # 'height' is the number of rows
    suite.run_test(puz.get_width(), 4, "Test #1b: 'remove_duplicate' method")  # 'width' is the number of columns
    suite.run_test(puz.get_number(1, 1), 5, "Test #1c: 'get_number' method")

    suite.run_test(puz.update_puzzle("rrrdd"), None, "Test #1d: 'update_puzzle' method")  # this is how we move '0' tile to the opposite end
    suite.run_test(puz.current_position(1, 3), (0, 3), "Test #1e: 'current_position' method")  # this shows where is the tile we are looking for, by giving it's solved position ex: at (1, 3) should be '7', but it is at (0, 3)
    print(puz)


    # 2. check the main functions of PHASE ONE
    puz = Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 0, 14, 15]])  # this is the situation from Homework, question 8
    suite.run_test(puz.lower_row_invariant(3, 1), True, "Test #2a: 'lower_row_invariant' method")
    print(puz)

    suite.run_test(puz.solve_interior_tile(3, 1), "uuulddrulddruld", "Test #2b: 'solve_interior_tile' method - center")
    print(puz)
    puz = Puzzle(4, 4, [[4, 15, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 13, 14, 0]])  # this is the situation where the target is to the left
    print(puz)
    suite.run_test(puz.solve_interior_tile(3, 3), "uuulldrruldrulddrulddruld", "Test #2c: 'solve_interior_tile' method - to left")
    print(puz)
    puz = Puzzle(4, 4, [[4, 3, 1, 13], [5, 10, 2, 7], [8, 12, 6, 11], [9, 0, 14, 15]])  # this is the situation where the target is to the left
    suite.run_test(puz.solve_interior_tile(3, 1), "uuurrdllurdlludrulddrulddruld", "Test #2d: 'solve_interior_tile' method - to right")
    print(puz)

    puz = Puzzle(4, 4, [[4, 3, 1, 9], [5, 10, 2, 7], [12, 8, 6, 11], [0, 13, 14, 15]]); print(puz)
    suite.run_test(puz.solve_col0_tile(3), "urrr", "Test #2e: 'solve_col0_tile' method - lucky case")
    print(puz)
    puz = Puzzle(4, 4, [[4, 3, 1, 12], [5, 10, 2, 7], [9, 8, 6, 11], [0, 13, 14, 15]]); print(puz)
    suite.run_test(puz.solve_col0_tile(3), "uruurrdllurdlludrulddruldruldrdlurdluurddlurrr", "Test #2f: 'solve_col0_tile' method - unlucky case")
    print(puz)


    # 3. check the main functions of PHASE TWO
    puz = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]]); print(puz)
    suite.run_test(puz.row1_invariant(1), True, "Test #3a: 'row1_invariant' method")
    suite.run_test(puz.row1_invariant(2), False, "Test #3b: 'row1_invariant' method")

    puz = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]]); print(puz)
    suite.run_test(puz.row0_invariant(0), True, "Test #3c: 'row0_invariant' method")

    puz = Puzzle(4, 5, [[7, 6, 5, 3, 2], [4, 1, 9, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]]); print(puz)
    suite.run_test(puz.solve_row1_tile(4), "llurrdlur", "Test #3d: 'solve_row1_tile' method")

    puz = Puzzle(3, 3, [[4, 2, 0], [3, 1, 5], [6, 7, 8]]); print(puz)
    suite.run_test(puz.solve_row0_tile(2), "ld", "Test #3e: 'solve_row0_tile' method - lucky case")

    puz = Puzzle(3, 3, [[3, 1, 0], [2, 4, 5], [6, 7, 8]]); print(puz)  # this is the situation from Homework, question 10 (from the midpoint onwards - the first two lines only)
    suite.run_test(puz.solve_row0_tile(2), "ldlurdlurrdluldrruld", "Test #3f: 'solve_row0_tile' method - unlucky case")


    # 4. check the main functions of PHASE THREE
    puz = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]]); print(puz)  # this is the situation from Homework, question 3-5
    suite.run_test(puz.solve_2x2(), "uldrul", "Test #4a: 'solve_2x2' method")

    puz = Puzzle(4, 3, [[3, 0, 2], [4, 1, 5], [9, 7, 8], [10, 6, 11]]); print(puz)
    suite.run_test(puz.solve_puzzle(), "rddduldlurrulduldurruldurldulrdlu", "Test #4b: 'solve_puzzle' method")

    puz = Puzzle(4, 4, [[0, 4, 8, 2], [15, 1, 14, 3], [5, 13, 10, 7], [12, 9, 6, 11]]); print(puz)  # this is the example from he last video
    suite.run_test(puz.solve_puzzle(), "rrrddduulllurrdlurrdldrulddrulduuurdlludrulddrulddrulduurdlludrulddruldurlruldrdlurdluurddlurrrullurrdldrulduulddrulduurrdllurdlludrulddrulduruldruldrdlurdluurddlurrrlurlduldruldurdlurrdluldrruldlurldulrdlu", "Test #4b: 'solve_puzzle' method")
    print(puz)


    # 6. report number of tests and failures
    suite.report_results()


# we run the test with a local 'run_suite' method, to which we pass the CLASS REFERENCE which we are going to test
run_suite(puzzle.Puzzle)  # here we import the puzzle for testing
