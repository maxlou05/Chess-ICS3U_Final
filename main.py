# ICS3U-01
# Maxwell Lou
# This is the main file of the chess game
# It contains the main logical controls and draws the window
# Players can play two player chess (against a friend) or one player chess (against the computer)

import pgzrun
import sys
from helper_functions import *
from get_moves import *
from data import *
from engine import *

# Control functions
def end_turn():
    '''
    This function is called at the end of a turn to prepare for the next turn.
    It calculates all possible moves for the next turn, and checks if the game is over.
    Args: None
    Returns: None
    '''
    global stop
    global turn
    global flipped
    global pieces
    global actors
    global mode
    global state
    global history
    global win

    # When promoting, need to give time for them to select
    # Everything else needs to stay still during that time
    # This if statement is for that purpose (ending the animation calls end_turn, but state is not game when promoting)
    if(state == "game"):
        # Update the turn
        if (turn == 'w'):
            turn = 'b'
        else:
            turn = 'w'

        # Calculate moves for all pieces
        pieces = get_moves(pieces, game, history[-1], turn)

        # print(history[-1].name, history[-1].start, history[-1].end, history[-1].taken, history[-1].special, history[-1].has_moved, history[-1].t_has_moved)

        # Check if the game is over or not
        mate = is_mate(pieces, turn)
        if(mate is not None):
            # Turn is flipped becasue if white has no moves, black wins
            if(turn == 'w'):
                # If the king is being attacked, it's a checkmate
                if(mate == "checkmate"):
                    state = "win_b"
                    win = "checkmate"
                # Otherwise it's a stalemate
                else:
                    state = "draw"
                    win = "stalemate"
            else:
                if(mate == "checkmate"):
                    state = "win_w"
                    win = "checkmate"
                else:
                    state = "draw"
                    win = "stalemate"
            # Do not continue and end the game
            return

        # Check for repeated moves draw (if the same board position occurs 3 times in a row)
        # (The board positions in between the repeating ones don't matter)
        # This doesn't exactly follow the official rules, but it's good enough for normal players
        if(len(history) > 10):
            if(history[-1].equals(history[-5]) and history[-1].equals(history[-9])):
                if(history[-2].equals(history[-6]) and history[-2].equals(history[-10])):
                    state = "draw"
                    win = "repetition"
                    # Game is over, do not continue
                    return

        # Reset draw condition (if opponent requested a draw but you moved, they have to request again)
        # If white requested draw and it's their turn again, that means black rejected their request
        if(win == "draw_w" and turn == 'w'):
            win = ""
        elif(win == "draw_b" and turn == 'b'):
            win = ""

        if(mode == "2-player"):
            flipped = not flipped # true -> false, false -> true
            # Flip the pieces
            for key in pieces:
                actors[key].topleft = get_coord(flipped, pieces[key].pos)

            # Add time back
            if(time_limit > 0):
                if(turn == 'w'): # This is reversed becasue turn was just changed earlier
                    time_black.add_time(0, time_back, 0)
                else:
                    time_white.add_time(0, time_back, 0)

        stop = False # Allow the user to input again


def pause():
    '''
    This function stops the player from being able to input, so no additional inputs happen during animations.
    Args: None
    Returns: None
    '''
    global stop
    stop = True


def unpause():
    '''
    This function is used to put a delay between the animation end and the player's ability to input again.
    This makes sure the animation finishes, and also there is a little pause before the board flips, making it look less wonky.
    Args: None
    Returns: None
    '''
    clock.schedule(end_turn, 0.1)


def promotion_w():
    '''
    This function triggers the promotion state for white.
    Args: None
    Returns: None
    '''
    global state
    state = "promotion_w"


def promotion_b():
    '''
    This function triggers the promotion state for black.
    Args: None
    Returns: None
    '''
    global state
    state = "promotion_b"


