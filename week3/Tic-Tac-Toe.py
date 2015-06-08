# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    players = [provided.PLAYERX, provided.PLAYERO]
    if player == provided.PLAYERX:
        current_player = 0
    else:
        current_plaer = 1
    empty_squares = board.get_empty_squares()
    while len(empty_squares) > 0 and board.check_win() is None:
        index = random.randrange(len(empty_squares))
        (current_row, current_col) = empty_squares[index]
        board.move(current_row, current_col, players[current_player])
        current_player = (current_player + 1) % 2
        empty_squares.remove((current_row, current_col))
    return
    
abc = provided.TTTBoard(3)
mc_trial(abc, provided.PLAYERX)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
