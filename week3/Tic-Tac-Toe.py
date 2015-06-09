"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.


def mc_trial(board, player):
    '''
    This function takes a current board and the next player to move. The function should
    play a game starting with the given player by making random moves, alternating between
    players. The function should return when the game is over. The modified board will contain
    the state of the game, so the function does not return anything. In other words, the function
    should modify the board input.
    '''
    players = [provided.PLAYERX, provided.PLAYERO]
    if player == provided.PLAYERX:
        current_player = 0
    else:
        current_player = 1
    empty_squares = board.get_empty_squares()
    while len(empty_squares) > 0 and board.check_win() is None:
        index = random.randrange(len(empty_squares))
        (current_row, current_col) = empty_squares[index]
        board.move(current_row, current_col, players[current_player])
        current_player = (current_player + 1) % 2
        empty_squares.remove((current_row, current_col))
    return

def mc_update_scores(scores, board, player):
    '''
        This function takes a grid of scores (a list of lists) with the same dimensions as
        the Tic-Tac-Toe board, a board from a completed game, and which player the machine
        player is. The function should score the completed board and update the scores grid.
        As the function updates the scores grid directly, it does not return anything.
    '''

    # if it is a tie do not need to do anything
    if board.check_win() == provided.DRAW:
        return
    # if this player is the winner
    if board.check_win() == player:
        for row in range(len(scores)):
            for col in range(len(scores[row])):
                if board.square(row, col) != provided.EMPTY:
                    scores[row][col] += SCORE_CURRENT if board.square(row, col) == player else -SCORE_OTHER
    # if if this player is losing the game
    else:
        for row in range(len(scores)):
            for col in range(len(scores[row])):
                if board.square(row, col) != provided.EMPTY:
                    scores[row][col] += -SCORE_CURRENT if board.square(row, col) == player else SCORE_OTHER


def get_best_move(board, scores):
    '''
    This function takes a current board and a grid of scores. The function should find all
    of the empty squares with the maximum score and randomly return one of them as a (row, column)
    tuple. It is an error to call this function with a board that has no empty squares (there is no
    possible next move), so your function may do whatever it wants in that case. The case where the
    board is full will not be tested.
    '''
    if board.check_win() is not None:
        return
    empty_squares = board.get_empty_squares()
    scores_empty_square = [(scores[row][col], random.random(), row, col) for (row,col) in empty_squares]
    scores_sorted = sorted(scores_empty_square, reverse=True)
    return (scores_sorted[0][2], scores_sorted[0][3])


def mc_move(board, player, trials):
    '''
    This function takes a current board, which player the machine player is, and the number of trials
    to run. The function should use the Monte Carlo simulation described above to return a move for the
    machine player in the form of a (row, column) tuple. Be sure to use the other functions you have written!
    '''
    scores = list()
    for dummy_i in range(board.get_dim()):
        scores.append([0] * board.get_dim())
    for dummy_i in range(trials):
        board_copy = board.clone()
        mc_trial(board_copy, player)
        #print board_copy
        mc_update_scores(scores, board_copy, player)
        #print scores
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
