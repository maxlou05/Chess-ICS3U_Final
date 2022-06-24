# ICS3U-01
# Maxwell Lou
# This file contains the rules of chess
# The functions calcualte what are the possible moves of each piece

import copy
from helper_functions import *
from data import *

def pawn_w(self, game, last_move):
    '''
    This function finds all the possible moves of a white pawn.
    Args:
        self: The Piece object of the pawn to calculate moves for
        game: 2D array containing the names of pieces at the locations of their squares
        last_move: Move object containing the last move that was played
    Returns:
        moves: Array of tuples containing partial information for a move (next position, name of taken piece, speical move type)
    '''
    moves = []

    # Check if there's something else in front
    test = (self.pos[0], self.pos[1] + 1)
    if (in_board(test)):
        if (get_piece(game, test) == None):
            moves.append((test, 0, None))  # 0 for empty square, 1 for capturing a piece (for drawing)
            # Can move forwards twice if on the starting row
            # Only works if the there's nothing blocking the square one ahead anyways
            if (self.pos[1] == 1):
                test = (self.pos[0], self.pos[1] + 2)
                if (get_piece(game, test) == None):
                    moves.append((test, 0, None))

    # Check if there's enemy pieces on the diagonals
    tests = [(self.pos[0] - 1, self.pos[1] + 1),
             (self.pos[0] + 1, self.pos[1] + 1)]
    for t in tests:
        if (in_board(t)):
            piece = get_piece(game, t)
            # Check if there is a piece to be taken
            if (piece != None):
                if (piece[-1] == 'b'):
                    moves.append((t, 1, None))
            # Check for enpassant
            piece = get_piece(game, (t[0], t[1] - 1))
            if (piece != None):
                if (piece[0] == 'p' and piece[-1] == 'b'):
                    if (pos_equals(last_move.start, (t[0], t[1] + 1))):
                        moves.append((t, 1, 'e'))

    return moves

def pawn_b(self, game, last_move):
    '''
    This function finds all the possible moves of a black pawn.
    Args:
        self: The Piece object of the pawn to calculate moves for
        game: 2D array containing the names of pieces at the locations of their squares
        last_move: Move object containing the last move that was played
    Returns:
        moves: Array of tuples containing partial information for a move (next position, name of taken piece, speical move type)
    '''
    # Black pawns move 'down' the board
    moves = []

    # Check if there's something else in front
    test = (self.pos[0], self.pos[1] - 1)
    if (in_board(test)):
        if (get_piece(game, test) == None):
            moves.append((test, 0, None))
            # Can move forwards twice if on the starting row
            # Only works if the there's nothing blocking the square one ahead anyways
            if (self.pos[1] == 6):
                test = (self.pos[0], self.pos[1] - 2)
                if (get_piece(game, test) == None):
                    moves.append((test, 0, None))

    # Check if there's enemy pieces on the diagonals
    tests = [(self.pos[0] - 1, self.pos[1] - 1),
             (self.pos[0] + 1, self.pos[1] - 1)]
    for t in tests:
        if (in_board(t)):
            piece = get_piece(game, t)
            if (piece != None):
                if (piece[-1] == 'w'):
                    moves.append((t, 1, None))
            # Check for enpassant
            piece = get_piece(game, (t[0], t[1] + 1))
            if (piece != None):
                if (piece[0] == 'p' and piece[-1] == 'w'):
                    if (pos_equals(last_move.start, (t[0], t[1] - 1))):
                        moves.append((t, 1, 'e'))

    return moves

def knight(self, game):
    '''
    This function finds all the possible moves of a knight.
    Args:
        self: The Piece object of the knight to calculate moves for
        game: 2D array containing the names of pieces at the locations of their squares
    Returns:
        moves: Array of tuples containing partial information for a move (next position, name of taken piece, speical move type)
    '''
    moves = []
    name = get_piece(game, self.pos)

    # List of possible moves
    tests = [(self.pos[0] - 2, self.pos[1] - 1),
             (self.pos[0] - 2, self.pos[1] + 1),
             (self.pos[0] - 1, self.pos[1] - 2),
             (self.pos[0] - 1, self.pos[1] + 2),
             (self.pos[0] + 1, self.pos[1] - 2),
             (self.pos[0] + 1, self.pos[1] + 2),
             (self.pos[0] + 2, self.pos[1] - 1),
             (self.pos[0] + 2, self.pos[1] + 1)]
    for t in tests:
        if (in_board(t)):
            piece = get_piece(game, t)
            if (piece == None):
                moves.append((t, 0, None))
            elif (piece[-1] != name[-1]):  # If the piece is other colour
                moves.append((t, 1, None))

    return moves

