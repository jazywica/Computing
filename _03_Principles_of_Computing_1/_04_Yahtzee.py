# -*- encoding: utf-8 -*-
""" Planner for Yahtzee with no GUI. Simplifications: only allow discard and roll, only score against upper level """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_PYc5821VfZ_2.py


def gen_all_sequences(outcomes, length):
    """ Iterative function that enumerates the set of all sequences of outcomes of given length. """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):  # (hand: full yahtzee hand)
    """ Compute the maximal score for a Yahtzee hand according to the upper section of the Yahtzee score card. Returns an integer score """
    return 0 if len(hand) == 0 else max([dummy_num * hand.count(dummy_num) for dummy_num in set(hand)])  # thanks to 'set(nums)' we filter the single digits and multiply them by how many times they apper


def expected_value(held_dice, num_die_sides, num_free_dice):  # (held_dice: dice that you will hold, num_die_sides: number of sides on each die, num_free_dice: number of dice to be rolled)
    """ Compute the expected value based on held_dice given that there are num_free_dice to be rolled, each with num_die_sides. Returns a floating point expected value """
    all_seq = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)  # here we generate all sequences for the number of dice we have left
    total_score = sum([score(held_dice + seq) for seq in all_seq])
    return total_score / float(len(all_seq))


def gen_all_holds(hand):  # (hand: full yahtzee hand)
    """ Generate all possible choices of dice from hand to hold. Returns a set of tuples, where each tuple is dice to hold """
    all_holds = set([()])
    for dice in hand:  # the main loop iterates through all dice in hand
        temp = all_holds.copy()  # here we make a copy on which we are going to operate, leaving the main SET behind
        for item in temp:  # Iterate through all items in hold set
            new_seq = list(item)
            new_seq.append(dice)
            all_holds.add(tuple(new_seq))  # Duplicates cannot be added into set
    return all_holds

    # all_holds = [()]  # this is a simplfied version that operates on a main collection, this is not recommended
    # for item in hand:
    #     for subset in all_holds:
    #         all_holds = all_holds + [tuple(subset) + (item,)]
    # return set(all_holds)


def strategy(hand, num_die_sides):  # (hand: full yahtzee hand, num_die_sides: number of sides on each die)
    """ Compute the hold that maximizes the expected value when the discarded dice are rolled. Returns a tuple where the first element is the expected score and the second element is a tuple of the dice to hold """
    max_value = 0
    max_hold = ()
    all_holds = gen_all_holds(hand)
    for hold in all_holds:
        exp_val = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if exp_val > max_value:
            max_value = exp_val
            max_hold = hold

    return (max_value, max_hold)


def run_example():
    """ Compute the dice to hold and expected score for an example hand """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()
