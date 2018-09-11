# -*- encoding: utf-8 -*-
""" Template testing suite for Word Wrangler - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest # this imports our testing engine
import _02_WordWrangler as wrangler # this imports the algorithms we are going to test
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"

def run_suite(WordWrangler): # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    print("\nSTARTING TESTS:")
    suite = poc_simpletest.TestSuite() # create a TestSuite object

    # 1. check the main functions directly: 'remove_duplicate
    suite.run_test(wrangler.remove_duplicates([]), [], "Test #1a: 'remove_duplicate' method")
    suite.run_test(wrangler.remove_duplicates([1, 2, 3, 4, 4, 4]), [1, 2, 3, 4], "Test #1b: 'remove_duplicate' method")
    suite.run_test(wrangler.remove_duplicates([1, 1, 1, 1, 2, 3, 3, 3, 3, 4]), [1, 2, 3, 4], "Test #1c: 'remove_duplicate' method")

    # 2. check the main functions directly: 'intersect'
    suite.run_test(wrangler.intersect([1, 2, 3, 4, 5], [0, 2, 6]), [2], "Test #2a: 'intersect' method")
    suite.run_test(wrangler.intersect([5], [0, 1, 2, 3, 4, 5, 6]), [5], "Test #2b: 'intersect' method")
    suite.run_test(wrangler.intersect([3, 4, 5], [3, 4, 5]), [3, 4, 5], "Test #2c: 'intersect' method")

    # 3. check the main functions directly: 'merge'
    suite.run_test(wrangler.merge([1, 2, 4, 5], [3]), [1, 2, 3, 4, 5], "Test #3a: 'merge' method")
    suite.run_test(wrangler.merge([4, 5], [0, 1, 2, 3, 4, 5, 6]), [0, 1, 2, 3, 4, 4, 5, 5, 6], "Test #3b: 'merge' method")
    suite.run_test(wrangler.merge([], [3, 4, 5]), [3, 4, 5], "Test #3c: 'merge' method")

    # 4. check the main functions directly: 'merge_sort'
    suite.run_test(wrangler.merge_sort([]), [], "Test #4a: 'merge_sort' method")
    suite.run_test(wrangler.merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5], "Test #4b: 'merge_sort' method")
    suite.run_test(wrangler.merge_sort([0, 7, 1, 2, 3, 4, 4, 5, 5, 6]), [0, 1, 2, 3, 4, 4, 5, 5, 6, 7], "Test #4c: 'merge_sort' method")
    suite.run_test(wrangler.merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5], "Test #4d: 'merge_sort' method")

    # 5. check the main functions directly: 'merge_sort'
    suite.run_test(wrangler.load_words(WORDFILE)[0], "aa","Test #5a: 'merge_sort' method - checking first element")
    suite.run_test(wrangler.load_words(WORDFILE)[-1], "zyzzyvas", "Test #5b: 'merge_sort' method - checking last element")

    # 6. report number of tests and failures
    print()
    suite.report_results()


# we run the test with a local 'run_suite' method, to which we pass the CLASS REFERENCE which we are going to test
run_suite(provided.WordWrangler) # here we import the WordWrangler for testing