def setup():
    '''
    This function resets all variables to default values needed to start a game from the beginning.
    Args: None
    Returns: None
    '''
    global selected
    global square
    global highlighted_moves
    global game
    global board
    global pieces
    global actors
    global move
    global stop
    global piecenum_w
    global piecenum_b
    global taken_pieces_w
    global taken_pieces_b
    global history
    global turn
    global flipped
    global state
    global mode
    global difficulty
    global time_limit
    global time_back
    global time_white
    global time_black
    global win
    global promote
    global player

    selected = None
    square = None
    highlighted_moves = []
    game = []
    board = []
    pieces = {}
    actors = {}
    move = None
    stop = False
    piecenum_w = {'p': 8, 'n': 2, 'b': 2, 'r': 2, 'q': 1}
    piecenum_b = {'p': 8, 'n': 2, 'b': 2, 'r': 2, 'q': 1}
    taken_pieces_w = {'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0}
    taken_pieces_b = {'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0}
    history = [Move("r0w",(0,0), (0,0), None, None, False, None)]
    turn = 'w'
    flipped = False
    state = "menu"
    mode = ""
    difficulty = 0
    time_limit = 0
    time_back = 0
    time_white = Time(0,0,0)
    time_black = Time(0,0,0)
    win = ""
    promote = None
    player = 'w'

    for x in range(8):
        board.append([])
        game.append([])
        for y in range(8):
            coord = get_coord(flipped, (x, y))
            board[x].append(Rect(coord, (TILE_SIZE, TILE_SIZE)))
            game[x].append("")

    game[0][1] = "p0w"
    pieces["p0w"] = Piece((0, 1))
    actors["p0w"] = Actor('pawn_w')
    game[1][1] = "p1w"
    pieces["p1w"] = Piece((1, 1))
    actors["p1w"] = Actor('pawn_w')
    game[2][1] = "p2w"
    pieces["p2w"] = Piece((2, 1))
    actors["p2w"] = Actor('pawn_w')
    game[3][1] = "p3w"
    pieces["p3w"] = Piece((3, 1))
    actors["p3w"] = Actor('pawn_w')
    game[4][1] = "p4w"
    pieces["p4w"] = Piece((4, 1))
    actors["p4w"] = Actor('pawn_w')
    game[5][1] = "p5w"
    pieces["p5w"] = Piece((5, 1))
    actors["p5w"] = Actor('pawn_w')
    game[6][1] = "p6w"
    pieces["p6w"] = Piece((6, 1))
    actors["p6w"] = Actor('pawn_w')
    game[7][1] = "p7w"
    pieces["p7w"] = Piece((7, 1))
    actors["p7w"] = Actor('pawn_w')
    game[0][0] = "r0w"
    pieces["r0w"] = Piece((0, 0))
    actors["r0w"] = Actor('rook_w')
    game[1][0] = "n0w"
    pieces["n0w"] = Piece((1, 0))
    actors["n0w"] = Actor('knight_w')
    game[2][0] = "b0w"
    pieces["b0w"] = Piece((2, 0))
    actors["b0w"] = Actor('bishop_w')
    game[3][0] = "q0w"
    pieces["q0w"] = Piece((3, 0))
    actors["q0w"] = Actor('queen_w')
    game[4][0] = "k0w"
    pieces["k0w"] = Piece((4, 0))
    actors["k0w"] = Actor('king_w')
    game[5][0] = "b1w"
    pieces["b1w"] = Piece((5, 0))
    actors["b1w"] = Actor('bishop_w')
    game[6][0] = "n1w"
    pieces["n1w"] = Piece((6, 0))
    actors["n1w"] = Actor('knight_w')
    game[7][0] = "r1w"
    pieces["r1w"] = Piece((7, 0))
    actors["r1w"] = Actor('rook_w')
    game[0][6] = "p0b"
    pieces["p0b"] = Piece((0, 6))
    actors["p0b"] = Actor('pawn_b')
    game[1][6] = "p1b"
    pieces["p1b"] = Piece((1, 6))
    actors["p1b"] = Actor('pawn_b')
    game[2][6] = "p2b"
    pieces["p2b"] = Piece((2, 6))
    actors["p2b"] = Actor('pawn_b')
    game[3][6] = "p3b"
    pieces["p3b"] = Piece((3, 6))
    actors["p3b"] = Actor('pawn_b')
    game[4][6] = "p4b"
    pieces["p4b"] = Piece((4, 6))
    actors["p4b"] = Actor('pawn_b')
    game[5][6] = "p5b"
    pieces["p5b"] = Piece((5, 6))
    actors["p5b"] = Actor('pawn_b')
    game[6][6] = "p6b"
    pieces["p6b"] = Piece((6, 6))
    actors["p6b"] = Actor('pawn_b')
    game[7][6] = "p7b"
    pieces["p7b"] = Piece((7, 6))
    actors["p7b"] = Actor('pawn_b')
    game[0][7] = "r0b"
    pieces["r0b"] = Piece((0, 7))
    actors["r0b"] = Actor('rook_b')
    game[1][7] = "n0b"
    pieces["n0b"] = Piece((1, 7))
    actors["n0b"] = Actor('knight_b')
    game[2][7] = "b0b"
    pieces["b0b"] = Piece((2, 7))
    actors["b0b"] = Actor('bishop_b')
    game[3][7] = "q0b"
    pieces["q0b"] = Piece((3, 7))
    actors["q0b"] = Actor('queen_b')
    game[4][7] = "k0b"
    pieces["k0b"] = Piece((4, 7))
    actors["k0b"] = Actor('king_b')
    game[5][7] = "b1b"
    pieces["b1b"] = Piece((5, 7))
    actors["b1b"] = Actor('bishop_b')
    game[6][7] = "n1b"
    pieces["n1b"] = Piece((6, 7))
    actors["n1b"] = Actor('knight_b')
    game[7][7] = "r1b"
    pieces["r1b"] = Piece((7, 7))
    actors["r1b"] = Actor('rook_b')

    for i in actors:
        actors[i].topleft = get_coord(flipped, pieces[i].pos)

    pieces = get_moves(pieces, game, history[-1], turn)



# MAIN
# Define global variables
selected = None  # Selected piece
square = None  # What square was clicked
highlighted_moves = []  # Possible moves for the selected piece
game = []  # Game state
board = []  # The board
pieces = {}  # The pieces
actors = {} # The actors (for drawing)
move = None
stop = False  # Make sure things don't move while other things are already moving
piecenum_w = {'n': 2, 'b': 2, 'r': 2, 'q': 1} # The maximum piece id number (for white) (used for promotion when creating new pieces)
piecenum_b = {'n': 2, 'b': 2, 'r': 2, 'q': 1} # The maximum piece id number (for black) (used for promotion when creating new pieces)
taken_pieces_w = {'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0} # How many white pieces were taken (for drawing on the side)
taken_pieces_b = {'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0} # How many black pieces were taken (for drawing on the side)
history = [Move("r0w",(0,0), (0,0), None, None, False, None)]  # Track move history (just a placeholder so no index out of bounds error)
turn = 'w'  # Who's turn (white starts)
flipped = False # Is the board flipped (white = false, black = true)
state = "menu"  # The state of game, start in menu (menu, game, piece selection, etc.)
mode = ""  # What mode (1-player, 2-player)
difficulty = 0 # Single player mode difficulty (recursion depth of engine)
time_limit = 0 # Time limit in minutes
time_back = 0 # How much time to add back after each move in seconds
time_white = Time(0,0,0) # How much time white still has
time_black = Time(0,0,0) # How much time black still has
win = "" # How the game is progressing (normal, win, draw/draw request, etc.)
promote = None # What piece the computer decides to promote to
player = 'w' # What color the player is using (for 1-player mode)

game_message = "" # Big text displayed at top for game messages

# Button objects
# Menu
btn_1plyr = Rect(WIDTH/2-100, 200, 200, 75)
btn_2plyr = Rect(WIDTH/2-100, 300, 200, 75)
btn_exit = Rect(WIDTH/2-100, 400, 200, 75)

# Difficulty selection screen
btn_lv = [
    Rect(100, 200, 100, 100),
    Rect(275, 200, 100, 100),
    Rect(450, 200, 100, 100),
    Rect(625, 200, 100, 100),
    Rect(100, 350, 100, 100),
    Rect(275, 350, 100, 100),
    Rect(450, 350, 100, 100),
    Rect(625, 350, 100, 100)]
btn_w = Rect(WIDTH/2 - 50, 500, 50, 50)
btn_b = Rect(WIDTH/2 + 50, 500, 50, 50)

# Time selection screen
btn_inc_total = Rect(300, 225, 50, 50)
btn_dec_total = Rect(300, 325, 50, 50)
btn_inc_back = Rect(600, 225, 50, 50)
btn_dec_back = Rect(600, 325, 50, 50)
btn_next = Rect(WIDTH/2-100, 500, 200, 75)

# Game buttons
btn_resign = Rect(675, 150, 100, 75)
btn_draw = Rect(675, 250, 100, 75)
btn_take_back = Rect(675, 350, 100, 75)


def draw():
    '''
    This function draws everything on the window.
    Args: None
    Returns: None
    '''
    # Things are drawn in order back to front
    # First, draw backgroud since that is always there
    screen.fill(background)

    # Drawing things in the menu
    if(state == "menu"):
        screen.draw.text("Welcome to chess", center=(WIDTH/2, 100), fontsize=96, color=text_light)
        screen.draw.filled_rect(btn_1plyr, text_light)
        screen.draw.filled_rect(btn_2plyr, text_light)
        screen.draw.filled_rect(btn_exit, text_light)
        screen.draw.text("1 player", center=btn_1plyr.center, fontsize=36, color=text_dark)
        screen.draw.text("2 player", center=btn_2plyr.center, fontsize=36, color=text_dark)
        screen.draw.text("Exit", center=btn_exit.center, fontsize=36, color=text_dark)

    # Drawing the buttons and sutff in the difficulty selection phase
    elif(state == "difficulty"):
        screen.draw.text("Select difficulty", center=(WIDTH/2, 100), fontsize=96, color=text_light)
        for i in range(len(btn_lv)):
            screen.draw.filled_rect(btn_lv[i], text_light)
            screen.draw.text(f"{i+1}", center=btn_lv[i].center, fontsize=48, color=text_dark)
        screen.draw.text("Play as", topleft=(WIDTH/2 - 200, 510), fontsize=48, color=text_light)
        if(player == 'w'):
            screen.draw.filled_rect(btn_w, highlight)
        else:
            screen.draw.filled_rect(btn_b, highlight)
        screen.blit('king_w', btn_w.topleft)
        screen.blit('king_b', btn_b.topleft)

    # Drawing stuff for the enter time limit phase
    elif(state == "time"):
        screen.draw.text("Enter time limit", center=(WIDTH/2, 100), fontsize=96, color=text_light)
        screen.draw.filled_rect(Rect(WIDTH/2-300, 200, 600, 200), text_light)
        screen.blit('up_arrow', btn_inc_total.topleft)
        screen.blit('down_arrow', btn_dec_total.topleft)
        screen.blit('up_arrow', btn_inc_back.topleft)
        screen.blit('down_arrow', btn_dec_back.topleft)
        screen.draw.text("(Total time 0 for infinite time)", center=(WIDTH/2, 450), fontsize=36, color=text_light)
        screen.draw.text(f"{time_limit}", midleft=(WIDTH/2-225, 300), fontsize=96, color=text_dark)
        screen.draw.text("Total time (min)", midtop=(WIDTH/2-200, 350), fontsize=36, color=text_dark)
        screen.draw.text(f"{time_back}", midleft=(WIDTH/2+50, 300), fontsize=96, color=text_dark)
        screen.draw.text("Time back (sec)", midtop=(WIDTH/2+75, 350), fontsize=36, color=text_dark)
        screen.draw.filled_rect(btn_next, text_light)
        screen.draw.text("Next", center=btn_next.center, fontsize=36, color=text_dark)

    # Drawing the game (other states just draw ontop of the game state)
    else:
        # Draw board (it stays the same even after flip)
        for x in range(8):
            for y in range(8):
                if ((x + y) % 2) == 0:
                    screen.draw.filled_rect(board[x][y], dark)
                else:
                    screen.draw.filled_rect(board[x][y], light)

        # Draw text surrounding the board
        chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if not flipped:
            for i in range(8):
                # Bottom row
                temp = get_coord(flipped, (i, 0))
                coord = (temp[0] + int(TILE_SIZE / 2), temp[1] + TILE_SIZE + PAD_TEXT)
                screen.draw.text(chars[i], midtop=coord, color=text_light)
                # Top row
                temp = get_coord(flipped, (i, 7))
                coord = (temp[0] + int(TILE_SIZE / 2), temp[1] - PAD_TEXT)
                screen.draw.text(chars[i], midbottom=coord, color=text_light)
                # Left
                temp = get_coord(flipped, (0, i))
                coord = (temp[0] - PAD_TEXT, temp[1] + int(TILE_SIZE / 2))
                screen.draw.text(f"{i+1}", midright=coord, color=text_light)
                # Right
                temp = get_coord(flipped, (7, i))
                coord = (temp[0] + TILE_SIZE + PAD_TEXT, temp[1] + int(TILE_SIZE / 2))
                screen.draw.text(f"{i+1}", midleft=coord, color=text_light)
        else:
            for i in range(8):
                # Bottom row (just switch the row to 7, since now that one's on the bottom)
                temp = get_coord(flipped, (i, 7))
                coord = (temp[0] + int(TILE_SIZE / 2), temp[1] + TILE_SIZE + PAD_TEXT)
                screen.draw.text(chars[i], midtop=coord, color=text_light)
                # Top row
                temp = get_coord(flipped, (i, 0))
                coord = (temp[0] + int(TILE_SIZE / 2), temp[1] - PAD_TEXT)
                screen.draw.text(chars[i], midbottom=coord, color=text_light)
                # Left
                temp = get_coord(flipped, (7, i))
                coord = (temp[0] - PAD_TEXT, temp[1] + int(TILE_SIZE / 2))
                screen.draw.text(f"{i+1}", midright=coord, color=text_light)
                # Right
                temp = get_coord(flipped, (0, i))
                coord = (temp[0] + TILE_SIZE + PAD_TEXT, temp[1] + int(TILE_SIZE / 2))
                screen.draw.text(f"{i+1}", midleft=coord, color=text_light)

        # Draw the game buttons
        screen.draw.filled_rect(btn_resign, text_light)
        screen.draw.text("resign", center=btn_resign.center, fontsize=24, color=text_dark)
        screen.draw.filled_rect(btn_draw, text_light)
        screen.draw.text("draw", center=btn_draw.center, fontsize=24, color=text_dark)
        screen.draw.filled_rect(btn_take_back, text_light)
        screen.draw.text("take back", center=btn_take_back.center, fontsize=24, color=text_dark)

        # Draw timer
        if(time_limit > 0 and mode == "2-player"):
            white_coord = (0,0)
            black_coord = (0,0)
            if not flipped:
                white_coord = get_coord(flipped, (0,0))
                black_coord = get_coord(flipped, (0,7))
            else:
                white_coord = get_coord(flipped, (7,0))
                black_coord = get_coord(flipped, (7,7))
            white_coord = (white_coord[0] - 175, white_coord[1])
            black_coord = (black_coord[0] - 175, black_coord[1])
            white_box = Rect(white_coord, (125, 50))
            black_box = Rect(black_coord, (125, 50))
            screen.draw.filled_rect(white_box, color=(255,255,255))
            screen.draw.filled_rect(black_box, color=(0,0,0))
            screen.blit('stopwatch_b', (white_coord[0]+PAD_TEXT, white_coord[1]+9))
            screen.blit('stopwatch_w', (black_coord[0]+PAD_TEXT, black_coord[1]+9))
            screen.draw.text(time_white.get_time(), color=(0,0,0), right=white_box.right-PAD_TEXT, centery=white_box.centery, fontsize=36)
            screen.draw.text(time_black.get_time(), color=(255,255,255), right=black_box.right-PAD_TEXT, centery=black_box.centery, fontsize=36)

        # Draw taken pieces
        anchor_w = (0,0)
        anchor_b = (0,0)
        if not flipped:
            anchor_w = get_coord(flipped, (0,7))
            anchor_b = get_coord(flipped, (0,0))
            anchor_w = (anchor_w[0] - 175, anchor_w[1] + 75)
            anchor_b = (anchor_b[0] - 175, anchor_b[1] - 75)
            counter = 0
            for i in taken_pieces_w:
                for j in range(taken_pieces_w[i]):
                    # Drawing them in rows of five, putting all the same types of pieces together
                    screen.blit(name_to_pic(f"{i}w"), (anchor_w[0]+(counter%5)*25, anchor_w[1]+(counter//5)*25))
                    counter += 1
            counter = 0
            for i in taken_pieces_b:
                for j in range(taken_pieces_b[i]):
                    screen.blit(name_to_pic(f"{i}b"), (anchor_b[0]+(counter%5)*25, anchor_b[1]-(counter//5)*25))
                    counter += 1
        else:
            anchor_w = get_coord(flipped, (7,7))
            anchor_b = get_coord(flipped, (7,0))
            anchor_w = (anchor_w[0] - 175, anchor_w[1] - 75)
            anchor_b = (anchor_b[0] - 175, anchor_b[1] + 75)
            counter = 0
            for i in taken_pieces_w:
                for j in range(taken_pieces_w[i]):
                    screen.blit(name_to_pic(f"{i}w"), (anchor_w[0]+(counter%5)*25, anchor_w[1]-(counter//5)*25))
                    counter  += 1
            counter = 0
            for i in taken_pieces_b:
                for j in range(taken_pieces_b[i]):
                    screen.blit(name_to_pic(f"{i}b"), (anchor_b[0]+(counter%5)*25, anchor_b[1]+(counter//5)*25))
                    counter += 1

        # Draw game message
        screen.draw.text(game_message, center=(WIDTH/2, 40), fontsize=72, color=text_light)

        # Draw highlighted/selected square
        if (square is not None and selected is not None):
            if not flipped:
                screen.draw.filled_rect(board[square[0]][square[1]], highlight)
            else:
                screen.draw.filled_rect(board[7 - square[0]][7 - square[1]], highlight)

        # Draw pieces
        for key in actors:
            actors[key].draw()

        # Draw move indicators
        for i in highlighted_moves:
            # Get the coordinates of the middle of the square
            temp = get_coord(flipped, i[0])
            coord = (temp[0] + int(TILE_SIZE / 2), temp[1] + int(TILE_SIZE / 2))
            # If it's not a taking move, draw a dot
            if (i[1] == 0):
                screen.draw.filled_circle(coord, int(TILE_SIZE / 6), highlight)
            # If it's a taking move, draw a circle around the piece
            else:
                # I don't know how else to make the circle thicker other than drawing multiple circles lol
                r = int(TILE_SIZE / 2)
                for i in range(4):
                    screen.draw.circle(coord, r-i, highlight)

        # White promotion selection (draw the options)
        if (state == "promotion_w"):
            temp = (WIDTH/2-2*TILE_SIZE, (HEIGHT-8*TILE_SIZE)/2-TILE_SIZE)
            r = Rect(temp, (4*TILE_SIZE, TILE_SIZE))
            screen.draw.filled_rect(r, highlight)
            screen.blit('knight_w', temp)
            screen.blit('bishop_w', (temp[0]+TILE_SIZE, temp[1]))
            screen.blit('rook_w', (temp[0]+2*TILE_SIZE, temp[1]))
            screen.blit('queen_w', (temp[0]+3*TILE_SIZE, temp[1]))

        # Black promotion selection (draw the options)
        elif (state == "promotion_b"):
            temp = (WIDTH/2-2*TILE_SIZE, (HEIGHT-8*TILE_SIZE)/2-TILE_SIZE)
            r = Rect(temp, (4*TILE_SIZE, TILE_SIZE))
            screen.draw.filled_rect(r, highlight)
            screen.blit('knight_b', temp)
            screen.blit('bishop_b', (temp[0]+TILE_SIZE, temp[1]))
            screen.blit('rook_b', (temp[0]+2*TILE_SIZE, temp[1]))
            screen.blit('queen_b', (temp[0]+3*TILE_SIZE, temp[1]))

        # White wins (draw game over message)
        elif(state == "win_w"):
            r = Rect(WIDTH/2-150, HEIGHT/2-100, 300, 200)
            screen.draw.filled_rect(r, highlight)
            screen.draw.text("White wins!", center=(WIDTH/2, HEIGHT/2-50), fontsize=48, color=text_dark)
            screen.draw.text(f"By {win}", center=(WIDTH/2, HEIGHT/2-10), fontsize=36, color=text_dark)
            screen.draw.text("Click anywhere to return to main menu", center=(WIDTH/2, HEIGHT/2+75), fontsize=24, color=text_dark, width=250)

        # Black wins (draw game over message)
        elif(state == "win_b"):
            r = Rect(WIDTH/2-150, HEIGHT/2-100, 300, 200)
            screen.draw.filled_rect(r, highlight)
            screen.draw.text("Black wins!", center=(WIDTH/2, HEIGHT/2-50), fontsize=48, color=text_dark)
            screen.draw.text(f"By {win}", center=(WIDTH/2, HEIGHT/2-10), fontsize=36, color=text_dark)
            screen.draw.text("Click anywhere to return to main menu", center=(WIDTH/2, HEIGHT/2+75), fontsize=24, color=text_dark, width=250)

        # Draw (draw game over message)
        elif(state == "draw"):
            r = Rect(WIDTH/2-150, HEIGHT/2-100, 300, 200)
            screen.draw.filled_rect(r, highlight)
            screen.draw.text("Draw", center=(WIDTH/2, HEIGHT/2-50), fontsize=48, color=text_dark)
            screen.draw.text(f"By {win}", center=(WIDTH/2, HEIGHT/2-10), fontsize=36, color=text_dark)
            screen.draw.text("Click anywhere to return to main menu", center=(WIDTH/2, HEIGHT/2+75), fontsize=24, color=text_dark, width=250)


def update():
    '''
    This function is automatically called by pygame zero at a set interval of time, and draw() is called after update is complete.
    It is supposed to update once every 1/60 seconds, but it seems to be a little faster than that.
    The game message and timer are updated here, as well as moving the piece and recognizing when the computer moves (so it moves instantaneously after player moves).
    Args: None
    Returns: None
    '''
    # I realized that global only needs to be decalred for the variables that need to be changed
    # When reading, python automatically considers it as global if not found locally
    global game_message
    global state
    global win
    global pieces
    global game
    global move
    global taken_pieces_w
    global taken_pieces_b
    global square
    global selected
    global highlighted_moves

    # Set the game message if there is a draw request
    if(win == "draw_w"):
        if(turn == 'w'):
            game_message = "Requested a draw"
        else:
            game_message = "Opponent requested a draw"
    elif(win == "draw_b"):
        if(turn == 'b'):
            game_message = "Requested a draw"
        else:
            game_message = "Opponent requested a draw"
    else:
        game_message = ""

    # Count the time (tick the clock)
    if(time_limit > 0):
        if(state == "game" and mode == "2-player" and not stop):
            if(turn == 'w'):
                if time_white.is_zero():
                    win = "timeout"
                    state = "win_b"
                else:
                    time_white.minus_time(0,0,1)
            else:
                if time_black.is_zero():
                    win = "timeout"
                    state = "win_w"
                else:
                    time_black.minus_time(0,0,1)

    # This means it's the computer's move
    if(state == "game" and mode == "1-player" and turn != player and not stop):
        # Calcualte the computer's move, return a Move object is better
        move, score = get_best_move(pieces, game, piecenum_w, piecenum_b, history[-1], turn, difficulty)
        selected = move.name
        # Save this into global variable so can access later during promotion phase
        promote = move.special

    # Move the piece if a move was made
    if(move is not None):
        # If enpassant, the taken piece is not actually on the square that we move to
        if(move.special == 'e'):
            # If the move is going to the 6th rank, it means white pawn is taking black pawn
            if(move.end[1] == 5):
                # The actual pawn is behind the move, so -1 to the y coordinate
                move.taken = game[move.end[0]][move.end[1]-1]
                # Need to remove from the game, since not overwritten
                game[move.end[0]][move.end[1]-1] = ""
            # Black pawn is taking white pawn
            elif(move.end[1] == 2):
                # The actual pawn is behind the move, so +1 to the y coordinate (black is reversed)
                move.taken = game[move.end[0]][move.end[1]+1]
                game[move.end[0]][move.end[1]+1] = ""

        # Taking a piece
        if(move.taken is not None):
            # Record the state of the taken piece
            move.t_has_moved = pieces[move.taken].has_moved
            # Add the piece to taken list (draw it on the side)
            if(move.taken[-1] == 'w'):
                taken_pieces_w[move.taken[0]] += 1
            else:
                taken_pieces_b[move.taken[0]] += 1
            # Remove the actor from the board
            del actors[move.taken]

        # Pretend the move was played (calculate the next board)
        # No need to check promotion, because the effects only happen next turn
        # (if a piece is promoted this turn, it cannot move until the next turn, so it can be treated as just a normal move forward)
        results = next_board(pieces, game, move, None, None, turn)
        pieces = results[0]
        game = results[1]

        # Castling (just need to account for the rook being moved since king already moved)
        # Castling is a predetermined move, has to be those exact squares and pieces
        if(move.special == 'O_O_Ow'):  # White O_O_O
            coords = get_coord(flipped, (3, 0))
            pieces["r0w"].has_moved = True
            animate(actors["r0w"], topleft=coords, tween='linear', duration=ANIMATION_TIME, on_finished=None)
        elif(move.special == 'O_Ow'):  # White O_O
            coords = get_coord(flipped, (5, 0))
            pieces["r1w"].has_moved = True
            animate(actors["r1w"], topleft=coords, tween='linear', duration=ANIMATION_TIME, on_finished=None)
        elif(move.special == 'O_O_Ob'):  # Black O_O_O
            coords = get_coord(flipped, (3, 7))
            pieces["r0b"].has_moved = True
            animate(actors["r0b"], topleft=coords, tween='linear', duration=ANIMATION_TIME, on_finished=None)
        elif(move.special == 'O_Ob'):  # Black O_O
            coords = get_coord(flipped, (5, 7))
            pieces["r1b"].has_moved = True
            animate(actors["r1b"], topleft=coords, tween='linear', duration=ANIMATION_TIME, on_finished=None)

        # Promotion (will be dealt with after animation ends)
        if(move.name[0] == 'p'):
            # White's pawn has reached the last rank (pawns cannot move backwards)
            if(move.end[1] == 7):
                clock.schedule(promotion_w, ANIMATION_TIME)
                move.special = 'p'
            # Black's pawn has reached the last rank (pawns cannot move backwards)
            elif(move.end[1] == 0):
                clock.schedule(promotion_b, ANIMATION_TIME)
                move.special = 'p'

        # Set has_moved to True (If the king or the rook moves, it loses its castling rights)
        pieces[move.name].has_moved = True
        # Log the move into the move history
        history.append(move)

        # Draw the animation (move the piece) and stop taking inputs during this time
        coords = get_coord(flipped, move.end)
        animate(actors[move.name], topleft=coords, tween='linear', duration=ANIMATION_TIME, on_finished=unpause)
        pause()

        # Reset/unselect (the turn is updated in unpause so board can flip after animation is over)
        square = None
        selected = None
        move = None
        highlighted_moves = []


def on_mouse_up(pos, button):
    '''
    This function is automatically called by pygame zero when a mouse button is released.
    The parameters record where the click happened and what mouse button was used.
    It controls what variables the buttons change when pressed, as well as determining what the palyer wants to do.
    Args: None
    Returns: None
    '''
    global selected
    global square
    global highlighted_moves
    global game
    global board
    global pieces
    global actors
    global move
    global stop
    global piecenum_w
    global piecenum_b
    global history
    global turn
    global flipped
    global state
    global mode
    global difficulty
    global time_limit
    global time_back
    global win
    global promote
    global player

    if (button == mouse.LEFT):
        # In the main menu
        if(state == "menu"):
            # Setup the board depending on game mode (In the future, may have different setups)
            if btn_1plyr.collidepoint(pos):
                setup()
                state = "difficulty"
                mode = "1-player"
            if btn_2plyr.collidepoint(pos):
                setup()
                state = "time"
                mode = "2-player"
            if btn_exit.collidepoint(pos):
                sys.exit()

        # In the difficulty selection screen
        elif(state == "difficulty"):
            for i in range(len(btn_lv)):
                if(btn_lv[i].collidepoint(pos)):
                    # Set the difficulty to the corresponding button the player clicked on
                    difficulty = i+1
                    # Need to flip the board if the palyer chose to play as black
                    if(player == 'b'):
                        flipped = True
                        for key in pieces:
                            actors[key].topleft = get_coord(flipped, pieces[key].pos)
                    state = "game"
            if(btn_w.collidepoint(pos)):
                player = 'w'
            elif(btn_b.collidepoint(pos)):
                player = 'b'

        # In the time selection screen
        elif(state == "time"):
            # Add 1 to the time limit when the up arrow is clicked
            if(btn_inc_total.collidepoint(pos)):
                time_limit += 1
            # Subtract 1 to the time limit when the down arrow is clicked
            elif(btn_dec_total.collidepoint(pos)):
                if(time_limit > 0):
                    time_limit -= 1
            # Add 1 to the time back when the other up arrow is clicked
            elif(btn_inc_back.collidepoint(pos)):
                time_back += 1
            # Subtract 1 to the time back when the other down arrow is clicked
            elif(btn_dec_back.collidepoint(pos)):
                if(time_back > 0):
                    time_back -= 1
            # Set the time that the player chose, record it to memory
            elif(btn_next.collidepoint(pos)):
                time_white.set_time(time_limit, 0, 0)
                time_black.set_time(time_limit, 0, 0)
                state = "game"

        # Regular game logic
        elif(state == "game" and not stop):
            # Click was within the chess board
            if(pos[0] >= PAD_LEFT and pos[0] < PAD_LEFT + 8 * TILE_SIZE and pos[1] >= PAD_TOP and pos[1] < PAD_TOP + 8 * TILE_SIZE):
                # The square that was clicked
                square = get_pos(flipped, pos)
                move = None

                # If it's a player's move
                if(mode == "2-player" or turn == player):
                    for i in highlighted_moves:
                        if(pos_equals(square, i[0])):
                            move = Move(selected, pieces[selected].pos, i[0], get_piece(game, i[0]), i[2], pieces[selected].has_moved, None)
                            break

                # Update the selected piece (if a move was not made)
                if(move is None):
                    selected = get_piece(game, square)

                    # Highlight the selected piece's moves
                    if(selected is not None):
                        # Has to be your own piece, not opponenet's piece
                        if(selected[-1] == turn):
                            # The moves that are displayed on screen
                            highlighted_moves = pieces[selected].moves
                        else:
                            highlighted_moves = []
                            selected = None
                    else:
                        highlighted_moves = []

            # Clicked on resign
            elif(btn_resign.collidepoint(pos)):
                if(turn == 'w'):
                    state = "win_b"
                else:
                    state = "win_w"
                win = "resignation"

            # Clicked on draw
            elif(btn_draw.collidepoint(pos)):
                # If opponent requested a draw last turn and you clicked draw, then draw the match
                if(win == "draw_w" and turn == 'b'):
                    state = "draw"
                    win = "agreement"
                elif(win == "draw_b" and turn == 'w'):
                    state = "draw"
                    win = "agreement"
                else:
                    win = f"draw_{turn}"

            # Clicked on take back (no animation)
            elif(btn_take_back.collidepoint(pos)):
                num = 1
                # Need to run this twice because the computer's move needs to be taken back as well
                if(mode == "1-player"):
                    num = 2
                for i in range(num):
                    # Don't want index out of bounds error (must always keep that one placeholder move)
                    if(len(history) > 1):
                        back = history[-1]
                        # If last back was a promotion
                        if(back.special == 'p'):
                            # The pawn is gone, so have to re-create it
                            actors[back.name] = Actor(name_to_pic(back.name))
                            pieces[back.name] = Piece(back.start)
                            # Delete the new promoted piece
                            promoted_piece = get_piece(game, back.end)
                            del pieces[promoted_piece]
                            del actors[promoted_piece]
                            # Reset the counters
                            if(back.name[-1] == 'w'):
                                piecenum_w[promoted_piece[0]] -= 1
                            else:
                                piecenum_b[promoted_piece[0]] -= 1
                        # Put the moved piece back where it came from
                        game[back.start[0]][back.start[1]] = back.name
                        pieces[back.name].pos = back.start
                        pieces[back.name].has_moved = back.has_moved
                        actors[back.name].topleft = get_coord(flipped, back.start)
                        # If a piece was taken, put the taken piece back
                        if(back.taken is not None):
                            taken_pos = back.end
                            if(back.special == 'e'):
                                # If white enpassant, then the black pawn gets put back behind where the white pawn ended up
                                if(back.name[-1] == 'w'):
                                    taken_pos = (back.end[0], back.end[1]-1)
                                # Black pawn is reversed, so +1
                                else:
                                    taken_pos = (back.end[0], back.end[1]+1)
                                # Nothing was the spot where the pawn was had no piece
                                game[back.end[0]][back.end[1]] = ""
                            # Put the taken piece back to where it used to be
                            game[taken_pos[0]][taken_pos[1]] = back.taken
                            # Re-add the taken piece to memory
                            pieces[back.taken] = Piece(taken_pos)
                            pieces[back.taken].has_moved = back.t_has_moved
                            actors[back.taken] = Actor(name_to_pic(back.taken))
                            actors[back.taken].topleft = get_coord(flipped, taken_pos)
                            # Remove it from taken pieces (don't draw it on the side)
                            if(back.taken[-1] == 'w'):
                                taken_pieces_w[back.taken[0]] -= 1
                            else:
                                taken_pieces_b[back.taken[0]] -= 1
                        # If no piece was taken, then the spot where the piece was is empty
                        else:
                            game[back.end[0]][back.end[1]] = ""
                        # Castling is pre-determined, and king was already accounted for
                        if(back.special == 'O_O_Ow'):
                            game[0][0] = "r0w"
                            game[3][0] = ""
                            pieces["r0w"].pos = (0,0)
                            actors["r0w"].topleft = get_coord(flipped, (0,0))
                            # If a castle happened, that means the rook definitely hasn't moved before
                            pieces["r0w"].has_moved = False
                        elif(back.special == 'O_Ow'):
                            game[7][0] = "r1w"
                            game[5][0] = ""
                            pieces["r1w"].pos = (7,0)
                            actors["r1w"].topleft = get_coord(flipped, (7,0))
                            pieces["r1w"].has_moved = False
                        elif(back.special == 'O_O_Ob'):
                            game[0][7] = "r0b"
                            game[3][7] = ""
                            pieces["r0b"].pos = (0,7)
                            actors["r0b"].topleft = get_coord(flipped, (0,7))
                            pieces["r0b"].has_moved = False
                        elif(back.special == 'O_Ob'):
                            game[7][7] = "r1b"
                            game[5][7] = ""
                            pieces["r1b"].pos = (7,7)
                            actors["r1b"].topleft = get_coord(flipped, (7,7))
                            pieces["r1b"].has_moved = False

                        # Remove that move from the history (it never happened)
                        del history[-1]
                        # De-select anything that's still highlighted
                        square = None
                        selected = None
                        highlighted_moves = []
                        # Don't reward player whose turn got skipped with extra time
                        # (ending turn rewards them with time, so both black and white need to remove time)
                        # Unfortunantly, this does not account for time lost spent clicking the button during the skipped player's turn
                        time_black.minus_time(0, time_back, 0)
                        time_white.minus_time(0, time_back, 0)
                        # Let the player who took back do another move (by ending the current turn without any moves)
                        end_turn()

            # Click was outisde the board and not on one of the buttons
            else:
                # De-select and remove highlights/move indicators
                square = None
                selected = None
                highlighted_moves = []

        # White promotion selection
        elif(state == "promotion_w"):
            name = None

            # If predetermined, then set the name
            if(promote == 'pn'):
                name = f"n{piecenum_w['n']}w"
            elif(promote == 'pb'):
                name = f"b{piecenum_w['b']}w"
            elif(promote == 'pr'):
                name = f"r{piecenum_w['r']}w"
            elif(promote == 'pq'):
                name = f"q{piecenum_w['q']}w"
            # If not predetermined, then choose a piece to promote to
            else:
                temp = (WIDTH/2-2*TILE_SIZE, (HEIGHT-8*TILE_SIZE)/2-TILE_SIZE)
                # Knight is chosen
                if(pos[0] > temp[0] and pos[0] < temp[0] + TILE_SIZE and pos[1] > temp[1] and pos[1] < temp[1] + TILE_SIZE):
                    name = f"n{piecenum_w['n']}w"
                # Bishop is chosen
                elif(pos[0] > temp[0] + TILE_SIZE and pos[0] < temp[0] + 2*TILE_SIZE and pos[1] > temp[1] and pos[1] < temp[1] + TILE_SIZE):
                    name = f"b{piecenum_w['b']}w"
                # Rook is chosen
                elif(pos[0] > temp[0] + 2*TILE_SIZE and pos[0] < temp[0] + 3*TILE_SIZE and pos[1] > temp[1] and pos[1] < temp[1] + TILE_SIZE):
                    name = f"r{piecenum_w['r']}w"
                # Queen is chosen
                elif(pos[0] > temp[0] + 3*TILE_SIZE and pos[0] < temp[0] + 4*TILE_SIZE and pos[1] > temp[1] and pos[1] < temp[1] + TILE_SIZE):
                    name = f"q{piecenum_w['q']}w"

            # Something was chosen or predetermined
            if(name is not None):
                # Remove the pawn (it was the last moved piece)
                pawn = get_piece(game, history[-1].end)
                del pieces[pawn]
                del actors[pawn]
                # Place the new piece in memory
                game[history[-1].end[0]][history[-1].end[1]] = name
                piecenum_w[name[0]] += 1
                # Draw the new piece
                pieces[name] = Piece(history[-1].end)
                actors[name] = Actor(name_to_pic(name))
                actors[name].topleft = get_coord(flipped, history[-1].end)
                # Reset to the game after selection
                state = "game"
                end_turn()

        # Black promotion selection
        elif(state == "promotion_b"):
            name = None

            if(promote == 'pn'):
                name = f"n{piecenum_b['n']}b"
            elif(promote == 'pb'):
                name = f"b{piecenum_b['b']}b"
            elif(promote == 'pr'):
                name = f"r{piecenum_b['r']}b"
            elif(promote == 'pq'):
                name = f"q{piecenum_b['q']}b"
            else:
                temp = (WIDTH/2-2*TILE_SIZE, (HEIGHT-8*TILE_SIZE)/2-TILE_SIZE)
                # Knight is chosen
                if(pos[0] > temp[0] and pos[0] < temp[0] + TILE_SIZE and pos[1] > temp[1] and pos[1] < temp[1] + TILE_SIZE):
                    name = f"n{piecenum_b['n']}b"
                # Bishop is chosen
                elif(pos[0] > temp[0] + TILE_SIZE and pos[0] < temp[0] + 2*TILE_SIZE and pos[1] > temp[1] and pos[1] < temp[1] + TILE_SIZE):
                    name = f"b{piecenum_b['b']}b"
                # Rook is chosen
                elif(pos[0] > temp[0] + 2*TILE_SIZE and pos[0] < temp[0] + 3*TILE_SIZE and pos[1] > temp[1] and pos[1] < temp[1] + TILE_SIZE):
                    name = f"r{piecenum_b['r']}b"
                # Queen is chosen
                elif(pos[0] > temp[0] + 3*TILE_SIZE and pos[0] < temp[0] + 4*TILE_SIZE and pos[1] > temp[1] and pos[1] < temp[1] + TILE_SIZE):
                    name = f"q{piecenum_b['q']}b"

            # Something was chosen or predetermined
            if(name is not None):
                pawn = get_piece(game, history[-1].end)
                del pieces[pawn]
                del actors[pawn]
                game[history[-1].end[0]][history[-1].end[1]] = name
                piecenum_b[name[0]] += 1
                pieces[name] = Piece(history[-1].end)
                actors[name] = Actor(name_to_pic(name))
                actors[name].topleft = get_coord(flipped, history[-1].end)
                state = "game"
                end_turn()

        # If someone wins or draws, when click, just go to main menu
        elif(state == "win_w"):
            state = "menu"

        elif(state == "win_b"):
            state = "menu"

        elif(state == "draw"):
            state = "menu"



pgzrun.go()
