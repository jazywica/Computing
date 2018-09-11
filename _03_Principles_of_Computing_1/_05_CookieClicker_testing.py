# -*- encoding: utf-8 -*-
""" Template testing suite for Cookie Clicker - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # this imports our testing engine
import _05_CookieClicker as clicker  # this imports the algorithms we are going to test
import poc_clicker_provided as provided


def run_suite(ClickerState):  # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    print("\nSTARTING TESTS:")
    suite = poc_simpletest.TestSuite()  # create a TestSuite object
    state = ClickerState()  # here we create an object of the class, which functionality we want to test

    # 1. test the initial configuration of the state class using the '__str__' method
    print(state)  # should print an empty state

    # 2. check the basic methods of the state CLASS
    state._cps = 2.2
    suite.run_test(state.time_until(5), 3.0, "Test #2a: 'time_until' method")
    suite.run_test(state.time_until(9), 5.0, "Test #2b: 'time_until' method")
    print()
    state._time = 10.0; state._total_cookies = 100.0; state._current_cookies = 10.0
    suite.run_test_no_return(state.wait(78), state._time, state._time == 88, "Test #2c: 'wait' method")
    state._time = 10.0; state._total_cookies = 100.0; state._current_cookies = 10.0
    suite.run_test_no_return(state.wait(78), state._current_cookies, state._current_cookies == 181.6, "Test #2d: 'wait' method")
    state._time = 10.0; state._total_cookies = 100.0; state._current_cookies = 10.0
    suite.run_test_no_return(state.wait(78), state._total_cookies, state._total_cookies == 271.6, "Test #2e: 'wait' method")
    print()
    state._cps = 2.2; state._current_cookies = 66.0; state._history = [(0.0, None, 0.0, 0.0)]
    suite.run_test_no_return(state.buy_item("test_item", 65, 0.5), state._cps, state._cps == 2.7, "Test #2f: 'wait' method")
    state._cps = 2.2; state._current_cookies = 66.0; state._history = [(0.0, None, 0.0, 0.0)]
    suite.run_test_no_return(state.buy_item("test_item", 65, 0.5), state._current_cookies, state._current_cookies == 1.0, "Test #2g: 'wait' method")
    state._cps = 2.2; state._current_cookies = 66.0; state._history = [(0.0, None, 0.0, 0.0)]
    suite.run_test_no_return(state.buy_item("test_item", 65, 0.5), state._history, state._history == [(0.0, None, 0.0, 0.0), (88.0, 'test_item', 65, 271.6)], "Test #2h: 'wait' method")

    # 3. extra check from the OWL TEST
    obj = ClickerState(); obj.wait(78.0); obj.buy_item('item', 1.0, 1.0)
    suite.run_test(obj.time_until(22.0), 0.0, "Test #3: 'combined OWL TEST")  # expected 0.0 but received: "(Exception: Returned Type Mismatch) Expected type 'float' but returned type 'int'."

    # 4. check the main functions directly: 'simulate_clicker'
    clicker.simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16.0, clicker.strategy_cursor_broken)  # expected obj: Time: 16.0 Current Cookies: 13.9125 CPS: 151.0 Total Cookies: 66.0 History [.., (16.0, 'Cursor', 19.837499999999999, 66.0)]
    # print(state)

    # 5. check the strategy functions directly
    suite.run_test(clicker.strategy_cheap(2999, 0, 0, 0, provided.BuildInfo()), 'Cursor', "Test #5a: 'strategy_cheap'")
    suite.run_test(clicker.strategy_cheap(14, 0, 0, 0, provided.BuildInfo()), None, "Test #5b: 'strategy_cheap'")
    suite.run_test(clicker.strategy_cheap(1.0, 3.0, [(0.0, None, 0.0, 0.0)], 17.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)), 'A', "Test #5c: 'strategy_cheap'")

    suite.run_test(clicker.strategy_expensive(1666666, 0, 0, 0, provided.BuildInfo()), 'Portal', "Test #5e: 'strategy_expensive'")
    suite.run_test(clicker.strategy_expensive(1.0, 3.0, [(0.0, None, 0.0, 0.0)], 17.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)), 'A', "Test #5d: 'strategy_expensive'")

    # 7. report number of tests and failures
    print()
    suite.report_results()


# we run the test with a local 'run_suite' method, to which we pass the CLASS REFERENCE which we are going to test
run_suite(clicker.ClickerState)  # here we import the state class for testing
