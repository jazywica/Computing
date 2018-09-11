# -*- encoding: utf-8 -*-
""" Template testing suite for Yahtzee - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # this imports our testing engine
import _04_Yahtzee as yah  # this imports the algorithms we are going to test

def run_suite():  # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    suite = poc_simpletest.TestSuite()  # create a TestSuite object

    # 1. test 'score' on various inputs
    suite.run_test(yah.score((1, 1, 1, 5, 6)), 6, "Test #1.1: score")
    suite.run_test(yah.score((2, 3, 3, 4, 5)), 6, "Test #1.2: score")
    suite.run_test(yah.score((1, 1, 5, 5, 6)), 10, "Test #1.3: score")
    suite.run_test(yah.score((1, 1, 1, 1, 1)), 5, "Test #1.4: score")
    suite.run_test(yah.score((6, 6, 6, 6, 6)), 30, "Test #1.5: score")
    suite.run_test(yah.score((1, 2, 2)), 4, "Test #1.6: score")
    suite.run_test(yah.score((5, )), 5, "Test #1.7: score")
    suite.run_test(yah.score(()), 0, "Test #1.8: score")


    # 2. test 'expected_value' on various inputs
    num_die_sides = 3  # here we can manipulate the amount of data for testing
    suite.run_test(yah.expected_value((1, 1, 3, 3), num_die_sides, 1), 7.0, "Test #2.1: expected_value")


    # 3. test 'gen_all_holds' on various inputs
    hand = tuple([])
    suite.run_test(yah.gen_all_holds(hand), set([()]), "Test #3.1: gen_all_holds")
    hand = tuple([1,])
    suite.run_test(yah.gen_all_holds(hand), set([(), (1,)]) , "Test #3.2: gen_all_holds")
    hand = tuple([2, 4])
    suite.run_test(yah.gen_all_holds(hand), set([(), (2,), (4,), (2, 4)]), "Test #3.3: gen_all_holds")
    hand = tuple([3, 3, 3])
    suite.run_test(yah.gen_all_holds(hand), set([(), (3,), (3, 3), (3, 3, 3)]), "Test #3.4: gen_all_holds")
    hand = tuple([1, 2, 2])
    suite.run_test(yah.gen_all_holds(hand), set([(), (1,), (2,), (1, 2), (2, 2), (1, 2, 2)]), "Test #3.5: gen_all_holds")
    hand = tuple([2, 3, 6])
    suite.run_test(yah.gen_all_holds(hand), set([(), (2,), (3,), (6,), (2, 3), (2, 6), (3, 6), (2, 3, 6)]), "Test #3.6: gen_all_holds")


    # 4. test 'strategy' on various inputs
    num_die_sides = 6  # here we can manipulate the amount of data for testing
    suite.run_test(yah.strategy((1,), num_die_sides, ), (3.5, ()), "Test #4.1: strategy")
    suite.run_test(yah.strategy((1, 1, 1, 5, 6), num_die_sides,), (10.691358024691358, (6,)), "Test #4.1: strategy")


    # 5. report number of tests and failures
    suite.report_results()


# we run the test with a local 'run_suite' method, to which we pass the CLASS REFERENCE which we are going to test
run_suite()
