# -*- encoding: utf-8 -*-
""" Template testing suite for Zombie Apocalypse - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # this imports our testing engine
import _01_ZombieApocalypse as zombie_apocalypse  # this imports the algorithms we are going to test

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


def run_suite(Apocalypse):  # here we only pass a class reference, from which we are going to create an object later on
    """ Some informal testing code """
    print("\nSTARTING TESTS:")
    suite = poc_simpletest.TestSuite() # create a TestSuite object
    apo = Apocalypse(8, 10, [(2, 4), (3, 4), (4, 4)], [(1, 2), (3, 2)], [(1, 6), (3, 6)])  # here we create an object of the class, which functionality we want to test

    # 1. test the initial configuration of the ZOMBIE CLASS using the '__str__' method
    print(apo)  # should print an empty zombie

    # 2. check the basic methods of the ZOMBIE CLASS
    suite.run_test_no_return(apo.clear(), apo._zombie_list, apo._zombie_list == [], "Test #2a: 'clear' method")
    suite.run_test_no_return(apo.clear(), apo._human_list, apo._human_list == [], "Test #2b: 'clear' method")
    print()
    suite.run_test_no_return(apo.add_zombie(1, 2), apo._zombie_list, apo._zombie_list == [(1, 2)], "Test #2c: 'add_zombie' method")
    suite.run_test_no_return(apo.add_zombie(3, 2), apo._zombie_list, apo._zombie_list == [(1, 2), (3, 2)], "Test #2d: 'add_zombie' method")
    suite.run_test_no_return(apo.add_human(1, 6), apo._human_list, apo._human_list == [(1, 6)], "Test #2e: 'add_human' method")
    suite.run_test_no_return(apo.add_human(3, 6), apo._human_list, apo._human_list == [(1, 6), (3, 6)], "Test #2f: 'add_human' method")
    print()
    suite.run_test(apo.num_zombies(), 2, "Test #2g: 'num_zombies' method")
    suite.run_test(apo.num_humans(), 2, "Test #2h: 'num_humans' method")
    print()

    # 3. check the main functions directly: 'compute distance_field'
    obj = Apocalypse(3, 3, [], [], [(2, 2)])
    suite.run_test(obj.compute_distance_field(HUMAN), [[4, 3, 2], [3, 2, 1], [2, 1, 0]], "Test #3: 'compute distance_field' method")

    # 4. check the main functions directly: 'move_humans'
    obj = Apocalypse(3, 3, [], [(2, 2)], [(1, 1)])  # the human should move diagonally from (1, 1) to (0, 0)
    suite.run_test_no_return(obj.move_humans([[4, 3, 2], [3, 2, 1], [2, 1, 0]]), obj._human_list, obj._human_list == [(0, 0)], "Test #4: 'move_humans' method")

    # 5. check the main functions directly: 'move_zombies'
    obj = Apocalypse(3, 3, [(1, 1), (1, 2)], [(2, 2)], [(0, 2)])  # here the zombie and the human are separated by an obstacle to the north, so the zombie has to move along the obstacle to the west
    suite.run_test_no_return(obj.move_zombies([[2, 1, 0], [3, 9, 9], [4, 5, 6]]), obj._zombie_list, obj._zombie_list == [(2, 1)], "Test #5: 'move_zombies' method")

    # 7. report number of tests and failures
    print()
    suite.report_results()


# we run the test with a local 'run_suite' method, to which we pass the CLASS REFERENCE which we are going to test
run_suite(zombie_apocalypse.Apocalypse)  # here we import the ZOMBIE CLASS for testing
