# -*- encoding: utf-8 -*-
""" MERGE - Merge function for 2048 game: adds the same digits and removes zeroes """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_vCzpSt1yr2_3.py


def merge(line):
    """ Function that merges a single row or column in 2048. """

    # create a copy of the list that is going to be modified
    merged_list = list(line)

    # move all zero's to the end of the list
    for zero_num in line:
        if zero_num == 0:
            merged_list.append(0)  # we need to keep the same amount of 'append' and 'remove' so the total amount of elements remain the same
            merged_list.remove(0)

    # merge numbers in merged_list
    for number in range(len(merged_list) - 1):
        if merged_list[number] != 0:
            if merged_list[number] == merged_list[number + 1]:
                merged_list[number] *= 2
                merged_list.pop(number + 1)
                merged_list.append(0)

    return merged_list


print(merge([2, 4, 4, 2, 2]))  # [2, 8, 4, 0, 0]  # these two functions should output the same value
print(merge([0, 4, 16, 16]))  # [4, 32, 0, 0]
