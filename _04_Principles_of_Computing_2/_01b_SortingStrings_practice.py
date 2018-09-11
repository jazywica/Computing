# -*- encoding: utf-8 -*-
""" Sorting a list of strings using an alphabetical grid (allocated space for each single letter)"""

import random


# constants
NUM_CHARS = 26  # this number corresponds to the amount of letters we are going to use (a-z)
CHARACTERS = [chr(ord("a") + char_num) for char_num in range(NUM_CHARS)]  # since a-z letters are 97 to 122 in ASCI code, we can add 'char_num' to 'a' and the convert it to a character (ord())
print("This is how the characters a-z look like: " + str(CHARACTERS))


def order_by_letter(string_list, letter_pos):
    """ Takes a list of strings and order them alphabetically using the letter at the specified position """
    buckets = [[] for dummy_idx in range(NUM_CHARS)]  # buckets corresponding to a-z letters: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for string in string_list:
        char_index = ord(string[letter_pos]) - ord("a")  # this is a clever way of finding the INDEX of the letter we are comparing
        buckets[char_index] += [string]  # here we populate the string into the right place according to the letter we currently analyze
        print("Buckets for characters: ", buckets)

    answer = []
    for char_index in range(NUM_CHARS):  # here we just concatenate the strings as they are (from left to right)
        answer += buckets[char_index]  # since they already have been sorted by rightmost letters the current identical letters can just be concatenated
    return answer


def string_sort(string_list, length):  # the function string_sort sorts a list of strings by repeatedly applying order_by_character to the list of strings working from the last letter to the first
    """ Order a list of strings of the specific length in ascending alphabetical order """
    for position in range(length - 1, -1, -1):  # here we sort the strings by one letter at the time, moving from the end to the beginning
        string_list = order_by_letter(string_list, position)  # this is where we pass the sorted (by the previous letter) list to the next sort, thanks to this the order of processing current letter is correct
        print("The current string list: ", string_list)  # this should be printed 3 times (as many as there are letters in the word)
    return string_list


def run_example():
    """ Example of string sort """
    string_length = 3
    test_list = ["".join([random.choice(CHARACTERS) for _ in range(string_length)]) for dummy_index in range(5)]  # this LC creates a randomly generated words made of three letters each
    print("Unsorted string list:", test_list)
    print("Sorted string list:", string_sort(test_list, string_length))  # this is where we call the 'string_sort' procedure

    print("Example with fixed values: \n")
    print("Unsorted string list:", ["ape", "bat", "ant"])  # this list would be reordered to ["ape", "ant", "bat"] (which is wrong) if it was only sorted by the first letter
    print("Sorted string list:", string_sort(["ape", "bat", "ant"], string_length))  # this is where we call the 'string_sort' procedure


run_example()
