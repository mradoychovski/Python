# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user27_egVNim2eFA_4.py

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("https://www.dropbox.com/s/248bd1dgh9st987/cards.jfitz.png?dl=1")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("https://www.dropbox.com/s/3dwvcdclq9bteau/card_back.png?dl=1")    

# initialize some useful global variables
in_play = False
outcome = ""
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
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
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0],
                           pos[1] + CARD_CENTER[1]], CARD_SIZE)

            
        
# define hand class
class Hand:
    def __init__(self, is_dealer=False):
        # create Hand object
        self.cards = []
        self.is_dealer = is_dealer

    def __str__(self):
        # return a string representation of a hand
        return ' '.join([str(card) for card in cards])

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        aces = False
        hand_value = 0
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                aces = True
        return (hand_value + 10 if aces and (hand_value + 10 <= 21)
                else hand_value)
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i, card in enumerate(self.cards):
            card.draw(canvas, [pos[0] + i*(CARD_SIZE[0] + 3), pos[1]])
        if in_play and self.is_dealer:
            canvas.draw_image(card_back,
                             CARD_BACK_CENTER, CARD_BACK_SIZE,
                             (pos[0] + CARD_BACK_CENTER[0],
                             pos[1] + CARD_BACK_CENTER[1]), CARD_SIZE)

            
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)	# use random.shuffle()

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        return ' '.join([str(card) for card in self.cards])


#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, dealer_score
    if in_play:
        outcome = "YOU LOOSE!"
        dealer_score += 1
    else:
        in_play = True
        outcome = None
        
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand(True)
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    
    in_play = True

def hit():
    global in_play, outcome, dealer_score
    # replace with your code below
    outcome = None
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            in_play = False
            outcome = 'YOU HAVE BUSTED'
            dealer_score += 1
    elif (deck is not None) and (player_hand.get_value() > 21):
        outcome = 'YOU HAVE BUSTED'
        
def stand():
    global in_play, outcome, player_score, dealer_score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())      
    # assign a message to outcome, update in_play and score
        in_play = False
        if dealer_hand.get_value() > 21:
            outcome = 'DEALER HAS BUSTED'
            player_score += 1
        elif 21 >= player_hand.get_value() > dealer_hand.get_value():
            outcome = "YOU WIN!"
            player_score += 1
        elif player_hand.get_value() <= dealer_hand.get_value() <= 21:
            outcome = "YOU LOOSE!"
            dealer_score += 1
           
    elif (deck is not None) and (player_hand.get_value() > 21):
        outcome = 'YOU HAVE BUSTED'
        
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('BLACKJACK', (20, 50), 40, 'Red')
    canvas.draw_text('BLACK', (20, 50), 40, 'Black')
    canvas.draw_text('DEALER', (120, 90), 30, 'Orange')
    canvas.draw_text('PLAYER', (120, 380), 30, 'Orange')
    canvas.draw_line((20, 280),(580, 280), 2, '#555555')
    canvas.draw_line((20, 330), (580, 330), 2, '#555555')
    canvas.draw_polygon([(97, 397), (108 + CARD_SIZE[0]*2, 397),
                         (108 + CARD_SIZE[0]*2, 405 + CARD_SIZE[1]),
                         (97, 405 + CARD_SIZE[1])], 3, '#888888')
    msg = ('Hit or Stand?' if in_play
         else 'NEW DEAL?')
    canvas.draw_text(msg, ((600 - frame.get_canvas_textwidth(msg, 40))/2.0, 320), 40, '#222222')
    if outcome is not None:
        canvas.draw_text(outcome,
            ((600 - frame.get_canvas_textwidth(outcome, 40))/2.0, 270), 40, 'White')
    if deck is not None:
        msg1 = 'Score: %d | %d' % (dealer_score, player_score)
        canvas.draw_text(msg1,
                         (600 - frame.get_canvas_textwidth(msg1, 40) - 20, 50), 40, '#111111')
        dealer_hand.draw(canvas, [100, 110])
        player_hand.draw(canvas, [100, 400])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric