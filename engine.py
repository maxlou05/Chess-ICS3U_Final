# ICS3U-01
# Maxwell Lou
# This file contains the logic of the chess engine, which uses piece-square tables to evaluate a position

import copy
from data import *
from helper_functions import *
from get_moves import *

# Function to evaluate the current position
def eval(pieces, turn):
    '''
    This function evaluates how strong a player's pieces are on the current board using piece-square tables retrieved online.
    Args:
        pieces: Dictionary with piece name as key, Piece object as value
        turn: String, white or black's turn
    Returns:
        score: A float detailing how strong the pieces are. 0 means equal, positive means better for the player whose turn it is.
    '''
    piece_val_MG_w = 0
    piece_val_MG_b = 0
    all_val_MG_w = 0
    all_val_MG_b = 0
    all_val_EG_w = 0
    all_val_EG_b = 0
    score_MG_w = 0
    score_EG_w = 0
    score_MG_b = 0
    score_EG_b = 0
    for i in pieces:
        # Count the value of all the pieces on the board
        if(i[0] == 'p'):
            if(i[-1] == 'w'):
                all_val_MG_w += PIECE_VAL_MG['p']
                all_val_EG_w += PIECE_VAL_EG['p']
            else:
                all_val_MG_b += PIECE_VAL_MG['p']
                all_val_EG_b += PIECE_VAL_EG['p']
        if(i[0] == 'n'):
            if(i[-1] == 'w'):
                all_val_MG_w += PIECE_VAL_MG['n']
                all_val_EG_w += PIECE_VAL_EG['n']
                piece_val_MG_w += PIECE_VAL_MG['n']
            else:
                all_val_MG_b += PIECE_VAL_MG['n']
                all_val_EG_b += PIECE_VAL_EG['n']
                piece_val_MG_b += PIECE_VAL_MG['n']
        elif(i[0] == 'b'):
            if(i[-1] == 'w'):
                all_val_MG_w += PIECE_VAL_MG['b']
                all_val_EG_w += PIECE_VAL_EG['b']
                piece_val_MG_w += PIECE_VAL_MG['b']
            else:
                all_val_MG_b += PIECE_VAL_MG['b']
                all_val_EG_b += PIECE_VAL_EG['b']
                piece_val_MG_b += PIECE_VAL_MG['b']
        elif(i[0] == 'r'):
            if(i[-1] == 'w'):
                all_val_MG_w += PIECE_VAL_MG['r']
                all_val_EG_w += PIECE_VAL_EG['r']
                piece_val_MG_w += PIECE_VAL_MG['r']
            else:
                all_val_MG_b += PIECE_VAL_MG['r']
                all_val_EG_b += PIECE_VAL_EG['r']
                piece_val_MG_b += PIECE_VAL_MG['r']
        elif(i[0] == 'q'):
            if(i[-1] == 'w'):
                all_val_MG_w += PIECE_VAL_MG['q']
                all_val_EG_w += PIECE_VAL_EG['q']
                piece_val_MG_w += PIECE_VAL_MG['q']
            else:
                all_val_MG_b += PIECE_VAL_MG['q']
                all_val_EG_b += PIECE_VAL_EG['q']
                piece_val_MG_b += PIECE_VAL_MG['q']
        elif(i[0] == 'k'):
            if(i[-1] == 'w'):
                all_val_MG_w += PIECE_VAL_MG['k']
                all_val_EG_w += PIECE_VAL_EG['k']
            else:
                all_val_MG_b += PIECE_VAL_MG['k']
                all_val_EG_b += PIECE_VAL_EG['k']

        # Count the position score of all pieces based on tables
        # See description in data.py
        if(i[-1] == 'w'):
            score_MG_w += TABLES_MG[i[0]][7 - pieces[i].pos[1]][pieces[i].pos[0]]
            score_EG_w += TABLES_EG[i[0]][7 - pieces[i].pos[1]][pieces[i].pos[0]]
        else:
            score_MG_b += TABLES_MG[i[0]][pieces[i].pos[1]][pieces[i].pos[0]]
            score_EG_b += TABLES_EG[i[0]][pieces[i].pos[1]][pieces[i].pos[0]]

    # Game phase counts the midgame value of pieces (excluding pawns and king) on the board to determine endgame or midgame
    # If value is less than endgame, set it to be endgame, if value is larger than midgame, set it to be midgame
    gamePhase = max(EG_MIN, min(MG_MAX, piece_val_MG_w + piece_val_MG_b))
    # Depending on how much it is a midgame vs endgame, adjust the weights of the different tables
    factor_MG = (gamePhase - EG_MIN) / GAME_PHASE_RANGE
    factor_EG = 1 - factor_MG

    # Multiply the score by the weights based on game phase
    score_MG_w *= factor_MG
    score_EG_w *= factor_EG
    score_MG_b *= factor_MG
    score_EG_b *= factor_EG
    # Multiply the piece values by the game phase factor
    all_val_MG_w *= factor_MG
    all_val_EG_w *= factor_EG
    all_val_MG_b *= factor_MG
    all_val_EG_b *= factor_EG

    # Return the final score as the sum of all the part scores minus the opponent's scores
    if(turn == 'w'):
        return score_MG_w + score_EG_w + all_val_MG_w + all_val_EG_w - all_val_MG_b - all_val_EG_b - score_MG_b - score_EG_b
    else:
        return score_MG_b + score_EG_b + all_val_MG_b + all_val_EG_b - all_val_MG_w - all_val_EG_w - score_MG_w - score_EG_w

