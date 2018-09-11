# -*- encoding: utf-8 -*-
""" Template testing suite for Application_2 - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # imports testing engine
import _04_Application_2 as app_2  # imports the algorithms we are going to test
import alg_upa_trial as upa
import alg_module2_graphs as test_graphs  # http://storage.googleapis.com/codeskulptor-alg/alg_module2_graphs.py


def run_suite(): # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    print("\nSTARTING TESTS:")
    suite = poc_simpletest.TestSuite()  # create a TestSuite object

    # 1. check the provided functions directly
    suite.run_test(app_2.targeted_order({0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}), [0, 1, 2, 3], "Test #1a: 'targeted_order' method")  # all nodes are of same degree so returned the nodes from 0 to 3
    suite.run_test(app_2.targeted_order({0: set([3]), 1: set([2, 3]), 2: set([1, 3]), 3: set([0, 1, 2])}), [3, 1, 0, 2], "Test #1b: 'targeted_order' method")  # after deleting node 3 and 1 there are only empty nodes left

    # 2. check the basic functions directly
    suite.run_test(app_2.random_ugraph(4, 1), {0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}, "Test #2a: 'random_digraph' method")
    suite.run_test(app_2.random_ugraph(4, 0), {0: set([]), 1: set([]), 2: set([]), 3: set([])}, "Test #2b: 'random_digraph' method")

    suite.run_test(app_2.compute_edges({0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}), 6, "Test #2c: 'compute_edges' method")
    suite.run_test(app_2.compute_edges({0: set([1, 2, 3, 4]), 1: set([0, 2, 3, 4]), 2: set([0, 1, 3, 4]), 3: set([0, 1, 2, 4]), 4: set([0, 1, 2, 3])}), 10,  "Test #2d: 'compute_edges' method")
    suite.run_test(app_2.compute_edges({0: set([1, 2, 3, 4, 5]), 1: set([0, 2, 3, 4, 5]), 2: set([0, 1, 3, 4, 5]), 3: set([0, 1, 2, 4, 5]), 4: set([0, 1, 2, 3, 5]), 5: set([0, 1, 2, 3, 4])}), 15, "Test #2e: 'compute_edges' method")

    # 3. Testing basic functionality of the UPA CLASS
    suite.run_test(upa.UPATrial(3)._node_numbers, [0, 0, 0, 1, 1, 1, 2, 2, 2], "Test #3a: 'self._node_numbers' property")
    suite.run_test(upa.UPATrial(4)._node_numbers, [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3], "Test #3b: 'self._node_numbers' property")

    suite.run_test_in_range_multi(upa.UPATrial(3).run_trial(2), [0, 1, 2], "Test #3c: 'run_trial' method")

    # 4. check the basic functions directly
    suite.run_test(len(app_2.UPA(4, 2)), 4, "Test #4a: 'UPA' method")  # here we just check if we get the total 'n' amount of nodes
    suite.run_test(len(app_2.random_order({0: set([]), 1: set([]), 2: set([]), 3: set([])})), 4, "Test #4b: 'random_order' method")

    # 5. check the basic functions directly
    suite.run_test(app_2.targeted_order_fast({0: set([3]), 1: set([2, 3]), 2: set([1, 3]), 3: set([0, 1, 2])}), [3, 1, 0, 2], "Test #5a: 'targeted_order_fast' method")
    suite.run_test(app_2.targeted_order_fast(test_graphs.GRAPH2), [1, 3, 5, 7, 8, 2, 4, 6], "Test #5b: 'targeted_order_fast' method")
    suite.run_test(app_2.targeted_order_fast(test_graphs.GRAPH5), ['banana', 'dog', 'cat', 'monkey', 'ape'], "Test #5c: 'targeted_order_fast' method")
    suite.run_test(app_2.targeted_order_fast(test_graphs.GRAPH8), app_2.targeted_order(test_graphs.GRAPH8), "Test #5d: 'targeted_order_fast' method")
    suite.run_test(app_2.targeted_order_fast(test_graphs.GRAPH9), app_2.targeted_order(test_graphs.GRAPH9), "Test #5e: 'targeted_order_fast' method")
    suite.run_test(app_2.targeted_order_fast(test_graphs.GRAPH10), app_2.targeted_order(test_graphs.GRAPH10), "Test #5f: 'targeted_order_fast' method")
    suite.run_test(app_2.targeted_order_fast(test_graphs.GRAPH10), app_2.targeted_order(test_graphs.GRAPH10), "Test #5g: 'targeted_order_fast' method")

    # 6. report number of tests and failures
    suite.report_results()


run_suite()
