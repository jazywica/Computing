# -*- encoding: utf-8 -*-
""" Cookie Clicker Simulator - analysis for choosing the best strategy """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_YHl0aZhb0i_3.py

import math
import poc_clicker_provided as provided
try:
    import simpleplot  # access to plotting module
    import codeskulptor
    codeskulptor.set_timeout(20)  # Used to increase the timeout, if necessary
except ImportError:
    import SimpleGUICS2Pygame.simpleplot as simpleplot  # CodeSkulptor plotting module stand alone version - 'simpleplot._block()' required to prevent the plotting window from disappearing


# Constants
SIM_TIME = 10000000000.0  # this is the SIMULATION TIME, for testing, we will keep it smaller


class ClickerState:
    """ Simple class to keep track of the game state. """
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]  # Each tuple in the list will contain 4 values: a time, an item that was bought at that time (or None), the cost of the item, and the total number of cookies produced by that time

    def __str__(self):
        """ Return human readable state """
        message = "Curent time       : " + str(self.get_time())+ "\nCurrent cookies   : " + str(self.get_cookies()) + "\nCurrent CPS       : " + str(self.get_cps()) \
                  + "\nTotal cookies     : " + str(self._total_cookies) + "\nHistory last item : " + str(self.get_history()[len(self.get_history()) - 1])
        return message

    def get_cookies(self):
        """ Return current number of cookies(not total number of cookies). *Should return a float """
        return self._current_cookies

    def get_cps(self):
        """ Get current CPS. *Should return a float """
        return self._cps

    def get_time(self):
        """ Get current time. *Should return a float. This method should return the number of seconds you must wait until you will have the given number of cookies"""
        return self._time

    def get_history(self):
        """ Return history list. History list should be a list of tuples of the form: (time, item, cost of item, total cookies) For example: [(0.0, None, 0.0, 0.0)]
        Should return a copy of any internal data structures, so that they will not be modified outside of the class. """
        return list(self._history)  # get_history should return a copy of the history list so that you are not returning a reference to an internal data structure

    def time_until(self, cookies):
        """ Return time until you have the given number of cookies (could be 0.0 if you already have enough cookies). Should return a float with no fractional part """
        if self._current_cookies >= cookies:
            return float(0)
        else:
            # Remember that you cannot wait for fractional seconds, so while you should return a float it should not have a fractional part.
            return float(int(math.ceil((cookies - self._current_cookies) / float(self._cps))))  # we have to round the number up (math.ceil) for us to work, as the standard cast 'int()' will round it down

    def wait(self, time):
        """ Wait for given amount of time and update state. *Should do nothing if time <= 0.0 """
        if time > 0:
            self._time += time
            self._current_cookies += time * self._cps
            self._total_cookies += time * self._cps

    def buy_item(self, item_name, cost, additional_cps):
        """ Buy an item and update state. *Should do nothing if you cannot afford the item """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._history.append(tuple([self._time, item_name, cost, self._total_cookies]))


def simulate_clicker(build_info, duration, strategy):  # Note that simulate_clicker is a higher-order function: it takes a strategy function as an argument!
    """ Function to run a Cookie Clicker game for the given duration with the given strategy. Returns a ClickerState object corresponding to the final state of the game. """
    state = ClickerState()
    build_info_clone = build_info.clone()  # '....The first thing you should do in this function is to make a clone of the build_info object and create a new ClickerState object.'

    while state.get_time() <= duration:
        time_left = duration - state.get_time()
        next_strategy = strategy(state.get_cookies(), state.get_cps(),state.get_history(), time_left, build_info_clone)
        if next_strategy == None:
            state.wait(time_left)
            break
        time_to_buy = state.time_until(build_info_clone.get_cost(next_strategy))
        if time_to_buy > time_left:
            state.wait(time_left)
            break
        state.wait(time_to_buy)
        while state.get_cookies() >= build_info_clone.get_cost(next_strategy):
            state.buy_item(next_strategy, build_info_clone.get_cost(next_strategy), build_info_clone.get_cps(next_strategy))
            build_info_clone.update_item(next_strategy)

    return state


# All strategy functions take the current number of cookies, current CPS, history of purchases in the simulation, amount of time left in the simulation, and a BuildInfo object (even if they don't use these parameters).
def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """ Always pick Cursor! Note that this simplistic (and broken) strategy does not properly check whether it can actually buy a Cursor in the time left. Your simulate_clicker function must be able to deal
    with such broken strategies. Further, your strategy functions must correctly check if you can buy the item in the time left and return None if you can't. """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """ Always return None. This is a pointless strategy that will never buy anything, but that you can use to help debug your simulate_clicker function. """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """ Always buy the cheapest item you can afford in the time left. """
    item_lst = build_info.build_items()
    cost_lst = map(build_info.get_cost, item_lst)

    min_idx = cost_lst.index(min(cost_lst))  # in the cheap strategy we are only pick the smallest value, because if we can't afford it we won't be able to buy anything else
    min_key = item_lst[min_idx]
    if cost_lst[min_idx] <= cookies + cps * time_left:  # 'cookies + cps * time_left' is the total amount of cookies we can get in a given timespan
        return min_key
    else:
        return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """ Always buy the most expensive item you can afford in the time left. """
    item_lst = build_info.build_items()
    cost_lst = map(build_info.get_cost, item_lst)

    maxval = float('-inf')  # in the expensive strategy we are going to chenc the values one by one
    maxkey = None
    for index in range(len(item_lst)):
        if cost_lst[index] > maxval and cost_lst[index] <= cookies + cps * time_left:
            maxval = cost_lst[index]
            maxkey = item_lst[index]
    return maxkey

def strategy_best(cookies, cps, history, time_left, build_info):
    """ The best strategy that you are able to implement. """
    item_lst = build_info.build_items()
    cost_lst = map(build_info.get_cost, item_lst)
    cps_lst = map(build_info.get_cps, item_lst)
    best_ratio = [cps_lst[index] / cost_lst[index] for index in range(len(item_lst))]  # the best strategy is simply a ratio of the upgrade to its cost

    maxval = float('-inf')
    maxkey = None
    for index in range(len(item_lst)):
        if best_ratio[index] > maxval and cost_lst[index] <= cookies + cps * time_left:  # we look for a maximum value based on the best ratio
            maxval = best_ratio[index]
            maxkey = item_lst[index]
    return maxkey


def run_strategy(strategy_name, time, strategy):  # function runs the simulation, prints out the final state of the game after the given time and then plots the total number of cookies over time.
    """ Run a simulation for the given time with one strategy. """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print "Strategy name:", strategy_name
    print(state)  # this line is to print the details of each strategy in the console

    # Plot total cookies over time
    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True); simpleplot._block()


def run():
    """ Run the simulator. """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)


run()
