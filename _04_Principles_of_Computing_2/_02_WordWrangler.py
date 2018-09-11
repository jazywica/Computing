# -*- encoding: utf-8 -*-
""" Word Wrangler game. Choose a word and then guess other words that can be made from its letters """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_pbqKOi55Y5_14.py

import urllib2  # standard Python2 module for working with files over the network
# import urllib.request as urllib2  # the urllib2 module has been split across several modules in Python 3 named urllib.request and urllib.error. The 2to3 tool will automatically adapt imports when converting your sources to Python3
import poc_wrangler_provided as provided
try:
    import codeskulptor
except ImportError:
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor


WORDFILE = "assets_scrabble_words3.txt"

# Important: None of these functions should mutate their inputs. You must leave the inputs as they are and return new lists.
# 1. Functions to manipulate ordered word lists
def remove_duplicates(list1):
    """ Eliminate duplicates in a sorted list. Returns a new sorted list with the same elements in list1, but with no duplicates. This function can be iterative. """
    if not list1:  # this is just for empty list
        return []

    no_duplicates = [list1[0]]  # we start by copying the first element, as we need it anyway
    for item in list1[1:]:  # now we walk through the remaining elements and compare it to the last stored elemnt in the new list
        if item != no_duplicates[-1]:
            no_duplicates.append(item)
    return no_duplicates


def intersect(list1, list2):
    """ Compute the intersection of two sorted lists. Returns a new sorted list containing only elements that are in both list1 and list2. This function can be iterative. """
    intersection = []
    index = 0
    for item in list1:
        while index < len(list2) and list2[index] <= item:
            if item == list2[index]:
                intersection.append(item)
            index += 1
    return intersection

def intersect_recursive(list1, list2):
    """ Compute the intersection of two sorted lists. Returns a new sorted list containing only elements that are in both list1 and list2. This function can be iterative. """
    if not list1 or not list2:
        return []  # we start turning back with an empty list as soon as one of the lists come to an end
    else:
        if list1[0] == list2[0]:  # this is the case where the first elements match so we are going to store them and go deeper equally on both lists
            return [list1[0]] + intersect_recursive(list1[1:], list2[1:])  # this is the only place where we add an item (identical item) to our empty list
        elif list2[0] > list1[0]:
            return intersect_recursive(list1[1:], list2)  # in this, and the case below, we are going deeper on one of the lists amd just pass on the list with the results
        else:
            return intersect_recursive(list1, list2[1:])


# 2. Functions to perform merge sort
def merge(list1, list2):
    """ Merge two sorted lists. Returns a new sorted list containing those elements that are in either list1 or list2. Iterative version. """
    temp1 = list(list1)
    temp2 = list(list2)
    merged_list = []

    while temp1 and temp2:  # we stop the main loop as soon as one of the lists are empty,the other list has bigger numbers and we can just glue it to the end
        if temp1[0] <= temp2[0]:  # the "<=" means that when we have duplicates, we will first take it from the list number 1
            merged_list.append(temp1.pop(0))
        else:
            merged_list.append(temp2.pop(0))

    return merged_list + temp1 + temp2  # here we glue the remaining numbers form either of the lists to the end

def merge_recursive(list1, list2):
    """ Merge two sorted lists. Returns a new sorted list containing those elements that are in either list1 or list2. Recursive version. """
    if not list1 or not list2:  # we start the BASE CASE when one of the lists is empty
        return list1 + list2  # here, where we start creating our MERGED LIST from the biggest remaining numbers in either of the lists
    else:
        if list1[0] <= list2[0]:  # the "<=" means that when we have duplicates, we will first take it from the list number 1
            return [list1[0]] + merge_recursive(list1[1:], list2)  # we call recursively again the same funciton, but we shrink the list with the smaller element
        else:
            return [list2[0]] + merge_recursive(list1, list2[1:])


def merge_sort(list1):
    """ DIVIDE AND CONQUER : Sort the elements of list1. Return a new sorted list with the same elements as list1. This function should be recursive. """
    if len(list1) < 2:  # we start the BASE CASE where there is only one element left.
        return list1

    mid = len(list1) // 2  # this is the mid point, where we are going to divide the list
    left = merge_sort(list1[:mid])  # this will take the list down to a single element and then go up to the beginning
    right = merge_sort(list1[mid:])  # this will kick off at the bottom-left, where there is either 0 or 1 element, and will go up together with 'left'
    return merge(left, right)  # this is going to merge the ALREADY SORTED 'left' and 'right'


# 3. Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """ Generate all strings that can be composed from the letters in word in any order. Returns a list of all strings that can be formed from the letters in word. This function should be recursive. """
    if not word:
        return [""]
    else:
        first = word[0]
        rest_strings = gen_all_strings(word[1:])  # this is a recursive call in order to dive all the way to the last letter and then process everything on the way to front
        all_strings = []  # we are going to need an extra list to add all the possibilities

        for item in rest_strings:  # this loop goes through all the collected items during the recursive process
            for index in range(len(item) + 1):  # this lop will move through the item and will stick the first
                all_strings.append(item[:index] + first + item[index:])  # this is the key part, if the item='on' and first='h' then by moving the index we can put 'h' everywhere to get: 'hon', 'ohn', 'onh']
        return rest_strings + all_strings  # this is where we merge the results from previous recursion with the current ones


# 4. Function to load words from a file
def load_words(filename):
    """ Load word list from the file named filename. Returns a list of strings. """
    url = codeskulptor.file2url(WORDFILE)  # this is just a feature of the CODESCULPTOR of creating an url: 'http://codeskulptor-examples.commondatastorage.googleapis.com/examples_files_dracula.txt' in this case
    netfile = urllib2.urlopen(url)  # this will download the file from the internet
    # netfile = open(WORDFILE, "r+")  # this reads the file from the hard drive
    words = [word[:-1] for word in netfile.readlines()]  # this is for Python2, 'word[:-1]' is for removing CrLf at the end
    return words


def run():
    """ Run game. """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, intersect, merge_sort, gen_all_strings)
    provided.run_game(wrangler)


# Uncomment when you are ready to try the game
run()