def bishop(self, game):
    '''
    This function finds all the possible moves of a bishop.
    Args:
        self: The Piece object of the bishop to calculate moves for
        game: 2D array containing the names of pieces at the locations of their squares
    Returns:
        moves: Array of tuples containing partial information for a move (next position, name of taken piece, speical move type)
    '''
    moves = []
    name = get_piece(game, self.pos)

    steps = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Possible steps
    for s in steps:
        available = True
        test = [self.pos[0], self.pos[1]]  # Reset to current position
        while available:
            available = False
            # Increment by step (next possible square along the line)
            test[0] += s[0]
            test[1] += s[1]
            # Check if that square is a possible move
            # If it's not a valid move, then stop and check the next line
            if (in_board(test)):
                piece = get_piece(game, test)
                if (piece == None):
                    moves.append(((test[0], test[1]), 0, None))
                    available = True  # If it's an empty square, continue and check the next increment
                # If the piece that it encounters is an opposing piece
                elif (piece[-1] != name[-1]):
                    moves.append(((test[0], test[1]), 1, None))  # If it's a capture, stop and check the next line

    return moves

def rook(self, game):
    '''
    This function finds all the possible moves of a rook.
    Args:
        self: The Piece object of the rook to calculate moves for
        game: 2D array containing the names of pieces at the locations of their squares
    Returns:
        moves: Array of tuples containing partial information for a move (next position, name of taken piece, speical move type)
    '''
    moves = []
    name = get_piece(game, self.pos)

    steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Possible steps
    for s in steps:
        available = True
        test = [self.pos[0], self.pos[1]]
        while available:
            available = False
            test[0] += s[0]
            test[1] += s[1]
            if (in_board(test)):
                piece = get_piece(game, test)
                if (piece == None):
                    moves.append(((test[0], test[1]), 0, None))
                    available = True
                elif (piece[-1] != name[-1]):
                    moves.append(((test[0], test[1]), 1, None))

    return moves

def queen(self, game):
    '''
    This function finds all the possible moves of a queen.
    Args:
        self: The Piece object of the queen to calculate moves for
        game: 2D array containing the names of pieces at the locations of their squares
    Returns:
        moves: Array of tuples containing partial information for a move (next position, name of taken piece, speical move type)
    '''
    moves = []
    name = get_piece(game, self.pos)

    steps = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1),
             (-1, -1)]  # Possible steps
    for s in steps:
        available = True
        test = [self.pos[0], self.pos[1]]
        while available:
            available = False
            test[0] += s[0]
            test[1] += s[1]
            if (in_board(test)):
                piece = get_piece(game, test)
                if (piece == None):
                    moves.append(((test[0], test[1]), 0, None))
                    available = True
                elif (piece[-1] != name[-1]):
                    moves.append(((test[0], test[1]), 1, None))

    return moves

