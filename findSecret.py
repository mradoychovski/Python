def isMyNumber(guess):
    secretNum = -49467865
    if secretNum > guess:
        return -1
    elif secretNum < guess:
        return 1
    else:
        return 0
    
def jumpAndBackpedal(isMyNumber):
    '''
    isMyNumber: Procedure that hides a secret number. 
     It takes as a parameter one number and returns:
     *  -1 if the number is less than the secret number
     *  0 if the number is equal to the secret number
     *  1 if the number is greater than the secret number
 
    returns: integer, the secret number
    '''
    def BSearch(guess):
        global min_guess, max_guess
        
        if isMyNumber(guess) == 0:
            return guess
        
        if (isMyNumber(guess) == -1 and guess > 0) or (isMyNumber(guess) == 1 and guess < 0):
            min_guess = guess
            guess *= 2
        
        elif (isMyNumber(guess) == 1 and guess > 0) or (isMyNumber(guess) == -1 and guess < 0):
            max_guess = guess
            guess = (min_guess + max_guess) / 2
            
        return BSearch(guess)


    guess = 0
    if isMyNumber(guess) == 0:
        return 0
    
    guess = (-1)*isMyNumber(guess)
    return BSearch(guess)  
