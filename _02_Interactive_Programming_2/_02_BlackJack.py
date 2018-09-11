# -*- encoding: utf-8 -*-
""" BLACK JACK - Final version for submission - Week 2 """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_f1zeEgpDbr_1.py

import random
try:
    import simplegui  # access to drawing operations for interactive applications
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  # CodeSkulptor GUI module stand alone version


# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define classes
class Card:
    """ Card class - this describes the class for the cards """
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


class Hand:
    """ Hand class - this is responsible for everything that is being held in a hand """
    def __init__(self):
        self.cards_hand = []

    def __str__(self):
        concat = ""
        for card in self.cards_hand:
            concat += card.get_suit() + card.get_rank() + " "
        return "Hand contains " + concat

    def add_card(self, card):
        self.cards_hand.append(card)

    def get_value(self):  # compute the value of the hand. Since there can't be two aces in a row (value = 22) then the best option is to count Ace as 1 and see what happens when we add 10
        self.hand_value = 0
        is_Ace = False
        for card in self.cards_hand:
            self.hand_value += VALUES[card.get_rank()]  # here we look into the 'VALUES' dictionary to compute the initial value, with Aces equal to 1
            if card.rank == "A":
                is_Ace = True

        if not is_Ace:
            return self.hand_value
        else:
            if self.hand_value + 10 <= 21:  # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
                return self.hand_value + 10
            else:
                return self.hand_value

    def draw(self, canvas, pos):  # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.cards_hand:
            card.draw(canvas, [pos[0] + (80 * i), pos[1]])  # this code passes on both canvas and position onto the draw method of the CARD CLASS
            i += 1

class Deck:
    """ Deck class - this is responsible for what happens with the pile of cards on the table """
    def __init__(self):
        self.cards_deck = []
        for i in SUITS:
            for j in RANKS:
                self.cards_deck.append(Card(i, j))

    def shuffle(self):  # shuffle the deck
        return random.shuffle(self.cards_deck)

    def deal_card(self):
        return self.cards_deck.pop(-1)

    def __str__(self):
        concat = ""
        for i in self.cards_deck:
            concat += i.suit + i.rank + " "
        return "Deck contains " + concat


# define event handlers for buttons
def deal():
    global in_play, outcome, message, score, deck, player_hand, dealer_hand
    if in_play:  # this is designed so the player will lose if he tries to deal cards just after they are already dealt
        score -= 1
        message = "You lost the round. New game"
        in_play = False  # this will switch to FALSE automatically so with the next button press the new deal will start
    else:
        deck = Deck()
        player_hand = Hand()
        dealer_hand = Hand()
        deck.shuffle()
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        outcome = "Hit or stand?"
        message = ""
        in_play = True

def hit():
    global in_play, outcome, message, score, player_hand, dealer_hand
    if in_play:  # if the hand is in play, hit the player
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:  # if busted, assign a message to outcome, update in_play and score
            in_play = False
            score -= 1
            message = "You went bust and lose."
            outcome = "New deal?"

def stand():
    global in_play, outcome, message, score, dealer_hand
    if in_play:
        while dealer_hand.get_value() < 17:  # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:  # this is separate, just to display the special message that the dealer went bust
            score += 1
            message = "Dealer went bust. You win."
        elif player_hand.get_value() > dealer_hand.get_value():  # we know already that the player's value is not bust
            score += 1
            message = "You win."
        else:
            score -= 1
            message = "You lose."
        in_play = False
        outcome = "New deal?"

# draw handler
def draw(canvas):
    canvas.draw_text('Blackjack', [70, 80], 40, 'Black')
    canvas.draw_text('Score: ' + str(score), [430, 80], 32, 'Black')
    canvas.draw_text('Dealer:   ' + message, [70, 150], 32, 'White')
    canvas.draw_text('Player:   ' + outcome, [70, 350], 32, 'White')

    dealer_hand.draw(canvas, [70, 180])  # here we only specify the starting point for the hand images fot the HNAD CLASS method
    player_hand.draw(canvas, [70, 380])

    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [70 + CARD_BACK_CENTER[0], 180 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
