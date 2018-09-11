""" GUESS THE NUMBER - guessing game with hints to help the player """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_OjeNV3SApk_2.py

import random
import math
try:
    import simplegui  # access to drawing operations for interactive applications
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  # CodeSkulptor GUI module stand alone version


# initialize global variables used in your code here
num_range = 100

# helper function to start and restart the game and initialize the necessary messages to display
def new_game():  # one should call new_game() in four places: in each of the two buttons handlers, after a completed game in input_guess()and before frame.start() to initialize the first game
    global secret_number, num_guesses
    secret_number = random.randrange(0, num_range)
    print "New game. Range is [0, " + str(num_range) + ")"
    num_guesses = int(math.log(num_range, 2)) + 1
    print "Number of remaining guesses is " + str(num_guesses)
    print

# define event handlers for control panel
def range100():  #  button that changes the range to [0,100) and starts a new game
    global num_range
    num_range = 100
    new_game()

def range1000():  # button that changes the range to [0,1000) and starts a new game
    global num_range
    num_range = 1000
    new_game()

def input_guess(guess):
    global secret_number, num_guesses
    num_guesses -= 1
    print "Guess was " + guess
    print "Number of remaining guesses is " + str(num_guesses)

    if num_guesses == 0 and int(guess) != secret_number:
        print "You ran out of guesses.  The number was " + str(secret_number)
        print
        new_game()
    elif int(guess) == secret_number:
        print "Correct!"
        print
        new_game()
    elif int(guess) < secret_number:
        print "Higher!"
        print
    elif int(guess) > secret_number:
        print "Lower!"
        print


# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# call new_game
new_game()
frame.start()
