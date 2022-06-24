# ICS3U-01
# Maxwell Lou
# This file contains useful functions that are used a lot
# It is a sort of toolbox, util functions

import copy
from data import *

def get_coord(flip, pos):
    '''
    This function gets the coordinates on the window given a square on the chess board.
    Args:
        flip: Bool, whether the board is flipped or not
        pos: A tuple (int, int) of which square on the board
    Returns:
        coord: A tuple (int, int) of the corresponding coordinates
    '''
    if not flip:
        return (pos[0] * TILE_SIZE + PAD_LEFT, (7 - pos[1]) * TILE_SIZE + PAD_TOP)
    else:
        return ((7 - pos[0]) * TILE_SIZE + PAD_LEFT, pos[1] * TILE_SIZE + PAD_TOP)


def get_pos(flip, coord):
    '''
    This function gets the square of the chess board given a coordinate (only use when coordinate is within the board).
    Args:
        flip: Bool, whether the board is flipped or not
        coord: A tuple (int, int) of the corresponding coordinates
    Returns:
        pos: A tuple (int, int) of which square on the board
    '''
    if not flip:
        return (int((coord[0] - PAD_LEFT) / TILE_SIZE), 7 - int((coord[1] - PAD_TOP) / TILE_SIZE))
    else:
        return (7 - int((coord[0] - PAD_LEFT) / TILE_SIZE), int((coord[1] - PAD_TOP) / TILE_SIZE))


def get_piece(game, pos):
    '''
    This function returns the piece that is on a given square of the chess board.
    Args:
        game: 2D array containing the names of pieces at the locations of their squares
        pos: A tuple (int, int) of which square on the board
    Returns:
        name: String, the name of piece on the given square, or None if there is no piece on that square
    '''
    if (len(game[pos[0]][pos[1]]) != 0):
        return game[pos[0]][pos[1]]
    return None


def in_board(pos):
    '''
    This function returns whether a square is within the chess board or not.
    Args:
        pos: A tuple (int, int) of which square on the board
    Returns: True or False
    '''
    if (pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8):
        return True
    return False


def pos_equals(pos1, pos2):
    '''
    This function returns whether two squares are the same or not.
    Args:
        pos1: A tuple (int, int) of which square on the board
        pos2: A tuple (int, int) of which square on the board
    Returns: True or False    
    '''
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]


def name_to_pic(name):
    '''
    This function returns the name of picutre file corresponding to a piece type.
    Args:
        name: String, name of the piece
    Returns:
        pic: String, file name of the picutre of the piece
    '''
    if(name[0] == 'p'):
        return f"pawn_{name[-1]}"
    elif(name[0] == 'n'):
        return f"knight_{name[-1]}"
    elif(name[0] == 'b'):
        return f"bishop_{name[-1]}"
    elif(name[0] == 'r'):
        return f"rook_{name[-1]}"
    elif(name[0] == 'q'):
        return f"queen_{name[-1]}"
    elif(name[0] == 'k'):
        return f"king_{name[-1]}"

def next_board(pieces, game, move, piecenum_w, piecenum_b, turn):
    '''
    This function updates all the variables when a move is made.
    Args:
        pieces: Dictionary with piece name (string) as key, Piece object as value
        game: 2D array containing the names of pieces at the locations of their squares
        move: Move object containing the move to be made
        piecenum_w: Dictionary with the piece type (string) as key, id (int) for white as value
        piecenum_b: Dictionary with the piece type (string) as key, id (int) for black as value
        turn: String, white or black's turn
    Returns:
        pieces_next: Dictionary with piece name (string) as key, Piece object as value
        game_next: 2D array containing the names of pieces at the locations of their squares
        piecenum_w: Dictionary with the piece type (string) as key, id (int) for white as value
        piecenum_b: Dictionary with the piece type (string) as key, id (int) for black as value
    '''
    # Make deep copies to not chnage the inputted ones
    pieces_next = copy.deepcopy(pieces)
    game_next = copy.deepcopy(game)

    # Move the piece
    # The piece has moved away from its current square
    game_next[move.start[0]][move.start[1]] = ""
    # Put the piece on the new square (overwrites the piece that was there)
    game_next[move.end[0]][move.end[1]] = move.name
    pieces_next[move.name].pos = move.end

    # Taking a piece
    if(move.taken is not None):
        # Remove taken piece from memory
        del pieces_next[move.taken]

    # Castling (just need to account for the rook being moved since king already moved)
    # Castling is a predetermined move, has to be those exact squares and pieces
    if(move.special == "O_O_Ow"):
        game_next[0][0] = ""
        game_next[3][0] = "r0w"
        pieces_next["r0w"].pos = (3, 0)
    elif(move.special == "O_Ow"):
        game_next[7][0] = ""
        game_next[5][0] = "r1w"
        pieces_next["r1w"].pos = (5, 0)
    elif(move.special == "O_O_Ob"):
        game_next[0][7] = ""
        game_next[3][7] = "r0b"
        pieces_next["r0b"].pos = (3, 7)
    elif(move.special == "O_Ob"):
        game_next[7][7] = ""
        game_next[5][7] = "r1b"
        pieces_next["r1b"].pos = (5, 7)

    # Promotion, if specified which piece it is
    # In other uses, when unknown/not specified, it just skips this part
    name = None
    num = None
    if(turn == 'w'):
        num = piecenum_w
    else:
        num = piecenum_b
    # Just to be safe, I can input None for piecenum to skip this
    if(num is not None):
        # Promotion for knight
        if(move.special == 'pn'):
            name = f"n{num['n']}{turn}"
            # This should change the corresponding piecenum because num is a reference to it
            num['n'] += 1
        # Promotion for bishop
        elif(move.special == 'pb'):
            name = f"n{num['b']}{turn}"
            num['b'] += 1
        # Promotion for rook
        elif(move.special == 'pr'):
            name = f"r{num['r']}{turn}"
            num['r'] += 1
        # Promotion for queen
        elif(move.special == 'pq'):
            name = f"q{num['q']}{turn}"
            num['q'] += 1
        if(name is not None):
            # Delete the pawn
            del pieces_next[move.name]
            # Add the piece to memory
            game_next[move.end[0]][move.end[1]] = name
            pieces_next[name] = Piece(move.end)

    return pieces_next, game_next, piecenum_w, piecenum_b
