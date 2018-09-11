# -*- encoding: utf-8 -*-
""" Template testing suite for Project_2 - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # imports testing engine
import _03_Project_2 as pro  # imports the algorithms we are going to test


def run_suite():
    """ Some informal testing code """
    print("\nSTARTING TESTS:")
    suite = poc_simpletest.TestSuite() # create a TestSuite object

    # 1. check the basic methods of the program
    suite.run_test(pro.bfs_visited({0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}, 0), set([0, 1, 2, 3]), "Test #1a: 'bfs_visited' method")
    suite.run_test(pro.bfs_visited({0: set([]), 1: set([2]), 2: set([1]), 3: set([])}, 0), set([0]), "Test #1b: 'bfs_visited' method")
    suite.run_test(pro.bfs_visited({0: set([]), 1: set([2]), 2: set([1]), 3: set([])}, 2), set([1, 2]), "Test #1b: 'bfs_visited' method")

    # 2. check the basic methods of the program
    suite.run_test(pro.cc_visited({0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}), [set([0, 1, 2, 3])], "Test #2a: 'cc_visited' method")
    suite.run_test(pro.cc_visited({0: set([]), 1: set([2]), 2: set([1]), 3: set([]), 4: set([])}), [set([0]), set([1, 2]), set([3]), set([4])], "Test #2b: 'cc_visited' method")
    suite.run_test(pro.cc_visited({0: set([]), 1: set([]), 2: set([]), 3: set([])}), [set([0]), set([1]), set([2]), set([3])], "Test #2c: 'cc_visited' method")

    # 3. check the basic methods of the program
    suite.run_test(pro.largest_cc_size({0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}), 4, "Test #3a: 'largest_cc_size' method")
    suite.run_test(pro.largest_cc_size({0: set([]), 1: set([2, 3]), 2: set([1]), 3: set([1]), 4: set([])}), 3, "Test #3b: 'largest_cc_size' method")
    suite.run_test(pro.largest_cc_size({0: set([]), 1: set([]), 2: set([]), 3: set([])}), 1, "Test #3c: 'largest_cc_size' method")  # if there are no edges, then the answer is '1' as there is one node at the time

    # 4. check the basic methods of the program
    suite.run_test(pro.compute_resilience({0: set([]), 1: set([2, 3]), 2: set([1]), 3: set([1]), 4: set([])}, [2, 3, 1]), [3, 2, 1, 1], "Test #4a: 'compute_resilience' method")  # first element in the list is the initial state

    # 6. report number of tests and failures
    suite.report_results()


run_suite()
