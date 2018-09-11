# -*- encoding: utf-8 -*-
""" Analyzing a simple dice game - for 3 rolls of dice we are going to get 10$ for having same number twice and 200$ if it comes 3 times (all times). Else we loose 10$ """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_vMooz6xFHM_0.py


def gen_all_sequences(outcomes, length):
    """ Iterative function that enumerates the set of all sequences of outcomes of given length """
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

def max_repeats(seq):
    """ Compute the maximum number of times that an outcome is repeated in a sequence """
    item_count = [seq.count(item) for item in seq]  # if there are 3 different numbers it retrns: [1, 1, 1], if they are all the same: [3]
    return max(item_count)

def compute_expected_value(outcomes, length):
    """ Function to compute expected value of simple dice game """
    all_rolls = gen_all_sequences(outcomes, length)  # all the possible outcomes to see how often repetitions occur
    possible_rolls = len(all_rolls)  # this number is important for calculating the probability
    results = [max_repeats(roll) for roll in all_rolls]  # this will return a LIST with maximum occurance (in all possible sequences) of the same number: [2, 1, 1, 3, .......1]

    a = len(results)
    expected_value = 0  # we are going to compute the EXPECTED VALUE in dollars, as we want to see is it more likely to gain (at least) 10$ or loose 10$
    for result in results:
        if result == 2:
            expected_value += 10 / float(possible_rolls)  # this is the probability of getting 10$
        elif result == 3:
            expected_value += 200 / float(possible_rolls)  # this is the probability of getting 200$
        # else:  # this is think would give an esimated loss if we played the same amount of times as there were results in the list (216 times)
            # expected_value -= 10
    return expected_value


def run_test():
    """ Testing code, note that the initial cost of playing the game has been subtracted """
    outcomes = set([1, 2, 3, 4, 5, 6])  # the number of 'outcomes' must be at least 3, the 'length' must remain 3
    print "All possible sequences of three dice are:"
    print gen_all_sequences(outcomes, 3)
    print
    print "Test for max repeats"
    print "Max repeat for (3, 1, 2) is", max_repeats((3, 1, 2))
    print "Max repeat for (3, 3, 2) is", max_repeats((3, 3, 2))
    print "Max repeat for (3, 3, 3) is", max_repeats((3, 3, 3))
    print
    print "Ignoring the initial $10, the expected value was $", compute_expected_value(outcomes, 3)
    # function returns approximately $9.72 which is consistent with the game being slightly unfavorable. So, resist the urge to play and learn how to count cards in Blackjack instead.


run_test()
