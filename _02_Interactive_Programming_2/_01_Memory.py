# -*- encoding: utf-8 -*-
""" MEMORY GAME - Final version for submission - Week 1 """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_dX6VwBU3iO_1.py

import random
try:
    import simplegui  # access to drawing operations for interactive applications
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  # CodeSkulptor GUI module stand alone version


def new_game():  # helper function to initialize globals
    global numbers, exposed, state, turns
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    numbers = list(range(0, 8)) + list(range(0, 8))
    random.shuffle(numbers)
    state = 0
    turns = 0
    label.set_text("Turns = " + str(turns))


# define event handlers
def mouseclick(pos):
    global exposed, state, card1, card2, turns
    index = pos[0] // 50
    if not exposed[index]:  # here we exclude all the clicks where the card is already exposed
        exposed[index] = True
        # In this program we are going to update the counter on the first click, as it is more intuitive
        if state == 0:  # 'state0' is just a to start the game
            state = 1
            card1 = index
            turns += 1
            label.set_text("Turns = " + str(turns))
        elif state == 1: # 'state1' is the second click, where we assign 'card2'
            state = 2
            card2 = index
        else:  # 'state2' is the third click, where we check if the numbers are the same, but we also have to acknowledge the click as another 'card1'
            if numbers[card1] != numbers[card2]:
                exposed[card1] = False
                exposed[card2] = False
            card1 = index  # we have to assign the 'card1' to a new card
            state = 1
            turns += 1
            label.set_text("Turns = " + str(turns))


def draw(canvas):  # cards are logically 50x100 pixels in size
    global numbers
    red_rim = 1
    for i in range(len(numbers)):
        if exposed[i]:
            canvas.draw_text(str(numbers[i]), (13 + (i * 50), 65), 50, 'White')
        else:
            canvas.draw_polygon([[i*50, 0], [50 + i*50, 0], [50 + i*50, 100], [i*50, 100]], 1, 'Red', 'Green')
    canvas.draw_polygon([[0, 0], [800 - red_rim, 0], [800 - red_rim, 100 - red_rim], [0, 100 - red_rim]], red_rim, 'Red')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
