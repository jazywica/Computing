# -*- encoding: utf-8 -*-
""" A simple Minimax recursive solver for Nim. http://en.wikipedia.org/wiki/Nim#The_21_game """


MAX_REMOVE = 3  # this is the max amount of digits that a player can remove

# 1. Recursive solver with no memoization
def evaluate_position(current_num):
    """ Recursive solver for Nim """
    global counter
    counter += 1
    for removed_num in range(1, min(MAX_REMOVE + 1, current_num + 1)):  # we scan everything from 1 to whatever is smaller on the upper range(either the max possible move or whatever is left)
        new_num = current_num - removed_num
        print "Current range is from 1 to:", min(MAX_REMOVE, current_num), ", Current number: ", current_num, "New number: ", new_num
        if evaluate_position(new_num) == "lost":  # if we manage to get the previous number to 'lost' our number then will be 'won'
            print "returned won"
            return "won"

    print "returned lost"
    return "lost"  # we return "lost" to indicate that the opponent has just made the winning move of removing all of the remaining items. When we run out of 'remove_num' and don't get 'won' we return 'lost'

def run_standard(items):
    """ Encapsulate code to run regular recursive solver """
    global counter
    counter = 0
    print
    print "Standard recursive version"
    print "Position with", items, "items is", evaluate_position(items)
    print "Evaluated in", counter, "calls"


run_standard(4)


# 2. Memoized version with dictionary
def evaluate_memo_position(current_num, memo_dict):
    """ Memoized version of evaluate_position memo_dict is a dictionary that stores previously computed results """
    global counter
    counter += 1
    for removed_num in range(1, min(MAX_REMOVE + 1, current_num + 1)):
        new_num = current_num - removed_num
        if new_num in memo_dict.keys():  # this is basically the same as the standard version, but here we only check if the new level we are going to enter is already in the dictionary
            if memo_dict[new_num] == "lost":  # this is the most important part, here we check if by any combination of numbers we can get to 'lost' so we can actually win
                memo_dict[current_num] = "won"  # if the level below is 'lost' then we 'won' and we have to put it in the dictionary
                return "won"
        else:
            if evaluate_memo_position(new_num, memo_dict) == "lost":  # this is where the recursion will happen, just as in the standard version we are goint to dive all the way to 0 here
                memo_dict[current_num] = "won"
                return "won"

    memo_dict[current_num] = "lost"  # this is where we return 'lost' if we couldn't get to it in the current round, but in this version it is not going to be used for new_num = 0 as we declare it in the dictionary
    return "lost"


def run_memoized(items):
    """ Run the memoized version of the solver """
    global counter
    counter = 0
    print
    print "Memoized version"
    print "Position with", items, "items is", evaluate_memo_position(items, {0: "lost"})
    print "Evaluated in", counter, "calls"


run_memoized(4)
