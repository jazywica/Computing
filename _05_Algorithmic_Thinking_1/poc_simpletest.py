# -*- encoding: utf-8 -*-
"""
Lightweight testing class inspired by unittest from Pyunit 'https://docs.python.org/2/library/unittest.html'
Note that code is designed to be much simpler than unittest and does NOT replicate unittest functionality
"""

class TestSuite:
    """ Create a suite of tests similar to unittest """
    def __init__(self):
        """ Creates a test suite object """
        self.total_tests = 0
        self.failures = 0

    def run_test(self, computed, expected, message=""):
        """ Compare computed and expected. If not equal, print message, computed, expected """
        self.total_tests += 1
        if computed != expected:
            msg = message + " Computed: " + str(computed) + " Expected: " + str(expected)
            print(msg)
            self.failures += 1

    def run_test_in_range(self, computed, expected, message=""):
        """ Compare computed and expected. If not in a given range of expected values, print message, computed, expected """
        self.total_tests += 1
        if computed not in expected:
            msg = message + " Computed: " + str(computed) + " Expected: " + str(expected)
            print(msg)
            self.failures += 1

    def run_test_in_range_multi(self, computed, expected, message=""):
        """ Compare computed and expected. If not in a given range of expected values, print message, computed, expected """
        self.total_tests += 1
        for item in computed:
            if item not in expected:
                msg = message + " Computed: " + str(computed) + " Expected: " + str(expected)
                print(msg)
                self.failures += 1
                break

    def run_test_no_return(self, function, property, condition, message=""):
        """ Compare computed and expected. If the condition is not fulfilled, then print message, computed, expected """
        self.total_tests += 1
        f = function
        if not condition: # here we just check if our condition is true
            msg = message + " New value: " + str(property) + " Test result: " + str(condition)
            print(msg)
            self.failures += 1

    def report_results(self):
        """ Report back summary of successes and failures from run_test() """
        msg = "Ran " + str(self.total_tests) + " tests. " + str(self.failures) + " failures."
        print(msg)