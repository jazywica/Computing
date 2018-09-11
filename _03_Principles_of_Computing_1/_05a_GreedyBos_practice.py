# -*- encoding: utf-8 -*-
""" Simulator for greedy boss scenario: Incrementing salary by making bribes """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_oVlrvF97EJ_2.py

import math
try:
    import simpleplot  # access to plotting module
    import codeskulptor
    codeskulptor.set_timeout(20)
except ImportError:
    import SimpleGUICS2Pygame.simpleplot as simpleplot  # CodeSkulptor plotting module stand alone version - 'simpleplot._block()' required to prevent the plotting window from disappearing


# possible plot types
STANDARD = True
LOGLOG = False

# constants for simulation
INITIAL_SALARY = 100
SALARY_INCREMENT = 100
INITIAL_BRIBE_COST = 1000


def greedy_boss(days_in_simulation, bribe_cost_increment, plot_type=STANDARD):
    """ Simulation of greedy boss. Arguments: (number of days in the simulation, amount by which the boss increases the cost of a bribe after each bribe, constant value STANDARD or LOGLOG) """
    # initialize necessary local variables
    current_day = 0
    current_savings = 0  # 'current_savings' and 'total_salary_earned' have to be split, as: '...total salary earned should include money spent on the current day's bribe as well as all previous bribes.'
    total_salary_earned = 0
    current_bribe_cost = INITIAL_BRIBE_COST
    current_salary = INITIAL_SALARY

    # define  list consisting of days vs. total salary earned for analysis
    days_vs_earnings = []

    # Each iteration of this while loop simulates one bribe
    while current_day <= days_in_simulation:
        # update list with days vs total salary earned - use plot_type to control whether regular or log/log plot
        if plot_type == STANDARD:
            days_vs_earnings.append((current_day, total_salary_earned))
        elif current_day != 0:  # we can't take a LOG of a 0 or negative number, so the first case of the LOGLOG graph has to go here
            days_vs_earnings.append([math.log(current_day), math.log(total_salary_earned)])

        # check whether we have enough money to bribe without waiting
        if current_savings >= current_bribe_cost:
            days_to_next_bribe = 0
        else:
            days_to_next_bribe = int(math.ceil((current_bribe_cost - current_savings) / float(current_salary)))  # we have to round the number up (math.ceil) for us to work, as the standard cast 'int()' will round it down

        # advance current_day to day of next bribe (DO NOT INCREMENT BY ONE DAY as it its inefficient)
        current_day += days_to_next_bribe

        # update state of simulation to reflect bribe - note that this part will never be displayed if the remaining days are shorter than the days remaining to the next bribe
        current_savings += days_to_next_bribe * current_salary  # this will increase the salary by the old amounts
        current_savings -= current_bribe_cost  # and then correct it by the bribe
        total_salary_earned += days_to_next_bribe * current_salary  # we have to split this from the total salary, just because we are operating on savings and need to display the whole amount for the graphs
        current_bribe_cost += bribe_cost_increment
        current_salary += SALARY_INCREMENT

    return days_vs_earnings  # this is a list of lists: [2.302585092994046, 6.907755278982137], []], it is designed to display data in simpleplot with a pair of x and y


def run_simulations():
    """ Run simulations for several possible bribe increments """
    plot_type = LOGLOG  # we choose the logarithmic plot
    days = 70
    inc_0 = greedy_boss(days, 0, plot_type)
    inc_500 = greedy_boss(days, 500, plot_type)
    inc_1000 = greedy_boss(days, 1000, plot_type)
    inc_2000 = greedy_boss(days, 2000, plot_type)
    simpleplot.plot_lines("Greedy boss", 600, 600, "days", "total earnings", [inc_0, inc_500, inc_1000, inc_2000], False, ["Bribe increment = 0", "Bribe increment = 500", "Bribe increment = 1000", "Bribe increment = 2000"])
    simpleplot._block()

run_simulations()  # this is a separate function that plots several different scenarios

print greedy_boss(35, 1000)
# should print [(0, 0), (10, 1000), (16, 2200), (20, 3400), (23, 4600), (26, 6100), (29, 7900), (31, 9300), (33, 10900), (35, 12700)]

print greedy_boss(35, 0)
# should print [(0, 0), (10, 1000), (15, 2000), (19, 3200), (21, 4000), (23, 5000), (25, 6200), (27, 7600), (28, 8400), (29, 9300), (30, 10300), (31, 11400), (32, 12600), (33, 13900), (34, 15300), (34, 15300), (35, 16900)]