# Calculating which move is best
def get_best_move(pieces, game, piecenum_w, piecenum_b, last_move, turn, depth):
    '''
    This function returns the "best" move based on the eval function (highest eval means best)
    Args:
        pieces: Dictionary with piece name (string) as key, Piece object as value
        game: 2D array containing the names of pieces at the locations of their squares
        piecenum_w: Dictionary with the piece type (string) as key, id (int) for white as value
        piecenum_b: Dictionary with the piece type (string) as key, id (int) for black as value
        last_move: Move object containing the last move that was played
        turn: String, white or black's turn
        depth: Integer detailing how many moves ahead to compute
    Returns:
        best_move: Move object containing the best move for a given position
        best_score: Float containing the resulting eval score after playing the best move
    '''
    all_moves = []
    # The mutable types need to be copied, as we are doing lots of changes to them
    pieces_copy = copy.deepcopy(pieces)
    game_copy = copy.deepcopy(game)
    piecenum_w_copy = copy.deepcopy(piecenum_w)
    piecenum_b_copy = copy.deepcopy(piecenum_b)

    pieces_copy = get_moves(pieces_copy, game_copy, last_move, turn)

    # Add all possible moves
    for i in pieces_copy:
        # Only add moves from pieces of your own color
        if(i[-1] == turn):
            for move in pieces_copy[i].moves:
                temp = Move(i, pieces_copy[i].pos, move[0], get_piece(game_copy, move[0]), move[2], pieces_copy[i].has_moved, None)
                # If enpassant, the taken position is incorrect, so need to correct that
                if(move[2] == 'e'):
                    # If the move is going to the 6th rank, it means white pawn is taking black pawn
                    if(move[0][1] == 5):
                        # The actual pawn is behind the move, so -1 to the y coordinate
                        temp.taken = game_copy[move[0][0]][move[0][1]-1]
                    # Black pawn is taking white pawn
                    elif(move[0][1] == 2):
                        # The actual pawn is behind the move, so +1 to the y coordinate (black is reversed)
                        temp.taken = game_copy[move[0][0]][move[0][1]+1]

                # Note the state of the taken piece (for history/takeback)
                if(temp.taken is not None):
                    temp.t_has_moved = pieces_copy[temp.taken].has_moved

                if(i[0] == 'p'):
                    # A pawn has reached the last rank, meaning promotion
                    if(move[0][1] == 7 or move[0][1] == 0):
                        # There are four possible outcomes of a promotion, so need to add them all, one of which is temp
                        temp.special = 'pn'
                        all_moves.append(Move(i, pieces_copy[i].pos, move[0], temp.taken, 'pb', pieces_copy[i].has_moved, temp.t_has_moved))
                        all_moves.append(Move(i, pieces_copy[i].pos, move[0], temp.taken, 'pr', pieces_copy[i].has_moved, temp.t_has_moved))
                        all_moves.append(Move(i, pieces_copy[i].pos, move[0], temp.taken, 'pq', pieces_copy[i].has_moved, temp.t_has_moved))

                # Add the move to the list
                all_moves.append(temp)

    # If depth is 1, only checking the current best move
    if(depth == 1):
        # Set it to an arbritrarily low number becasue score can be negative
        best_score = -100000
        best_move = None
        # Check the score of each move
        for i in all_moves:
            # Calculate the positions after the move is made
            results = next_board(pieces_copy, game_copy, i, piecenum_w_copy, piecenum_b_copy, turn)

            # Check the score
            score = eval(results[0], turn)
            if(score > best_score):
                best_score = score
                best_move = i

        return best_move, best_score

    # Depth > 1, checking future steps with recursion (brute force)
    else:
        best_score = -100000
        best_move = None

        for i in all_moves:
            # Calculate the next board (make/choose a random move)
            results = next_board(pieces_copy, game_copy, i, piecenum_w_copy, piecenum_b_copy, turn)
            # Find the score of doing this move
            score_c = eval(results[0], turn)
            # Find the opponent's best move and the corresponding score
            if(turn == 'w'):
                move_o, score_o = get_best_move(results[0], results[1], results[2], results[3], i, 'b', depth-1)
            else:
                move_o, score_o = get_best_move(results[0], results[1], results[2], results[3], i, 'w', depth-1)
            # Subtract opponent's score from our's score (maximize the score difference rather than absolute score)
            total_score = score_c - score_o
            # Note down which move has highest score difference
            if(total_score > best_score):
                best_move = i
                best_score = total_score

        return best_move, best_score
