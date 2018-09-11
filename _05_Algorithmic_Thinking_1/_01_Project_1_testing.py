# -*- encoding: utf-8 -*-
""" Template testing suite for Project_1 - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # imports testing engine
import _01_Project_1 as pro  # imports the algorithms we are going to test
import alg_module1_graphs as test_graphs  # http://storage.googleapis.com/codeskulptor-alg/alg_module1_graphs.py


def run_suite():
    """ Some informal testing code """
    print("\nSTARTING TESTS:")
    suite = poc_simpletest.TestSuite()  # create a TestSuite object

    # 1. check the basic methods of the program
    suite.run_test(pro.make_complete_graph(4), {0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}, "Test #1a: 'make_complete_graph' method")

    suite.run_test(pro.compute_in_degrees(test_graphs.GRAPH1), {0: 4, 1: 0, 2: 0, 3: 0, 4: 0}, "Test #1b: 'compute_in_degrees' method")
    suite.run_test(pro.compute_in_degrees(test_graphs.GRAPH4), {'cat': 1, 'monkey': 0, 'banana': 1, 'dog': 1}, "Test #1c: 'compute_in_degrees' method")

    suite.run_test(pro.in_degree_distribution(test_graphs.GRAPH1), {0: 4, 4: 1}, "Test #1d: 'in_degree_distribution' method")
    suite.run_test(pro.in_degree_distribution(pro.EX_GRAPH1), {1: 5, 2: 2}, "Test #1d: 'in_degree_distribution' method")

    # 6. report number of tests and failures
    suite.report_results()


run_suite()
