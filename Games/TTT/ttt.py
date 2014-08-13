"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 1000    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 2.0  # Score for squares played by the other player


def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    The function play a game starting with the given player by
    making random moves, alternating between players.
    The function return when the game is over.
    The modified board will contain the state of the game,
    so the function does not return anything.
    """
    while len(board.get_empty_squares()) >= 1:
        choice = random.choice(board.get_empty_squares())
        board.move(choice[0], choice[1], player)
        player = provided.switch_player(player)
        if board.check_win() != None:
            break


def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists)
    with the same dimensions as the Tic-Tac-Toe board,
    a board from a completed game, and which player the machine player is.
    The function should score the completed board and
    update the scores grid. As the function updates
    the scores grid directly, it does not return anything,
    """
    for row in range(len(scores)):
        for col in range(len(scores[0])):
            if board.check_win() == player:
                if board.square(row, col) == player:
                    scores[row][col] += MCMATCH
                elif board.square(row, col) == \
                        provided.switch_player(player):
                    scores[row][col] -= MCOTHER
            elif board.check_win() == provided.switch_player(player):
                if board.square(row, col) == player:
                    scores[row][col] -= MCMATCH
                elif board.square(row, col) == \
                        provided.switch_player(player):
                    scores[row][col] += MCOTHER


def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores.
    The function should find all of the empty squares with the maximum
    score and randomly return one of them as a (row, column) tuple.
    It is an error to call this function with a board
    that has no empty squares (there is no possible next move),
    so your function may do whatever it wants in that case.
    The case where the board is full will not be tested.
    """
    empty_squares = board.get_empty_squares()
    max_score = max([scores[empty[0]][empty[1]] for empty in empty_squares])
    best = []
    for empty in empty_squares:
        if max_score == scores[empty[0]][empty[1]]:
            best.append(empty)
    if len(best) == 1:
        return best[0]
    best.pop(best.index(random.choice(best)))
    return random.choice(best)


def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is,
    and the number of trials to run. The function use the Monte Carlo
    simulation described above to return a move for
    the machine player in the form of a (row, column) tuple.
    Be sure to use the other functions you have written!
    """
    scores = [[0.0] * board.get_dim()] * board.get_dim()
    for dummy_trial in range(trials):
        clone = board.clone()
        mc_trial(clone, player)
        mc_update_scores(scores, clone, player)
    return get_best_move(board, scores)

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

