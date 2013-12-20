import simplegui, random, math


# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

# http://www.codeskulptor.org/#user23_jeZ4sopF79_2.py

# initialize global variables used in your code
low, high = 0, 100


# helper function to start and restart the game
def new_game():
    global comp_secret_guess, num_guesses
    num_guesses = int(math.ceil(math.log(high - low + 1, 2)))
    comp_secret_guess = random.randrange(low, high)
    print "New game. Range is from %d to %d" % (low, high)
    print "Number of remaining guesses is", num_guesses
    print ''


# define event handlers for control panel
def range100():
    global low, high
    # button that changes range to range [0,100) and restarts
    low, high = 0, 100
    new_game()

def range1000():
    global low, high
    # button that changes range to range [0,1000) and restarts
    low, high = 0, 1000
    new_game()
    
def input_guess(guess):
    global num_guesses
    # main game logic goes here
    if num_guesses > 1:
        player_guess = int(guess)
        num_guesses -= 1
        print "Guess was ", player_guess
        print "Number of remainig guesses is", num_guesses
        if player_guess > comp_secret_guess:
            print "Your guess is too high."
            print ''
        elif player_guess < comp_secret_guess:
            print "Your guess is too low."
            print ''
        elif player_guess == comp_secret_guess:
            print ''
            print "Corect"
            print "You win!"
            print 'The secret number is', comp_secret_guess
            print ''
            new_game()
    else:
        print "Sorry"
        print "Computer win!"
        print 'The secret number is', comp_secret_guess
        print ''
        new_game()

    
# create frame
game = simplegui.create_frame("Guess the number", 200, 200)


# register event handlers for control elements
game.add_button('Range is [0,100)', range100, 200)
game.add_button('Range is [0,1000)', range1000, 200)
game.add_input('Enter a guess', input_guess, 200)


# call new_game and start frame
new_game()
game.start()