def king(self, game, pieces):
    '''
    This function finds all the possible moves of a king.
    Args:
        self: The Piece object of the king to calculate moves for
        game: 2D array containing the names of pieces at the locations of their squares
        pieces: Dictionary with piece name (string) as key, Piece object as value
    Returns:
        moves: Array of tuples containing partial information for a move (next position, name of taken piece, speical move type)
    '''
    moves = []
    name = get_piece(game, self.pos)

    # Standard moves (in 8 directions)
    tests = [(self.pos[0] - 1, self.pos[1] - 1),
             (self.pos[0] - 1, self.pos[1]),
             (self.pos[0] - 1, self.pos[1] + 1),
             (self.pos[0] + 1, self.pos[1] - 1),
             (self.pos[0] + 1, self.pos[1]),
             (self.pos[0] + 1, self.pos[1] + 1),
             (self.pos[0], self.pos[1] + 1),
             (self.pos[0], self.pos[1] - 1)]
    for t in tests:
        if (in_board(t)):
            piece = get_piece(game, t)
            if (piece == None):
                moves.append((t, 0, None))
            elif (piece[-1] != name[-1]):
                moves.append((t, 1, None))

    # Castling (haven't moved yet)
    if (not self.has_moved):
        # White king
        if (name[-1] == 'w'):
            # The rook may be taken beforehand, resulting in key error
            try:
                # If rook 0 hasn't moved, it is on the queen side (by setup)
                if (not pieces["r0w"].has_moved):
                    O_O_O = True
                    # Make sure there's no pieces in between the king and the rook
                    for i in range(1, 4):
                        test = get_piece(game, (i, 0))
                        if (test != None):
                            O_O_O = False
                            break
                    if (O_O_O):
                        moves.append(((self.pos[0] - 2, 0), 0, 'O_O_Ow'))
            except:
                # If rook is taken, it's ok, just don't add this castling move
                pass
            try:
                # If rook 1 hasn't moved, it is on the king side (by setup)
                if (not pieces["r1w"].has_moved):
                    O_O = True
                    for i in range(5, 7):
                        test = get_piece(game, (i, 0))
                        if (test != None):
                            O_O = False
                            break
                    if (O_O):
                        moves.append(((self.pos[0] + 2, 0), 0, 'O_Ow'))
            except:
                pass

        # Black king
        if (name[-1] == 'b'):
            try:
                # If rook 0 hasn't moved, it is on the queen side (by setup)
                if (not pieces["r0b"].has_moved):
                    O_O_O = True
                    for i in range(1, 4):
                        test = get_piece(game, (i, 7))
                        if (test != None):
                            O_O_O = False
                            break
                    if (O_O_O):
                        moves.append(((self.pos[0] - 2, 7), 0, 'O_O_Ob'))
            except:
                pass
            try:
                # If rook 1 hasn't moved, it is on the king side (by setup)
                if (not pieces["r1b"].has_moved):
                    O_O = True
                    for i in range(5, 7):
                        test = get_piece(game, (i, 7))
                        if (test != None):
                            O_O = False
                            break
                    if (O_O):
                        moves.append(((self.pos[0] + 2, 7), 0, 'O_Ob'))
            except:
                pass

    return moves

def is_attacked(pieces, turn, square):
    '''
    This function finds if a particular square is under attack by the opponent's pieces
    Args:
        pieces: Dictionary with piece name (string) as key, Piece object as value
        turn: String, white or black's turn
        square: A tuple (int, int) of the square that is being examined
    Returns: True or False
    '''
    for i in pieces:
        # Only check the opposing pieces' moves
        if(i[-1] != turn):
            for j in pieces[i].moves:
                # If opposing pieces can move onto the selected square, it is being attacked
                if(pos_equals(j[0], square)):
                    return True
    return False

def get_moves_preliminary(pieces, game, last_move):
    '''
    This function calculates all the possible moves of each piece.
    Args:
        pieces: Dictionary with piece name (string) as key, Piece object as value
        game: 2D array containing the names of pieces at the locations of their squares
        last_move: Move object containing the last move that was played
    Returns:
        pieces: Dictionary with piece name (string) as key, Piece object as value
    '''
    # Use the corresponding algorithm to calculate the moves of each piece
    for i in pieces:
        if(i[0] == 'p'):
            if(i[-1] == 'w'):
                pieces[i].moves = pawn_w(pieces[i], game, last_move)
            elif(i[-1] == 'b'):
                pieces[i].moves = pawn_b(pieces[i], game, last_move)
        elif(i[0] == 'n'):
            pieces[i].moves = knight(pieces[i], game)
        elif(i[0] == 'b'):
            pieces[i].moves = bishop(pieces[i], game)
        elif(i[0] == 'r'):
            pieces[i].moves = rook(pieces[i], game)
        elif(i[0] == 'q'):
            pieces[i].moves = queen(pieces[i], game)
        elif(i[0] == 'k'):
            pieces[i].moves = king(pieces[i], game, pieces)

    return pieces

def is_check(pieces, game, last_move, turn, move, piece):
    '''
    This function checks whether a particular move causes the king to be in check.
    Args:
        pieces: Dictionary with piece name (string) as key, Piece object as value
        game: 2D array containing the names of pieces at the locations of their squares
        last_move: Move object containing the last move that was played
        turn: String, white or black's turn
        move: A tuple containing partial information for a move (next position, name of taken piece, speical move type)
        piece: String, the name of the piece making the move
    Returns: True or False
    '''
    # Make deep copies, because pieces and game are mutable objects (dictionary/list)
    # Mutable objects can be thought of as passed by reference
    # Hence, need to make a deepcopy if I don't want the outside one to change
    pieces_next = copy.deepcopy(pieces)
    game_next = copy.deepcopy(game)

    # Create the move
    temp = Move(piece, pieces_next[piece].pos, move[0], get_piece(game_next, move[0]), move[2], pieces_next[piece].has_moved, None)
    # If enpassant, the taken position is incorrect, so need to correct that
    if(move[2] == 'e'):
        # If the move is going to the 6th rank, it means white pawn is taking black pawn
        if(move[0][1] == 5):
            # The actual pawn is behind the move, so -1 to the y coordinate
            temp.taken = game_next[move[0][0]][move[0][1]-1]
        # Black pawn is taking white pawn
        elif(move[0][1] == 2):
            # The actual pawn is behind the move, so +1 to the y coordinate (black is reversed)
            temp.taken = game_next[move[0][0]][move[0][1]+1]

    # Note the state of the taken piece (for history/takeback)
    if(temp.taken is not None):
        temp.t_has_moved = pieces_next[temp.taken].has_moved

    # Pretend the move was played (calculate the next board)
    # No need to check promotion, because the effects only happen next turn
    # (if a piece is promoted this turn, it cannot move until the next turn, so it can be treated as just a normal move forward)
    results = next_board(pieces_next, game_next, temp, None, None, turn)

    # Then calculate all the next possible moves
    pieces_next = get_moves_preliminary(results[0], results[1], last_move)

    # See if doing that move ends up in check
    if(turn == 'w'):
        king_pos = pieces_next['k0w'].pos
    else:
        king_pos = pieces_next['k0b'].pos
    # return if this move causes the king to be attacked (in check)
    return is_attacked(pieces_next, turn, king_pos)

def get_moves(pieces, game, last_move, turn):
    '''
    This function gets all the possible moves and removes the illegal ones.
    Args:
        pieces: Dictionary with piece name (string) as key, Piece object as value
        game: 2D array containing the names of pieces at the locations of their squares
        last_move: Move object containing the last move that was played
        turn: String, white or black's turn
    Returns:
        pieces: Dictionary with piece name (string) as key, Piece object as value
    '''
    # Get possible moves
    pieces = get_moves_preliminary(pieces, game, last_move)

    # Check for illegal moves
    illegal_moves = []
    # Check every possible move to see if it puts yourself in check
    for i in pieces:
        # Don't check the opponent's moves, checking for your own illegal moves
        if(i[-1] == turn):
            for j in pieces[i].moves:
                # Anything that puts yourself into check is illegal
                if is_check(pieces, game, last_move, turn, j, i):
                    illegal_moves.append((i, j))

    # Remove the illegal moves
    for i in illegal_moves:
        pieces[i[0]].moves.remove(i[1])

    illegal_moves = []
    # Cannot castle while in check (have to do these later because may try to delete same move twice)
    king = f"k0{turn}"
    if(is_attacked(pieces, turn, pieces[king].pos)):
        for i in pieces[king].moves:
            if(i[2] is not None):
                illegal_moves.append((king, i))

    for i in illegal_moves:
        pieces[i[0]].moves.remove(i[1])

    illegal_moves = []
    # Cannot castle through danger
    if(is_attacked(pieces, turn, (3,0))): # For O_O_Ow
        for i in pieces["k0w"].moves:
            if(i[2] == "O_O_Ow"):
                illegal_moves.append(("k0w", i))
                break
    if(is_attacked(pieces, turn, (5,0))): # For O_Ow
        for i in pieces["k0w"].moves:
            if(i[2] == "O_Ow"):
                illegal_moves.append(("k0w", i))
                break
    if(is_attacked(pieces, turn, (3,7))): # For O_O_Ob
        for i in pieces["k0b"].moves:
            if(i[2] == "O_O_Ob"):
                illegal_moves.append(("k0b", i))
                break
    if(is_attacked(pieces, turn, (5,7))): # For O_Ob
        for i in pieces["k0b"].moves:
            if(i[2] == "O_Ob"):
                illegal_moves.append(("k0b", i))
                break

    for i in illegal_moves:
        pieces[i[0]].moves.remove(i[1])

    return pieces

def is_mate(pieces, turn):
    '''
    This function checks whether the game is in a checkmate or stalemate position.
    Args:
        pieces: Dictionary with piece name (string) as key, Piece object as value
        turn: String, white or black's turn
    Returns: "checkmate" (string) if checkmate, "stalemate" (string) if stalement, None if neither
    '''
    total_moves = 0
    # Check all possible moves
    for i in pieces:
        # Only the check possible moves for the player whose turn it is
        if(i[-1] == turn):
            total_moves += len(pieces[i].moves)
    # If no legal moves, that means checkmate
    if(total_moves == 0):
        if(is_attacked(pieces, turn, pieces[f'k0{turn}'].pos)):
            return "checkmate"
        else:
            return "stalemate"
    else:
        return None
