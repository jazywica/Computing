""" ROCK-PAPER-SCISSORS-LIZARD-SPOCK - simple game: player vs random computer choice """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_uPVHROOe6b_2.py

# The key idea of this program is to equate the strings "rock", "paper", "scissors", "lizard", "Spock" to numbers as follows:
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random


def name_to_number(name):  # this is a helper function that will convert between NAMES and NUMBERS
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Illegal name"

def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "Illegal number"

def rpsls(player_choice):
    player_number = name_to_number(player_choice)
    computer_number = random.randrange(0, 5)
    computer_choice = number_to_name(computer_number)
    print
    print "Player choose " + player_choice
    print "Computer choose " + computer_choice
    difference = (player_number - computer_number) % 5  # first - second = difference, which we then take modulo 5(total amount of elements) so we only have numbrs 0, 1, 2, 3, 4
    if difference == 1 or difference == 2:  # we have designed the 'wheel' in a way that two elements to the right are win and two to the left is loose...
        print "Player wins!"
    elif difference == 3 or difference == 4:  # so it is easy to split it into 1,2 and 3,4
        print "Computer wins!"
    else:
        print "Player and computer tie!"

		
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
