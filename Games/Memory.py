# implementation of card game - Memory
# http://www.codeskulptor.org/#user23_BwOqhtCYPg_0.py

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, state, turns
    cards = [[i % 8,False] for i in range(16)]
    random.shuffle(cards)
    turns = 0
    state = 0
     
# define event handlers
def mouseclick(pos):
    global cards, state, first_card, second_card, turns
    if pos[1] >= 0 and pos[1] <= 100 and not cards[pos[0] // 50][1]:
        if state == 0:
            state = 1
            first_card = pos[0] // 50
            cards[(pos[0] // 50)][1] = True
            turns += 1
        elif state == 1:
            state = 2
            second_card = pos[0] // 50
            cards[(pos[0] // 50)][1] = True
        elif state == 2:
            state = 1
            if cards[first_card][0] != cards[second_card][0] :
                cards[first_card][1] = False
                cards[second_card][1] = False
            first_card = pos[0] // 50
            cards[pos[0] // 50][1] = True
            turns += 1
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns = %d" % turns)
    for index in range(len(cards)):
        if cards[index][1]:
            canvas.draw_text(str(cards[index][0]), (index*50 + 10, 75), 50, "Red")
        elif not cards[index][1]:
            canvas.draw_polygon([(index*50, 0), ((index+1)*50, 0), ((index+1)*50, 100), (index*50, 100)], 1,"Black", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric