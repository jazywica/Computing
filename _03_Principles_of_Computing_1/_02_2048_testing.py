# -*- encoding: utf-8 -*-
""" Template testing suite for 2048 - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # this imports our testing engine
import _02_2048 as game  # this imports the algorithms we are going to test


def run_suite(TwentyFortyEight): # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    suite = poc_simpletest.TestSuite() # create a TestSuite object

    # 1. test 'merge' on various inputs
    suite.run_test(game.merge([2, 0, 2, 2]), [4, 2, 0, 0], "Test #1.1: merge")
    suite.run_test(game.merge([2, 0, 2, 4]), [4, 4, 0, 0], "Test #1.2: merge")
    suite.run_test(game.merge([0, 0, 2, 2]), [4, 0, 0, 0], "Test #1.3: merge")
    suite.run_test(game.merge([2, 2, 0, 0]), [4, 0, 0, 0], "Test #1.4: merge")
    suite.run_test(game.merge([2, 2, 2, 2, 2]), [4, 4, 2, 0, 0], "Test #1.5: merge")
    suite.run_test(game.merge([8, 16, 16, 8]), [8, 32, 8, 0], "Test #1.6: merge")
    suite.run_test(game.merge([4, 2, 2]), [4, 4, 0], "Test #1.7: merge")


    # 2. test 'expected_value' on various inputs
    obj = TwentyFortyEight(4, 4)
    obj.set_tile(0, 0, 0), obj.set_tile(0, 1, 0), obj.set_tile(0, 2, 4), obj.set_tile(0, 3, 2)
    obj.set_tile(1, 0, 0), obj.set_tile(1, 1, 0), obj.set_tile(1, 2, 4), obj.set_tile(1, 3, 2)
    obj.set_tile(2, 0, 0), obj.set_tile(2, 1, 0), obj.set_tile(2, 2, 4), obj.set_tile(2, 3, 2)
    obj.set_tile(3, 0, 0), obj.set_tile(3, 1, 0), obj.set_tile(3, 2, 4), obj.set_tile(3, 3, 2)
    print(obj)
    suite.run_test(obj.get_tile(0, 0), 0, "Test #2.1: checkng the value of a tile - before the move")
    suite.run_test(obj.get_tile(1, 0), 0, "Test #2.2: checkng the value of a tile - before the move")
    suite.run_test(obj.get_tile(2, 0), 0, "Test #2.3: checkng the value of a tile - before the move")
    suite.run_test(obj.get_tile(3, 0), 0, "Test #2.4: checkng the value of a tile - before the move")

    obj.move(game.LEFT) # now we move everything to the left
    suite.run_test(obj.get_tile(0, 0), 4, "Test #2.5: checkng the value of a tile - after the move")
    suite.run_test(obj.get_tile(1, 0), 4, "Test #2.6: checkng the value of a tile - after the move")
    suite.run_test(obj.get_tile(2, 0), 4, "Test #2.7: checkng the value of a tile - after the move")
    suite.run_test(obj.get_tile(3, 0), 4, "Test #2.8: checkng the value of a tile - after the move")
    print(obj)


    # 3. report number of tests and failures
    suite.report_results()


# we run the test with a local 'run_suite' method, to which we pass the CLASS REFERENCE which we are going to test
run_suite(game.TwentyFortyEight)
