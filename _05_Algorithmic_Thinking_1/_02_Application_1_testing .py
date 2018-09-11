# -*- encoding: utf-8 -*-
""" Template testing suite for Application_1 - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest # imports testing engine
import _02_Application_1 as app_1  # imports the algorithms we are going to test
import alg_dpa_trial as dpa


def run_suite():
    """ Some informal testing code """
    print("\nSTARTING TESTS:")
    suite = poc_simpletest.TestSuite()  # create a TestSuite object

    # 1. check the basic functions directly
    suite.run_test(app_1.normalized_distribution({0: set([1, 2]), 1: set([]), 2: set([])}), {0: 0.3333333333333333, 1: 0.6666666666666666}, "Test #1a: 'normalized_distribution' method")
    suite.run_test(app_1.normalized_distribution({0: set([1]), 1: set([2]), 2: set([1])}), {0: 0.3333333333333333, 1: 0.3333333333333333, 2: 0.3333333333333333}, "Test #1b: 'normalized_distribution' method")
    suite.run_test(app_1.normalized_distribution({0: set([1]), 1: set([0, 2]), 2: set([0, 1])}), {1: 0.3333333333333333, 2: 0.6666666666666666}, "Test #1c: 'normalized_distribution' method")

    # 2. check the basic functions directly
    suite.run_test(app_1.random_digraph(3, 1), {0: set([1, 2]), 1: set([0, 2]), 2: set([0, 1])}, "Test #2a: 'random_digraph' - full probability")  # this should be a COMPLETE GRAPH
    suite.run_test(app_1.random_digraph(4, 0), {0: set([]), 1: set([]), 2: set([]), 3: set([])}, "Test #2b: 'random_digraph' - zero probability")  # this should be a graph with no edges

    # 3. check the basic functions directly
    suite.run_test(app_1.compute_edges({0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1])}), 11, "Test #3a: 'compute_edges' method")
    suite.run_test(app_1.compute_edges({0: set([1]), 1: set([2, 3]), 2: set([1]), 3: set([1])}), 5, "Test #3b: 'compute_edges' method")
    suite.run_test(app_1.compute_edges({0: set([]), 1: set([]), 2: set([]), 3: set([])}), 0, "Test #3c: 'compute_edges' method")

    # 4. Testing basic functionality of the DPA CLASS
    suite.run_test((dpa.DPATrial(3)._node_numbers), [0, 0, 0, 1, 1, 1, 2, 2, 2], "Test #4a: 'self._node_numbers' property")
    suite.run_test((dpa.DPATrial(4)._node_numbers), [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3], "Test #4b: 'self._node_numbers' property")

    # 5. check the DPA methods
    suite.run_test_in_range_multi(dpa.DPATrial(3).run_trial(2), [0, 1, 2], "Test #5a: 'run_trial' method")
    suite.run_test(len(app_1.dpa_stand_alone({0: set([3]), 1: set([0, 2]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}, 6, 4)), 6, "Test #5b: 'dpa_stand_alone' method")

    # 6. check the basic functions directly
    suite.run_test(app_1.merge_data({0: 2, 1: 2, 2: 2}, {0: 4, 1: 2, 2: 1}), {0: 0.5, 1: 1.0, 2: 2.0}, "Test #6a: 'merge_data' property")  # all keys in both dictionaries
    suite.run_test(app_1.merge_data({0: 2, 1: 2, 2: 2, 3: 2}, {0: 4, 2: 1}), {0: 0.5, 2: 2.0}, "Test #6b: 'merge_data' property")  # not all keys in both dictionaries

    # 7. report number of tests and failures
    suite.report_results()


run_suite()
