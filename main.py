import pygame
import sys
from pygame.locals import *
import ctypes
import copy
import time


# Window display variables -------------------------------------------
def convert_to_supported_resolution(x, y):
    res_x = (x // 8) * 8
    res_y = (y // 8) * 8
    print("Window resolution:", res_x, res_y)
    return res_x, res_y


disp_x, disp_y = convert_to_supported_resolution(1000, 700)
ctypes.windll.user32.SetProcessDPIAware()
window = pygame.display.set_mode((disp_x, disp_y))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
FPS = 240

# Initializing board reference variables ----------------------------------
board_size = min(disp_x, disp_y)
b_pos_x = (disp_x - board_size) / 2
b_pos_y = (disp_y - board_size) / 2
square_size = board_size / 8
scale = 0.8
# --------------------------------
DEFAULT_tup = (-500, -500)
DEFAULT_int = -500

# Import of Images
dark_sqr = pygame.image.load('images\\darksqr.png').convert_alpha()
dark_sqr = pygame.transform.smoothscale(dark_sqr, (square_size, square_size)).convert_alpha()
light_sqr = pygame.image.load('images\\lightsqr.png').convert_alpha()
light_sqr = pygame.transform.smoothscale(light_sqr, (square_size, square_size)).convert_alpha()
w_p_img = pygame.image.load('images\\wpawn.png').convert_alpha()
w_pawn_img = pygame.transform.smoothscale(w_p_img, (square_size * 0.87, square_size * 0.87)).convert_alpha()
b_p_img = pygame.image.load('images\\bpawn.png').convert_alpha()
b_pawn_img = pygame.transform.smoothscale(b_p_img, (square_size * 0.87, square_size * 0.87)).convert_alpha()
w_n_img = pygame.image.load('images\\wknight.png').convert_alpha()
w_knight_img = pygame.transform.smoothscale(w_n_img, (square_size * scale, square_size * scale)).convert_alpha()
b_n_img = pygame.image.load('images\\bknight.png').convert_alpha()
b_knight_img = pygame.transform.smoothscale(b_n_img, (square_size * scale, square_size * scale)).convert_alpha()
w_b_img = pygame.image.load('images\\wbishop.png').convert_alpha()
w_bishop_img = pygame.transform.smoothscale(w_b_img, (square_size * scale, square_size * scale)).convert_alpha()
b_b_img = pygame.image.load('images\\bbishop.png').convert_alpha()
b_bishop_img = pygame.transform.smoothscale(b_b_img, (square_size * scale, square_size * scale)).convert_alpha()
w_r_img = pygame.image.load('images\\wrook.png').convert_alpha()
w_rook_img = pygame.transform.smoothscale(w_r_img, (square_size * scale, square_size * scale)).convert_alpha()
b_r_img = pygame.image.load('images\\brook.png').convert_alpha()
b_rook_img = pygame.transform.smoothscale(b_r_img, (square_size * scale, square_size * scale)).convert_alpha()
w_q_img = pygame.image.load('images\\wqueen.png').convert_alpha()
w_queen_img = pygame.transform.smoothscale(w_q_img, (square_size * scale, square_size * scale)).convert_alpha()
b_q_img = pygame.image.load('images\\bqueen.png').convert_alpha()
b_queen_img = pygame.transform.smoothscale(b_q_img, (square_size * scale, square_size * scale)).convert_alpha()
w_k_img = pygame.image.load('images\\wking.png').convert_alpha()
w_king_img = pygame.transform.smoothscale(w_k_img, (square_size * scale, square_size * scale)).convert_alpha()
b_k_img = pygame.image.load('images\\bking.png').convert_alpha()
b_king_img = pygame.transform.smoothscale(b_k_img, (square_size * scale, square_size * scale)).convert_alpha()
sqr_highlight0 = pygame.image.load('images\\highlight0.png').convert_alpha()
sqr_highlight0 = pygame.transform.smoothscale(sqr_highlight0, (square_size, square_size)).convert_alpha()
sqr_highlight1 = pygame.image.load('images\\highlight1.png').convert_alpha()
sqr_highlight1 = pygame.transform.smoothscale(sqr_highlight1, (square_size, square_size)).convert_alpha()
choose_piece_img = pygame.image.load('images\\ChoosePieceHighlight.png').convert_alpha()
choose_piece_img = pygame.transform.scale(choose_piece_img, (square_size, square_size * 4)).convert_alpha()
prev_light = pygame.image.load('images\\prevlight.png').convert()
prev_light = pygame.transform.smoothscale(prev_light, (square_size, square_size)).convert()
prev_dark = pygame.image.load('images\\prevdark.png').convert()
prev_dark = pygame.transform.smoothscale(prev_dark, (square_size, square_size)).convert()
to_light = pygame.image.load('images\\tolight.png').convert()
to_light = pygame.transform.smoothscale(to_light, (square_size, square_size)).convert()
to_dark = pygame.image.load('images\\todark.png').convert()
to_dark = pygame.transform.smoothscale(to_dark, (square_size, square_size)).convert()

# Representation of board in code ------------------------------------
board = []
for squ_on_board in range(64):
    board.append([squ_on_board, 0])
previous_board_state = copy.deepcopy(board)
# --------------------------------------------------------------------
white_occupancy = [[], [], [], [], [], []]
black_occupancy = [[], [], [], [], [], []]
# --------------------------------------------------------------------
white_pawn_moves, black_pawn_moves = [], []
knight_moves = []
bishop_moves = []
rook_moves = []
queen_moves = []
king_moves = []
# Mapping pieces to array indexes
segment_map = {9: 0, 10: 1, 11: 2,
               12: 3, 13: 4, 14: 5,
               17: 0, 18: 1, 19: 2,
               20: 3, 21: 4, 22: 5}

# light and dark squares representation
light_dark = [0, 1, 0, 1, 0, 1, 0, 1,
              1, 0, 1, 0, 1, 0, 1, 0,
              0, 1, 0, 1, 0, 1, 0, 1,
              1, 0, 1, 0, 1, 0, 1, 0,
              0, 1, 0, 1, 0, 1, 0, 1,
              1, 0, 1, 0, 1, 0, 1, 0,
              0, 1, 0, 1, 0, 1, 0, 1,
              1, 0, 1, 0, 1, 0, 1, 0
              ]

# Representation of pieces in code -----------------------------------
pawn = 1
knight = 2
bishop = 3
rook = 4
queen = 5
king = 6
# --------------------------------
white = 8
black = 16

# Mapping piece images to their piece numbers for rendering -----------
piece_and_img = [(9, w_pawn_img), (10, w_knight_img), (11, w_bishop_img),
                 (12, w_rook_img), (13, w_queen_img), (14, w_king_img),
                 (17, b_pawn_img), (18, b_knight_img), (19, b_bishop_img),
                 (20, b_rook_img), (21, b_queen_img), (22, b_king_img)]


# Functions ------------------------------------------------------------
def get_square_coord(sq_index):
    rank = 1
    file = 1
    file_count = 1
    for sq in range(sq_index + 1):
        if file_count > 8:
            file_count = 1
            rank += 1
        if sq == sq_index:
            file = file_count
        file_count += 1
    square_coord_x = b_pos_x + (square_size * (file - 1))
    square_coord_y = b_pos_y + (square_size * (8 - rank))
    square_coord = [square_coord_x, square_coord_y]
    return square_coord


def get_square_index(ref_pos=DEFAULT_tup, file=DEFAULT_int, rank=DEFAULT_int):
    square_index = DEFAULT_int
    if ref_pos != DEFAULT_tup:
        for sq in range(64):
            square_coord = get_square_coord(sq)
            if square_coord[0] <= ref_pos[0] <= (square_coord[0] + square_size):
                if square_coord[1] <= ref_pos[1] <= (square_coord[1] + square_size):
                    square_index = sq
                    break
    if (1 <= file <= 8) and (1 <= rank <= 8):
        square_index = ((rank * 8) - (8 - file)) - 1
    return square_index


def get_file_n_rank(sq_index):
    rank = ((sq_index + 1) / 8)
    if rank > int(rank):
        rank = int(rank) + 1
    else:
        rank = int(rank)
    file = sq_index - (((rank - 1) * 8) - 1)
    return file, rank


# Note: Order that these moves are generated IMPORTANT for checking direction to stop movement when a piece is blocked
def initialize_white_pawn_moves():
    global white_pawn_moves
    temp_arr = [[], [], []]
    # Generating all possible squares white pawns can move to from each square
    for wp_sqr in range(64):
        wp_file, wp_rank = get_file_n_rank(wp_sqr)

        wp_f, wp_r = wp_file + 1, wp_rank + 1
        if wp_f in range(1, 9) and wp_r in range(1, 9):
            temp_arr[0].append(get_square_index(file=wp_f, rank=wp_r))
        wp_f, wp_r = wp_file + 0, wp_rank + 1
        if wp_f in range(1, 9) and wp_r in range(1, 9):
            temp_arr[1].append(get_square_index(file=wp_f, rank=wp_r))
        if wp_sqr in range(8, 16):
            wp_f, wp_r = wp_file + 0, wp_rank + 2
            temp_arr[1].append(get_square_index(file=wp_f, rank=wp_r))
        wp_f, wp_r = wp_file - 1, wp_rank + 1
        if wp_f in range(1, 9) and wp_r in range(1, 9):
            temp_arr[2].append(get_square_index(file=wp_f, rank=wp_r))
        white_pawn_moves.append(temp_arr)
        temp_arr = [[], [], []]


def initialize_black_pawn_moves():
    global black_pawn_moves
    temp_arr = [[], [], []]
    # Generating all possible squares black pawns can move to from each square
    for bp_sqr in range(64):
        bp_file, bp_rank = get_file_n_rank(bp_sqr)

        bp_f, bp_r = bp_file - 1, bp_rank - 1
        if bp_f in range(1, 9) and bp_r in range(1, 9):
            temp_arr[0].append(get_square_index(file=bp_f, rank=bp_r))
        bp_f, bp_r = bp_file + 0, bp_rank - 1
        if bp_f in range(1, 9) and bp_r in range(1, 9):
            temp_arr[1].append(get_square_index(file=bp_f, rank=bp_r))
        if bp_sqr in range(48, 56):
            bp_f, bp_r = bp_file + 0, bp_rank - 2
            temp_arr[1].append(get_square_index(file=bp_f, rank=bp_r))
        bp_f, bp_r = bp_file + 1, bp_rank - 1
        if bp_f in range(1, 9) and bp_r in range(1, 9):
            temp_arr[2].append(get_square_index(file=bp_f, rank=bp_r))
        black_pawn_moves.append(temp_arr)
        temp_arr = [[], [], []]


def initialize_knight_moves():
    global knight_moves
    temp_arr = []
    # Generating all possible squares the knight can jump to from each square
    for n_sqr in range(64):
        n_file, n_rank = get_file_n_rank(n_sqr)

        n_f, n_r = n_file + 2, n_rank + 1
        if n_f in range(1, 9) and n_r in range(1, 9):
            temp_arr.append(get_square_index(file=n_f, rank=n_r))
        n_f, n_r = n_file + 1, n_rank + 2
        if n_f in range(1, 9) and n_r in range(1, 9):
            temp_arr.append(get_square_index(file=n_f, rank=n_r))
        n_f, n_r = n_file + 2, n_rank - 1
        if n_f in range(1, 9) and n_r in range(1, 9):
            temp_arr.append(get_square_index(file=n_f, rank=n_r))
        n_f, n_r = n_file + 1, n_rank - 2
        if n_f in range(1, 9) and n_r in range(1, 9):
            temp_arr.append(get_square_index(file=n_f, rank=n_r))
        n_f, n_r = n_file - 2, n_rank + 1
        if n_f in range(1, 9) and n_r in range(1, 9):
            temp_arr.append(get_square_index(file=n_f, rank=n_r))
        n_f, n_r = n_file - 1, n_rank + 2
        if n_f in range(1, 9) and n_r in range(1, 9):
            temp_arr.append(get_square_index(file=n_f, rank=n_r))
        n_f, n_r = n_file - 2, n_rank - 1
        if n_f in range(1, 9) and n_r in range(1, 9):
            temp_arr.append(get_square_index(file=n_f, rank=n_r))
        n_f, n_r = n_file - 1, n_rank - 2
        if n_f in range(1, 9) and n_r in range(1, 9):
            temp_arr.append(get_square_index(file=n_f, rank=n_r))
        knight_moves.append(temp_arr)
        temp_arr = []


def initialize_bishop_moves():
    global bishop_moves
    temp_arr = [[], [], [], []]
    # Generating all possible squares the bishop can slide to from each square
    for b_sqr in range(64):
        b_file, b_rank = get_file_n_rank(b_sqr)

        b_f, b_r = b_file, b_rank
        while b_f in range(1, 9) and b_r in range(1, 9):
            b_f += 1
            b_r += 1
            if b_f in range(1, 9) and b_r in range(1, 9):
                temp_arr[0].append(get_square_index(file=b_f, rank=b_r))
        b_f, b_r = b_file, b_rank
        while b_f in range(1, 9) and b_r in range(1, 9):
            b_f -= 1
            b_r += 1
            if b_f in range(1, 9) and b_r in range(1, 9):
                temp_arr[1].append(get_square_index(file=b_f, rank=b_r))
        b_f, b_r = b_file, b_rank
        while b_f in range(1, 9) and b_r in range(1, 9):
            b_f -= 1
            b_r -= 1
            if b_f in range(1, 9) and b_r in range(1, 9):
                temp_arr[2].append(get_square_index(file=b_f, rank=b_r))
        b_f, b_r = b_file, b_rank
        while b_f in range(1, 9) and b_r in range(1, 9):
            b_f += 1
            b_r -= 1
            if b_f in range(1, 9) and b_r in range(1, 9):
                temp_arr[3].append(get_square_index(file=b_f, rank=b_r))
        bishop_moves.append(temp_arr)
        temp_arr = [[], [], [], []]


def initialize_rook_moves():
    global rook_moves
    temp_arr = [[], [], [], []]
    # Generating all possible squares the rook can slide to from each square
    for r_sqr in range(64):
        r_file, r_rank = get_file_n_rank(r_sqr)

        r_f, r_r = r_file, r_rank
        while r_f in range(1, 9) and r_r in range(1, 9):
            r_f += 1
            r_r += 0
            if r_f in range(1, 9) and r_r in range(1, 9):
                temp_arr[0].append(get_square_index(file=r_f, rank=r_r))
        r_f, r_r = r_file, r_rank
        while r_f in range(1, 9) and r_r in range(1, 9):
            r_f += 0
            r_r += 1
            if r_f in range(1, 9) and r_r in range(1, 9):
                temp_arr[1].append(get_square_index(file=r_f, rank=r_r))
        r_f, r_r = r_file, r_rank
        while r_f in range(1, 9) and r_r in range(1, 9):
            r_f -= 1
            r_r += 0
            if r_f in range(1, 9) and r_r in range(1, 9):
                temp_arr[2].append(get_square_index(file=r_f, rank=r_r))
        r_f, r_r = r_file, r_rank
        while r_f in range(1, 9) and r_r in range(1, 9):
            r_f += 0
            r_r -= 1
            if r_f in range(1, 9) and r_r in range(1, 9):
                temp_arr[3].append(get_square_index(file=r_f, rank=r_r))
        rook_moves.append(temp_arr)
        temp_arr = [[], [], [], []]


def initialize_queen_moves():
    global queen_moves
    temp_arr = [[], [], [], [], [], [], [], []]
    # Generating all possible squares the queen can slide to from each square
    for q_sqr in range(64):
        q_file, q_rank = get_file_n_rank(q_sqr)

        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 1
            q_r += 0
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr[0].append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 1
            q_r += 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr[1].append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 0
            q_r += 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr[2].append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f -= 1
            q_r += 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr[3].append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f -= 1
            q_r += 0
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr[4].append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f -= 1
            q_r -= 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr[5].append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 0
            q_r -= 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr[6].append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 1
            q_r -= 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr[7].append(get_square_index(file=q_f, rank=q_r))
        queen_moves.append(temp_arr)
        temp_arr = [[], [], [], [], [], [], [], []]


def initialize_king_moves():
    global king_moves
    temp_arr = []
    # Generating all possible squares the king can move to from each square
    for k_sqr in range(64):
        k_file, k_rank = get_file_n_rank(k_sqr)

        k_f, k_r = k_file + 1, k_rank + 0
        if k_f in range(1, 9) and k_r in range(1, 9):
            temp_arr.append(get_square_index(file=k_f, rank=k_r))
        k_f, k_r = k_file + 1, k_rank + 1
        if k_f in range(1, 9) and k_r in range(1, 9):
            temp_arr.append(get_square_index(file=k_f, rank=k_r))
        k_f, k_r = k_file + 0, k_rank + 1
        if k_f in range(1, 9) and k_r in range(1, 9):
            temp_arr.append(get_square_index(file=k_f, rank=k_r))
        k_f, k_r = k_file - 1, k_rank + 1
        if k_f in range(1, 9) and k_r in range(1, 9):
            temp_arr.append(get_square_index(file=k_f, rank=k_r))
        k_f, k_r = k_file - 1, k_rank + 0
        if k_f in range(1, 9) and k_r in range(1, 9):
            temp_arr.append(get_square_index(file=k_f, rank=k_r))
        k_f, k_r = k_file - 1, k_rank - 1
        if k_f in range(1, 9) and k_r in range(1, 9):
            temp_arr.append(get_square_index(file=k_f, rank=k_r))
        k_f, k_r = k_file + 0, k_rank - 1
        if k_f in range(1, 9) and k_r in range(1, 9):
            temp_arr.append(get_square_index(file=k_f, rank=k_r))
        k_f, k_r = k_file + 1, k_rank - 1
        if k_f in range(1, 9) and k_r in range(1, 9):
            temp_arr.append(get_square_index(file=k_f, rank=k_r))
        king_moves.append(temp_arr)
        temp_arr = []


def load_fen(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
    sq = 7
    slash_count = 1
    piece = {"p": 1, "n": 2, "b": 3, "r": 4, "q": 5, "k": 6}
    fen_reverse = [""] * len(fen)
    fen_size = len(fen) - 1
    for a in fen:
        fen_reverse[fen_size] = a
        fen_size -= 1
    for b in fen_reverse:
        if b.isupper():
            board[sq][1] = piece[b.lower()] + white
            sq -= 1
        if b.islower():
            board[sq][1] = piece[b] + black
            sq -= 1
        if b.isnumeric():
            val_to_num = int(b)
            for c in range(val_to_num):
                board[sq][1] = 0
                sq -= 1
        if b == '/':
            slash_count += 1
            sq = (8 * slash_count) - 1


def initialize_white_occupancy():
    global white_occupancy
    white_occupancy = [[], [], [], [], [], []]
    for p_n_pos in board:
        square, piece = p_n_pos[0], p_n_pos[1]
        if piece > 0:
            if piece == 9:
                white_occupancy[0].append(square)
            if piece == 10:
                white_occupancy[1].append(square)
            if piece == 11:
                white_occupancy[2].append(square)
            if piece == 12:
                white_occupancy[3].append(square)
            if piece == 13:
                white_occupancy[4].append(square)
            if piece == 14:
                white_occupancy[5].append(square)


def initialize_black_occupancy():
    global black_occupancy
    black_occupancy = [[], [], [], [], [], []]
    for p_n_pos in board:
        square, piece = p_n_pos[0], p_n_pos[1]
        if piece > 0:
            if piece == 17:
                black_occupancy[0].append(square)
            if piece == 18:
                black_occupancy[1].append(square)
            if piece == 19:
                black_occupancy[2].append(square)
            if piece == 20:
                black_occupancy[3].append(square)
            if piece == 21:
                black_occupancy[4].append(square)
            if piece == 22:
                black_occupancy[5].append(square)


def draw_board():
    for square in range(64):
        file, rank = get_file_n_rank(square)
        if (file + rank) % 2 == 0:
            window.blit(dark_sqr, get_square_coord(square))
        else:
            window.blit(light_sqr, get_square_coord(square))


def draw_piece(piece, square_index, specific=False, coord=(0, 0)):
    if piece != 0:
        img = b_king_img
        p_coord = DEFAULT_tup
        for pni in piece_and_img:
            if pni[0] == piece:
                img = pni[1]
        if specific:
            p_coord = (coord[0] - (square_size * 1.021 / 2), coord[1] - (square_size * 1.021 / 2))
            img = pygame.transform.smoothscale(img, (square_size * 1.021, square_size * 1.021)).convert_alpha()
        if not specific:
            piece_coord_x = get_square_coord(square_index)[0] + ((1 - scale) * square_size / 2) + 1
            piece_coord_y = get_square_coord(square_index)[1] + ((1 - scale) * square_size / 2) + 1
            p_coord = [piece_coord_x, piece_coord_y]
            if piece == 9 or piece == 17:
                p_coord[0] = get_square_coord(square_index)[0] + ((1 - 0.87) * square_size / 2) + 1
                p_coord[1] = piece_coord_y + (square_size * 0.015)
        window.blit(img, p_coord)


def render_pieces(omit=DEFAULT_int):
    omit_square = omit
    attacked = attacked_squares()
    check, doublecheck = False, False
    pins = pin_n_check_resolves(False)
    check_resolve = ""
    if previous_board_state != board:
        from_here, to_there, from_here_index, to_there_index, square_counter = "", "", "", "", 0
        for sqr in previous_board_state:
            if sqr != board[square_counter] and board[square_counter][1] == 0:
                from_here = get_square_coord(sqr[0])
                from_here_index = previous_board_state[square_counter][0]
            if sqr != board[square_counter] and board[square_counter][1] != 0:
                to_there = get_square_coord(sqr[0])
                to_there_index = board[square_counter][0]
            square_counter += 1
        # ---------------------------------------------------------
        if from_here != "" and to_there != "":
            if light_dark[from_here_index] == 1:
                window.blit(to_light, from_here)
            else:
                window.blit(to_dark, from_here)
            if light_dark[to_there_index] == 1:
                window.blit(prev_light, to_there)
            else:
                window.blit(prev_dark, to_there)

    if omit != DEFAULT_int and board[omit][1] != 0:
        if turn_to_move == "w" and board[omit][1] <= 14:
            s_x = get_square_coord(omit_square)[0]
            s_y = get_square_coord(omit_square)[1]
            window.blit(sqr_highlight0, (s_x, s_y))
        if turn_to_move == "b" and board[omit][1] >= 17:
            s_x = get_square_coord(omit_square)[0]
            s_y = get_square_coord(omit_square)[1]
            window.blit(sqr_highlight0, (s_x, s_y))
        # Don't Highlight any moves if there is a pawn to promote
        if not pawn_to_promote():
            if turn_to_move == "w":
                if attacked[white_king_pos] == 1:
                    check = True
                    pins, check_resolve = pin_n_check_resolves(True)
                if attacked[white_king_pos] > 1:
                    doublecheck = True

                for piece in range(6):
                    if piece == 5:
                        if board[omit][1] == 9 and not doublecheck:
                            for sqr in legal_white_pawn_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 0:
                        if board[omit][1] == 10 and not doublecheck:
                            for sqr in legal_white_knight_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 1:
                        if board[omit][1] == 11 and not doublecheck:
                            for sqr in legal_white_bishop_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 2:
                        if board[omit][1] == 12 and not doublecheck:
                            for sqr in legal_white_rook_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 3:
                        if board[omit][1] == 13 and not doublecheck:
                            for sqr in legal_white_queen_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 4:
                        if board[omit][1] == 14:
                            for sqr in legal_white_king_moves(omit, attacked):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                        q_s_c, k_s_c = can_castle()
                        if board[omit][1] == 14 and turn_to_move == "w" and q_s_c:
                            window.blit(sqr_highlight0, get_square_coord(0))
                            window.blit(sqr_highlight1, get_square_coord(0))
                            window.blit(sqr_highlight0, get_square_coord(2))
                            window.blit(sqr_highlight1, get_square_coord(2))
                        if board[omit][1] == 14 and turn_to_move == "w" and k_s_c:
                            window.blit(sqr_highlight0, get_square_coord(6))
                            window.blit(sqr_highlight1, get_square_coord(6))
                            window.blit(sqr_highlight0, get_square_coord(7))
                            window.blit(sqr_highlight1, get_square_coord(7))
            if turn_to_move == "b":
                if attacked[black_king_pos] == 1:
                    check = True
                    pins, check_resolve = pin_n_check_resolves(True)
                if attacked[black_king_pos] > 1:
                    doublecheck = True

                for piece in range(6):
                    if piece == 5:
                        if board[omit][1] == 17 and not doublecheck:
                            for sqr in legal_black_pawn_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 0:
                        if board[omit][1] == 18 and not doublecheck:
                            for sqr in legal_black_knight_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 1:
                        if board[omit][1] == 19 and not doublecheck:
                            for sqr in legal_black_bishop_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 2:
                        if board[omit][1] == 20 and not doublecheck:
                            for sqr in legal_black_rook_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 3:
                        if board[omit][1] == 21 and not doublecheck:
                            for sqr in legal_black_queen_moves(omit, check, pins, check_resolve):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                    if piece == 4:
                        if board[omit][1] == 22:
                            for sqr in legal_black_king_moves(omit, attacked):
                                window.blit(sqr_highlight0, get_square_coord(sqr))
                                window.blit(sqr_highlight1, get_square_coord(sqr))
                        q_s_c, k_s_c = can_castle()
                        if board[omit][1] == 22 and turn_to_move == "b" and q_s_c:
                            window.blit(sqr_highlight0, get_square_coord(58))
                            window.blit(sqr_highlight1, get_square_coord(58))
                            window.blit(sqr_highlight0, get_square_coord(56))
                            window.blit(sqr_highlight1, get_square_coord(56))
                        if board[omit][1] == 22 and turn_to_move == "b" and k_s_c:
                            window.blit(sqr_highlight0, get_square_coord(62))
                            window.blit(sqr_highlight1, get_square_coord(62))
                            window.blit(sqr_highlight0, get_square_coord(63))
                            window.blit(sqr_highlight1, get_square_coord(63))
    if not picked:
        omit_square = DEFAULT_int
    for sqr in board:
        if sqr[0] != omit_square:
            draw_piece(sqr[1], sqr[0])
        if sqr[0] == 63 and picked and omit != DEFAULT_int:
            draw_piece(board[omit][1], DEFAULT_int, specific=True, coord=mouse_pos)
    # Draw list of possible promotions if there is a pawn to promote ---------------------
    if pawn_to_promote():
        for sqr in range(64):
            if sqr in range(56, 64):
                if board[sqr][1] == 9:
                    sqr_file, sqr_rank = get_file_n_rank(sqr)
                    window.blit(choose_piece_img, get_square_coord(sqr))
                    draw_piece(13, get_square_index(file=sqr_file, rank=sqr_rank))
                    draw_piece(12, get_square_index(file=sqr_file, rank=sqr_rank - 1))
                    draw_piece(11, get_square_index(file=sqr_file, rank=sqr_rank - 2))
                    draw_piece(10, get_square_index(file=sqr_file, rank=sqr_rank - 3))
            if sqr in range(0, 8):
                if board[sqr][1] == 17:
                    sqr_file, sqr_rank = get_file_n_rank(sqr)
                    window.blit(choose_piece_img, get_square_coord(sqr + 24))
                    draw_piece(21, get_square_index(file=sqr_file, rank=sqr_rank))
                    draw_piece(20, get_square_index(file=sqr_file, rank=sqr_rank + 1))
                    draw_piece(19, get_square_index(file=sqr_file, rank=sqr_rank + 2))
                    draw_piece(18, get_square_index(file=sqr_file, rank=sqr_rank + 3))


def keep_mouse_boundary():
    global mouse_pos
    global mouse_clicked_on
    global mouse_unclicked_on
    mouse_pos = pygame.mouse.get_pos()

    if mouse_pos[0] < b_pos_x:
        mouse_pos = (b_pos_x, mouse_pos[1])
    if mouse_pos[0] > b_pos_x + board_size - 1:
        mouse_pos = (b_pos_x + board_size - 1, mouse_pos[1])
    if mouse_pos[1] < b_pos_y:
        mouse_pos = (mouse_pos[0], b_pos_y)
    if mouse_pos[1] > b_pos_y + board_size - 1:
        mouse_pos = (mouse_pos[0], b_pos_y + board_size - 1)
    # -------------------------------------------
    if mouse_clicked_on != DEFAULT_tup:
        if mouse_clicked_on[0] < b_pos_x:
            mouse_clicked_on = DEFAULT_tup
        if mouse_clicked_on[0] > b_pos_x + board_size - 1:
            mouse_clicked_on = DEFAULT_tup
        if mouse_clicked_on[1] < b_pos_y:
            mouse_clicked_on = DEFAULT_tup
        if mouse_clicked_on[1] > b_pos_y + board_size - 1:
            mouse_clicked_on = DEFAULT_tup
    # --------------------------------------------
    if mouse_unclicked_on != DEFAULT_tup:
        if mouse_unclicked_on[0] < b_pos_x:
            mouse_unclicked_on = DEFAULT_tup
        if mouse_unclicked_on[0] > b_pos_x + board_size - 1:
            mouse_unclicked_on = DEFAULT_tup
        if mouse_unclicked_on[1] < b_pos_y:
            mouse_unclicked_on = DEFAULT_tup
        if mouse_unclicked_on[1] > b_pos_y + board_size - 1:
            mouse_unclicked_on = DEFAULT_tup


def update_king_position():
    global white_king_pos
    global black_king_pos
    for sqr in board:
        if sqr[1] == 14:
            white_king_pos = sqr[0]
        if sqr[1] == 22:
            black_king_pos = sqr[0]


def attacked_squares():
    global board
    attacked = [0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0]

    if turn_to_move == "w":
        # Removing the king from the board temporarily to avoid attack detection errors
        board[white_king_pos][1] = 0
        # ----------------------------------------
        for pawns in black_occupancy[0]:
            for move in black_pawn_moves[pawns][0]:
                attacked[move] += 1
            for move in black_pawn_moves[pawns][2]:
                attacked[move] += 1
        # ----------------------------------------
        for knights in black_occupancy[1]:
            for move in knight_moves[knights]:
                attacked[move] += 1
        # ----------------------------------------
        for bishops in black_occupancy[2]:
            for move in bishop_moves[bishops][0]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in bishop_moves[bishops][1]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in bishop_moves[bishops][2]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in bishop_moves[bishops][3]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
        # ----------------------------------------
        for rooks in black_occupancy[3]:
            for move in rook_moves[rooks][0]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in rook_moves[rooks][1]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in rook_moves[rooks][2]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in rook_moves[rooks][3]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
        # ----------------------------------------
        for queens in black_occupancy[4]:
            for move in queen_moves[queens][0]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][1]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][2]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][3]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][4]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][5]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][6]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][7]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
        # ----------------------------------------
        for kings in black_occupancy[5]:
            for move in king_moves[kings]:
                attacked[move] += 1
        # Adding the relevant king back to the board
        board[white_king_pos][1] = 14
    else:
        # Removing the king from the board temporarily to avoid attack detection errors
        board[black_king_pos][1] = 0
        # ----------------------------------------
        for pawns in white_occupancy[0]:
            for move in white_pawn_moves[pawns][0]:
                attacked[move] += 1
            for move in white_pawn_moves[pawns][2]:
                attacked[move] += 1
        # ----------------------------------------
        for knights in white_occupancy[1]:
            for move in knight_moves[knights]:
                attacked[move] += 1
        # ----------------------------------------
        for bishops in white_occupancy[2]:
            for move in bishop_moves[bishops][0]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in bishop_moves[bishops][1]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in bishop_moves[bishops][2]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in bishop_moves[bishops][3]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
        # ----------------------------------------
        for rooks in white_occupancy[3]:
            for move in rook_moves[rooks][0]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in rook_moves[rooks][1]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in rook_moves[rooks][2]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in rook_moves[rooks][3]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
        # ----------------------------------------
        for queens in white_occupancy[4]:
            for move in queen_moves[queens][0]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][1]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][2]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][3]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][4]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][5]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][6]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
            for move in queen_moves[queens][7]:
                attacked[move] += 1
                if board[move][1] != 0:
                    break
        # ----------------------------------------
        for kings in white_occupancy[5]:
            for move in king_moves[kings]:
                attacked[move] += 1
        # Adding the relevant king back to the board
        board[black_king_pos][1] = 22
    return attacked


def pin_n_check_resolves(in_check):
    pins = [[], [], [], [], []]
    check = ""

    # IF WHITE TO MOVE
    if turn_to_move == "w":
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[white_king_pos][0]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] >= 17:
                        if board[square][1] == 20 or board[square][1] == 21:
                            check = ("0" * (white_king_pos + 1)) + ("1" * (square - white_king_pos)) + (
                                    "0" * (63 - square))
                        break
                    else:
                        potential_pin = square
                else:
                    if 20 <= board[square][1] <= 21:
                        resolves = ("0" * (white_king_pos + 1)) + ("1" * (square - white_king_pos)) + (
                                "0" * (63 - square))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[white_king_pos][2]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] >= 17:
                        if board[square][1] == 20 or board[square][1] == 21:
                            check = ("0" * (white_king_pos + 1)) + ("00000001" * ((square - white_king_pos) // 8)) + (
                                    "0" * (63 - square))
                        break
                    else:
                        potential_pin = square
                else:
                    if 20 <= board[square][1] <= 21:
                        resolves = ("0" * (white_king_pos + 1)) + ("00000001" * ((square - white_king_pos) // 8)) + (
                                "0" * (63 - square))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[white_king_pos][4]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] >= 17:
                        if board[square][1] == 20 or board[square][1] == 21:
                            check = ("0" * square) + ("1" * (white_king_pos - square)) + ("0" * (64 - white_king_pos))
                        break
                    else:
                        potential_pin = square
                else:
                    if 20 <= board[square][1] <= 21:
                        resolves = ("0" * square) + ("1" * (white_king_pos - square)) + ("0" * (64 - white_king_pos))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[white_king_pos][6]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] >= 17:
                        if board[square][1] == 20 or board[square][1] == 21:
                            check = ("0" * square) + ("10000000" * ((white_king_pos - square) // 8)) + (
                                    "0" * (64 - white_king_pos))
                        break
                    else:
                        potential_pin = square
                else:
                    if 20 <= board[square][1] <= 21:
                        resolves = ("0" * square) + ("10000000" * ((white_king_pos - square) // 8)) + (
                                "0" * (64 - white_king_pos))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[white_king_pos][1]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] >= 17:
                        if board[square][1] == 19 or board[square][1] == 21:
                            check = ("0" * (white_king_pos + 1)) + ("000000001" * ((square - white_king_pos) // 9)) + (
                                    "0" * (63 - square))
                        break
                    else:
                        potential_pin = square
                else:
                    if board[square][1] == 19 or board[square][1] == 21:
                        resolves = ("0" * (white_king_pos + 1)) + ("000000001" * ((square - white_king_pos) // 9)) + (
                                "0" * (63 - square))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[white_king_pos][3]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] >= 17:
                        if board[square][1] == 19 or board[square][1] == 21:
                            check = ("0" * (white_king_pos + 1)) + ("0000001" * ((square - white_king_pos) // 7)) + (
                                    "0" * (63 - square))
                        break
                    else:
                        potential_pin = square
                else:
                    if board[square][1] == 19 or board[square][1] == 21:
                        resolves = ("0" * (white_king_pos + 1)) + ("0000001" * ((square - white_king_pos) // 7)) + (
                                "0" * (63 - square))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[white_king_pos][5]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] >= 17:
                        if board[square][1] == 19 or board[square][1] == 21:
                            check = ("0" * square) + ("100000000" * ((white_king_pos - square) // 9)) + (
                                    "0" * (64 - white_king_pos))
                        break
                    else:
                        potential_pin = square
                else:
                    if board[square][1] == 19 or board[square][1] == 21:
                        resolves = ("0" * square) + ("100000000" * ((white_king_pos - square) // 9)) + (
                                "0" * (64 - white_king_pos))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[white_king_pos][7]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] >= 17:
                        if board[square][1] == 19 or board[square][1] == 21:
                            check = ("0" * square) + ("1000000" * ((white_king_pos - square) // 7)) + (
                                    "0" * (64 - white_king_pos))
                        break
                    else:
                        potential_pin = square
                else:
                    if board[square][1] == 19 or board[square][1] == 21:
                        resolves = ("0" * square) + ("1000000" * ((white_king_pos - square) // 7)) + (
                                "0" * (64 - white_king_pos))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # If in check, check as well if knight or pawn is giving the check
        if in_check and check == "":
            for square in knight_moves[white_king_pos]:
                if board[square][1] == 18:
                    check = ("0" * square) + "1" + ("0" * (63 - square))
                    break
            for square in white_pawn_moves[white_king_pos][0]:
                if board[square][1] == 17:
                    check = ("0" * square) + "1" + ("0" * (63 - square))
            for square in white_pawn_moves[white_king_pos][2]:
                if board[square][1] == 17:
                    check = ("0" * square) + "1" + ("0" * (63 - square))

    # IF BLACK TO MOVE -----------
    else:
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[black_king_pos][0]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] <= 14:
                        if board[square][1] == 12 or board[square][1] == 13:
                            check = ("0" * (black_king_pos + 1)) + ("1" * (square - black_king_pos)) + (
                                    "0" * (63 - square))
                        break
                    else:
                        potential_pin = square
                else:
                    if 12 <= board[square][1] <= 13:
                        resolves = ("0" * (black_king_pos + 1)) + ("1" * (square - black_king_pos)) + (
                                "0" * (63 - square))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[black_king_pos][2]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] <= 14:
                        if board[square][1] == 12 or board[square][1] == 13:
                            check = ("0" * (black_king_pos + 1)) + ("00000001" * ((square - black_king_pos) // 8)) + (
                                    "0" * (63 - square))
                        break
                    else:
                        potential_pin = square
                else:
                    if 12 <= board[square][1] <= 13:
                        resolves = ("0" * (black_king_pos + 1)) + ("00000001" * ((square - black_king_pos) // 8)) + (
                                "0" * (63 - square))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[black_king_pos][4]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] <= 14:
                        if board[square][1] == 12 or board[square][1] == 13:
                            check = ("0" * square) + ("1" * (black_king_pos - square)) + ("0" * (64 - black_king_pos))
                        break
                    else:
                        potential_pin = square
                else:
                    if 12 <= board[square][1] <= 13:
                        resolves = ("0" * square) + ("1" * (black_king_pos - square)) + ("0" * (64 - black_king_pos))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[black_king_pos][6]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] <= 14:
                        if board[square][1] == 12 or board[square][1] == 13:
                            check = ("0" * square) + ("10000000" * ((black_king_pos - square) // 8)) + (
                                    "0" * (64 - black_king_pos))
                        break
                    else:
                        potential_pin = square
                else:
                    if 12 <= board[square][1] <= 13:
                        resolves = ("0" * square) + ("10000000" * ((black_king_pos - square) // 8)) + (
                                "0" * (64 - black_king_pos))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[black_king_pos][1]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] <= 14:
                        if board[square][1] == 11 or board[square][1] == 13:
                            check = ("0" * (black_king_pos + 1)) + ("000000001" * ((square - black_king_pos) // 9)) + (
                                    "0" * (63 - square))
                        break
                    else:
                        potential_pin = square
                else:
                    if board[square][1] == 11 or board[square][1] == 13:
                        resolves = ("0" * (black_king_pos + 1)) + ("000000001" * ((square - black_king_pos) // 9)) + (
                                "0" * (63 - square))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[black_king_pos][3]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] <= 14:
                        if board[square][1] == 11 or board[square][1] == 13:
                            check = ("0" * (black_king_pos + 1)) + ("0000001" * ((square - black_king_pos) // 7)) + (
                                    "0" * (63 - square))
                        break
                    else:
                        potential_pin = square
                else:
                    if board[square][1] == 11 or board[square][1] == 13:
                        resolves = ("0" * (black_king_pos + 1)) + ("0000001" * ((square - black_king_pos) // 7)) + (
                                "0" * (63 - square))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[black_king_pos][5]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] <= 14:
                        if board[square][1] == 11 or board[square][1] == 13:
                            check = ("0" * square) + ("100000000" * ((black_king_pos - square) // 9)) + (
                                    "0" * (64 - black_king_pos))
                        break
                    else:
                        potential_pin = square
                else:
                    if board[square][1] == 11 or board[square][1] == 13:
                        resolves = ("0" * square) + ("100000000" * ((black_king_pos - square) // 9)) + (
                                "0" * (64 - black_king_pos))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # -------------------------------------------------------------------------------------------------------------
        potential_pin = DEFAULT_int
        for square in queen_moves[black_king_pos][7]:
            if board[square][1] != 0:
                if potential_pin == DEFAULT_int:
                    if board[square][1] <= 14:
                        if board[square][1] == 11 or board[square][1] == 13:
                            check = ("0" * square) + ("1000000" * ((black_king_pos - square) // 7)) + (
                                    "0" * (64 - black_king_pos))
                        break
                    else:
                        potential_pin = square
                else:
                    if board[square][1] == 11 or board[square][1] == 13:
                        resolves = ("0" * square) + ("1000000" * ((black_king_pos - square) // 7)) + (
                                "0" * (64 - black_king_pos))
                        pinned_piece = board[potential_pin][1]
                        pins[segment_map[pinned_piece]].append(resolves)
                    else:
                        break
        # If in check, check as well if knight or pawn is giving the check
        if in_check and check == "":
            for square in knight_moves[black_king_pos]:
                if board[square][1] == 10:
                    check = ("0" * square) + "1" + ("0" * (63 - square))
                    break
            for square in black_pawn_moves[black_king_pos][0]:
                if board[square][1] == 9:
                    check = ("0" * square) + "1" + ("0" * (63 - square))
            for square in black_pawn_moves[black_king_pos][2]:
                if board[square][1] == 9:
                    check = ("0" * square) + "1" + ("0" * (63 - square))

    if in_check:
        return pins, check
    else:
        return pins


# For legal moves ------------------------------------------------------------------------------------------------------
def legal_white_pawn_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    global board
    leg = []
    pinned = False
    for move in white_pawn_moves[square][0]:
        if board[move][1] > 16 or move == en_passant_target:
            leg.append(move)
    for move in white_pawn_moves[square][1]:
        if board[move][1] != 0:
            break
        else:
            leg.append(move)
    for move in white_pawn_moves[square][2]:
        if board[move][1] > 16 or move == en_passant_target:
            leg.append(move)
    for bit_board in pin_list[0]:
        if bit_board[square] == "1":
            pinned = True
            hold = []
            for move in leg:
                if bit_board[move] == "1":
                    hold.append(move)
            leg = hold
    # EN PASSANT DISCOVERED CHECK ON SELF FIX
    if 31 < white_king_pos < 40:
        if 39 < en_passant_target < 48:
            for move in white_pawn_moves[square][0]:
                if move == en_passant_target:
                    board[square][1], board[move][1], board[move - 8][1] = 0, 9, 0
                    for right_dir in rook_moves[white_king_pos][0]:
                        if board[right_dir][1] != 0:
                            if board[right_dir][1] == 20 or board[right_dir][1] == 21:
                                leg.remove(move)
                            break
                    for left_dir in rook_moves[white_king_pos][2]:
                        if board[left_dir][1] != 0:
                            if board[left_dir][1] == 20 or board[left_dir][1] == 21:
                                leg.remove(move)
                            break
                    board[square][1], board[move][1], board[move - 8][1] = 9, 0, 17
    if in_check:
        if pinned:
            leg = []
        else:
            hold = []
            for move in leg:
                if check_list[move] == "1":
                    hold.append(move)
            leg = hold
            # if a pawn causing a check can be captured en passant
            if en_passant_target != DEFAULT_int:
                for sqr in white_pawn_moves[white_king_pos][0]:
                    if board[sqr][1] == 17 and en_passant_target == (sqr + 8):
                        leg.append(en_passant_target)
                for sqr in white_pawn_moves[white_king_pos][2]:
                    if board[sqr][1] == 17 and en_passant_target == (sqr + 8):
                        leg.append(en_passant_target)
    return leg


def legal_white_knight_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    if not in_check:
        for move in knight_moves[square]:
            if 0 < board[move][1] <= 14:
                continue
            else:
                leg.append(move)
        for bit_board in pin_list[1]:
            if bit_board[square] == "1":
                leg = []
                break
    else:
        pinned = False
        for bit_board in pin_list[1]:
            if bit_board[square] == "1":
                pinned, leg = True, []
                break
        if not pinned:
            for move in knight_moves[square]:
                if check_list[move] == "1":
                    leg.append(move)
    return leg


def legal_white_bishop_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    if not in_check:
        for direction in bishop_moves[square]:
            for move in direction:
                leg.append(move)
                if board[move][1] != 0:
                    if board[move][1] <= 14:
                        leg.remove(move)
                    break
        for bit_board in pin_list[2]:
            if bit_board[square] == "1":
                hold = []
                for move in leg:
                    if bit_board[move] == "1":
                        hold.append(move)
                leg = hold
    else:
        pinned = False
        for bit_board in pin_list[2]:
            if bit_board[square] == "1":
                pinned, leg = True, []
                break
        if not pinned:
            for direction in bishop_moves[square]:
                for move in direction:
                    if check_list[move] == "1":
                        leg.append(move)
                    if board[move][1] != 0:
                        break
    return leg


def legal_white_rook_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    if not in_check:
        for direction in rook_moves[square]:
            for move in direction:
                leg.append(move)
                if board[move][1] != 0:
                    if board[move][1] <= 14:
                        leg.remove(move)
                    break
        for bit_board in pin_list[3]:
            if bit_board[square] == "1":
                hold = []
                for move in leg:
                    if bit_board[move] == "1":
                        hold.append(move)
                leg = hold
    else:
        pinned = False
        for bit_board in pin_list[3]:
            if bit_board[square] == "1":
                pinned, leg = True, []
                break
        if not pinned:
            for direction in rook_moves[square]:
                for move in direction:
                    if check_list[move] == "1":
                        leg.append(move)
                    if board[move][1] != 0:
                        break
    return leg


def legal_white_queen_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    if not in_check:
        for direction in queen_moves[square]:
            for move in direction:
                leg.append(move)
                if board[move][1] != 0:
                    if board[move][1] <= 14:
                        leg.remove(move)
                    break
        for bit_board in pin_list[4]:
            if bit_board[square] == "1":
                hold = []
                for move in leg:
                    if bit_board[move] == "1":
                        hold.append(move)
                leg = hold
    else:
        pinned = False
        for bit_board in pin_list[4]:
            if bit_board[square] == "1":
                pinned, leg = True, []
                break
        if not pinned:
            for direction in queen_moves[square]:
                for move in direction:
                    if check_list[move] == "1":
                        leg.append(move)
                    if board[move][1] != 0:
                        break
    return leg


def legal_white_king_moves(square, enemy_targets):
    leg = []
    for move in king_moves[square]:
        if 14 > board[move][1] > 0:
            continue
        else:
            if enemy_targets[move] == 0:
                leg.append(move)
    return leg


# ----------------------------------------------------------------------------------------------------------------------
def legal_black_pawn_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    pinned = False
    for move in black_pawn_moves[square][0]:
        if (8 < board[move][1] < 15) or move == en_passant_target:
            leg.append(move)
    for move in black_pawn_moves[square][1]:
        if board[move][1] != 0:
            break
        else:
            leg.append(move)
    for move in black_pawn_moves[square][2]:
        if (8 < board[move][1] < 15) or move == en_passant_target:
            leg.append(move)
    for bit_board in pin_list[0]:
        if bit_board[square] == "1":
            pinned = True
            hold = []
            for move in leg:
                if bit_board[move] == "1":
                    hold.append(move)
            leg = hold
    # EN PASSANT DISCOVERED CHECK ON SELF FIX
    if 23 < black_king_pos < 32:
        if 15 < en_passant_target < 24:
            for move in black_pawn_moves[square][0]:
                if move == en_passant_target:
                    board[square][1], board[move][1], board[move + 8][1] = 0, 17, 0
                    for left_dir in rook_moves[black_king_pos][2]:
                        if board[left_dir][1] != 0:
                            if board[left_dir][1] == 12 or board[left_dir][1] == 13:
                                leg.remove(move)
                            break
                    for right_dir in rook_moves[white_king_pos][0]:
                        if board[right_dir][1] != 0:
                            if board[right_dir][1] == 12 or board[right_dir][1] == 13:
                                leg.remove(move)
                            break
                    board[square][1], board[move][1], board[move + 8][1] = 17, 0, 9
    if in_check:
        if pinned:
            leg = []
        else:
            hold = []
            for move in leg:
                if check_list[move] == "1" or move == en_passant_target:
                    hold.append(move)
            leg = hold
            # if a pawn causing a check can be captured en passant
            if en_passant_target != DEFAULT_int:
                for sqr in black_pawn_moves[black_king_pos][0]:
                    if board[sqr][1] == 9 and en_passant_target == (sqr - 8):
                        leg.append(en_passant_target)
                for sqr in black_pawn_moves[black_king_pos][2]:
                    if board[sqr][1] == 9 and en_passant_target == (sqr - 8):
                        leg.append(en_passant_target)
    return leg


def legal_black_knight_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    if not in_check:
        for move in knight_moves[square]:
            if board[move][1] > 16:
                continue
            else:
                leg.append(move)
        for bit_board in pin_list[1]:
            if bit_board[square] == "1":
                leg = []
                break
    else:
        pinned = False
        for bit_board in pin_list[1]:
            if bit_board[square] == "1":
                pinned, leg = True, []
                break
        if not pinned:
            for move in knight_moves[square]:
                if check_list[move] == "1":
                    leg.append(move)
    return leg


def legal_black_bishop_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    if not in_check:
        for direction in bishop_moves[square]:
            for move in direction:
                leg.append(move)
                if board[move][1] != 0:
                    if board[move][1] > 16:
                        leg.remove(move)
                    break
        for bit_board in pin_list[2]:
            if bit_board[square] == "1":
                hold = []
                for move in leg:
                    if bit_board[move] == "1":
                        hold.append(move)
                leg = hold
    else:
        pinned = False
        for bit_board in pin_list[2]:
            if bit_board[square] == "1":
                pinned, leg = True, []
                break
        if not pinned:
            for direction in bishop_moves[square]:
                for move in direction:
                    if check_list[move] == "1":
                        leg.append(move)
                    if board[move][1] != 0:
                        break
    return leg


def legal_black_rook_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    if not in_check:
        for direction in rook_moves[square]:
            for move in direction:
                leg.append(move)
                if board[move][1] != 0:
                    if board[move][1] > 16:
                        leg.remove(move)
                    break
        for bit_board in pin_list[3]:
            if bit_board[square] == "1":
                hold = []
                for move in leg:
                    if bit_board[move] == "1":
                        hold.append(move)
                leg = hold
    else:
        pinned = False
        for bit_board in pin_list[3]:
            if bit_board[square] == "1":
                pinned, leg = True, []
                break
        if not pinned:
            for direction in rook_moves[square]:
                for move in direction:
                    if check_list[move] == "1":
                        leg.append(move)
                    if board[move][1] != 0:
                        break
    return leg


def legal_black_queen_moves(square, in_check, pin_list, check_list=DEFAULT_tup):
    leg = []
    if not in_check:
        for direction in queen_moves[square]:
            for move in direction:
                leg.append(move)
                if board[move][1] != 0:
                    if board[move][1] > 16:
                        leg.remove(move)
                    break
        for bit_board in pin_list[4]:
            if bit_board[square] == "1":
                hold = []
                for move in leg:
                    if bit_board[move] == "1":
                        hold.append(move)
                leg = hold
    else:
        pinned = False
        for bit_board in pin_list[4]:
            if bit_board[square] == "1":
                pinned, leg = True, []
                break
        if not pinned:
            for direction in queen_moves[square]:
                for move in direction:
                    if check_list[move] == "1":
                        leg.append(move)
                    if board[move][1] != 0:
                        break
    return leg


def legal_black_king_moves(square, enemy_targets):
    leg = []
    for move in king_moves[square]:
        if board[move][1] > 16:
            continue
        else:
            if enemy_targets[move] == 0:
                leg.append(move)
    return leg


# ----------------------------------------------------------------------------------------------------------------------


def pawn_to_promote():
    global turn_to_move
    for sqr in range(64):
        if (sqr in range(0, 8)) or (sqr in range(56, 64)):
            if board[sqr][1] == 9:
                return True
            if board[sqr][1] == 17:
                return True
    return False


def promote_pawn(m_click_down, m_unclicked):
    global board
    for sqr in range(64):
        if (0 <= sqr <= 7) or (56 <= sqr <= 63):
            if m_click_down == m_unclicked:
                if board[sqr][1] == 9:
                    promotion_square_file, promotion_square_rank = get_file_n_rank(sqr)
                    choose_piece_file, choose_piece_rank = get_file_n_rank(get_square_index(m_unclicked))
                    if choose_piece_file == promotion_square_file:
                        if choose_piece_rank == promotion_square_rank:
                            board[sqr][1] = 13
                        if choose_piece_rank == promotion_square_rank - 1:
                            board[sqr][1] = 12
                        if choose_piece_rank == promotion_square_rank - 2:
                            board[sqr][1] = 11
                        if choose_piece_rank == promotion_square_rank - 3:
                            board[sqr][1] = 10
                if board[sqr][1] == 17:
                    promotion_square_file, promotion_square_rank = get_file_n_rank(sqr)
                    choose_piece_file, choose_piece_rank = get_file_n_rank(get_square_index(m_unclicked))
                    if choose_piece_file == promotion_square_file:
                        if choose_piece_rank == promotion_square_rank:
                            board[sqr][1] = 21
                        if choose_piece_rank == promotion_square_rank + 1:
                            board[sqr][1] = 20
                        if choose_piece_rank == promotion_square_rank + 2:
                            board[sqr][1] = 19
                        if choose_piece_rank == promotion_square_rank + 3:
                            board[sqr][1] = 18


def update_castle_rights():
    global castle_conditions
    if board[4][1] != 14:
        castle_conditions["w_k_moved"] = True
    if board[0][1] != 12:
        castle_conditions["w_q_r_moved"] = True
    if board[7][1] != 12:
        castle_conditions["w_k_r_moved"] = True
    if board[60][1] != 22:
        castle_conditions["b_k_moved"] = True
    if board[56][1] != 20:
        castle_conditions["b_q_r_moved"] = True
    if board[63][1] != 20:
        castle_conditions["b_k_r_moved"] = True


def can_castle():
    queen_side, king_side = False, False
    w_q_side, w_k_side = [1, 2, 3], [5, 6]
    b_q_side, b_k_side = [57, 58, 59], [61, 62]
    attacked, check, double = attacked_squares(), False, False

    if turn_to_move == "w":
        if attacked[white_king_pos] != 0:
            if attacked[white_king_pos] == 1:
                check = True
            else:
                double = True

        if not castle_conditions["w_k_moved"]:
            if not check and not double:
                if not castle_conditions["w_q_r_moved"]:
                    temp_hold = True
                    for sqr in w_q_side:
                        if board[sqr][1] != 0 or attacked[sqr] != 0:
                            temp_hold = False
                    queen_side = temp_hold
                if not castle_conditions["w_k_r_moved"]:
                    temp_hold = True
                    for sqr in w_k_side:
                        if board[sqr][1] != 0 or attacked[sqr] != 0:
                            temp_hold = False
                    king_side = temp_hold
    else:
        if attacked[black_king_pos] != 0:
            if attacked[black_king_pos] == 1:
                check = True
            else:
                double = True
        if not castle_conditions["b_k_moved"]:
            if not check and not double:
                if not castle_conditions["b_q_r_moved"]:
                    temp_hold = True
                    for sqr in b_q_side:
                        if board[sqr][1] != 0 or attacked[sqr] != 0:
                            temp_hold = False
                    queen_side = temp_hold
                if not castle_conditions["b_k_r_moved"]:
                    temp_hold = True
                    for sqr in b_k_side:
                        if board[sqr][1] != 0 or attacked[sqr] != 0:
                            temp_hold = False
                    king_side = temp_hold
    return queen_side, king_side


def castle_king(side):
    global board
    if turn_to_move == "w":
        if side == "king side":
            board[6][1] = 14
            board[5][1] = 12
            board[4][1] = 0
            board[7][1] = 0
        if side == "queen side":
            board[2][1] = 14
            board[3][1] = 12
            board[4][1] = 0
            board[0][1] = 0
    if turn_to_move == "b":
        if side == "king side":
            board[62][1] = 22
            board[61][1] = 20
            board[60][1] = 0
            board[63][1] = 0
        if side == "queen side":
            board[58][1] = 22
            board[59][1] = 20
            board[60][1] = 0
            board[56][1] = 0


# Switching Player turn
def switch_turn():
    global turn_to_move
    if turn_to_move == "w":
        turn_to_move = "b"
    else:
        turn_to_move = "w"


def set_en_passant(from_sqr, to_sqr):
    global en_passant_target
    if from_sqr < 16:
        en_passant_target = to_sqr - 8
    else:
        en_passant_target = to_sqr + 8


# When using saved mouse positions as input make sure to reset them after the piece is moved
def move_piece():
    # Do not move anything if there is a pawn on the back ranks
    if not pawn_to_promote():
        global board
        global en_passant_target
        from_index = get_square_index(mouse_clicked_on)
        to_index = get_square_index(mouse_unclicked_on)
        piece = board[from_index][1]
        attacked = attacked_squares()
        check, doublecheck = False, False
        pins = pin_n_check_resolves(False)
        moved = False
        double_pawn_push = False
        check_resolve = ""
        queen_side, king_side = can_castle()

        # -----------------------------------------------------------------------------------

        if turn_to_move == "w":
            if attacked[white_king_pos] == 1:
                check = True
                pins, check_resolve = pin_n_check_resolves(True)
            if attacked[white_king_pos] > 1:
                doublecheck = True

            if board[from_index][1] != 0:
                if piece == 9 and not doublecheck:
                    if to_index in legal_white_pawn_moves(from_index, check, pins, check_resolve):
                        if abs(from_index - to_index) == 16:
                            double_pawn_push = True
                        if to_index == en_passant_target:
                            board[to_index - 8][1] = 0
                        board[from_index][1] = 0
                        board[to_index][1] = 9
                        moved = True
                        switch_turn()
                if piece == 10 and not doublecheck:
                    if to_index in legal_white_knight_moves(from_index, check, pins, check_resolve):
                        board[from_index][1] = 0
                        board[to_index][1] = 10
                        moved = True
                        switch_turn()
                if piece == 11 and not doublecheck:
                    if to_index in legal_white_bishop_moves(from_index, check, pins, check_resolve):
                        board[from_index][1] = 0
                        board[to_index][1] = 11
                        moved = True
                        switch_turn()
                if piece == 12 and not doublecheck:
                    if to_index in legal_white_rook_moves(from_index, check, pins, check_resolve):
                        board[from_index][1] = 0
                        board[to_index][1] = 12
                        moved = True
                        switch_turn()
                if piece == 13 and not doublecheck:
                    if to_index in legal_white_queen_moves(from_index, check, pins, check_resolve):
                        board[from_index][1] = 0
                        board[to_index][1] = 13
                        moved = True
                        switch_turn()
                if piece == 14:
                    if to_index in legal_white_king_moves(from_index, attacked):
                        board[from_index][1] = 0
                        board[to_index][1] = 14
                        moved = True
                        switch_turn()
                    if (to_index in [6, 7]) and king_side:
                        castle_king("king side")
                        moved = True
                        switch_turn()
                    if (to_index in [0, 2]) and queen_side:
                        castle_king("queen side")
                        moved = True
                        switch_turn()
        # -----------------------------------------------------------------------------------
        else:
            if attacked[black_king_pos] == 1:
                check = True
                pins, check_resolve = pin_n_check_resolves(True)
            if attacked[black_king_pos] > 1:
                doublecheck = True

            if board[from_index][1] != 0:
                if piece == 17 and not doublecheck:
                    if to_index in legal_black_pawn_moves(from_index, check, pins, check_resolve):
                        if abs(from_index - to_index) == 16:
                            double_pawn_push = True
                        if to_index == en_passant_target:
                            board[to_index + 8][1] = 0
                        board[from_index][1] = 0
                        board[to_index][1] = 17
                        moved = True
                        switch_turn()
                if piece == 18 and not doublecheck:
                    if to_index in legal_black_knight_moves(from_index, check, pins, check_resolve):
                        board[from_index][1] = 0
                        board[to_index][1] = 18
                        moved = True
                        switch_turn()
                if piece == 19 and not doublecheck:
                    if to_index in legal_black_bishop_moves(from_index, check, pins, check_resolve):
                        board[from_index][1] = 0
                        board[to_index][1] = 19
                        moved = True
                        switch_turn()
                if piece == 20 and not doublecheck:
                    if to_index in legal_black_rook_moves(from_index, check, pins, check_resolve):
                        board[from_index][1] = 0
                        board[to_index][1] = 20
                        moved = True
                        switch_turn()
                if piece == 21 and not doublecheck:
                    if to_index in legal_black_queen_moves(from_index, check, pins, check_resolve):
                        board[from_index][1] = 0
                        board[to_index][1] = 21
                        moved = True
                        switch_turn()
                if piece == 22:
                    if to_index in legal_black_king_moves(from_index, attacked):
                        board[from_index][1] = 0
                        board[to_index][1] = 22
                        moved = True
                        switch_turn()
                    if (to_index in [62, 63]) and king_side:
                        castle_king("king side")
                        moved = True
                        switch_turn()
                    if (to_index in [56, 58]) and queen_side:
                        castle_king("queen side")
                        moved = True
                        switch_turn()
        if moved:
            if double_pawn_push:
                pass
            else:
                en_passant_target = DEFAULT_int


# AI stuff begins ------------------------------------------------------------------------------------------------------
def evaluation():
    white_material = 0
    white_material += len(white_occupancy[0])
    white_material += len(white_occupancy[1]) * 3
    white_material += len(white_occupancy[2]) * 3
    white_material += len(white_occupancy[3]) * 5
    white_material += len(white_occupancy[4]) * 9
    black_material = 0
    black_material += len(black_occupancy[0])
    black_material += len(black_occupancy[1]) * 3
    black_material += len(black_occupancy[2]) * 3
    black_material += len(black_occupancy[3]) * 5
    black_material += len(black_occupancy[4]) * 9
    return white_material - black_material


def search(depth):
    if depth == 0:
        return evaluation()
    global turn_to_move, board, white_occupancy, black_occupancy, white_king_pos, black_king_pos, en_passant_target
    attacked = attacked_squares()
    best_move = ""
    if turn_to_move == "w":
        best_eval = -1000
        # --------------------------------------------------
        # --------------------------------------------------
        if attacked[white_king_pos] == 1:
            check = True
            pins, check_resolve = pin_n_check_resolves(True)
        else:
            check = False
            pins = pin_n_check_resolves(False)
            check_resolve = ""
        if attacked[white_king_pos] > 1:
            doublecheck = True
        else:
            doublecheck = False
        # --------------------------------------------------
        # --------------------------------------------------
        if not doublecheck:
            previous_occupancy_state = copy.deepcopy(white_occupancy[0])
            for p in previous_occupancy_state:
                if 47 < p < 56:
                    for move in legal_white_pawn_moves(p, check, pins, check_resolve):
                        for promotion in range(10, 14):
                            previously_occupied_by = board[move][1]

                            board[move][1] = promotion
                            board[p][1] = 0
                            white_occupancy[0].remove(p)
                            white_occupancy[segment_map[promotion]].append(move)
                            if previously_occupied_by != 0:
                                black_occupancy[segment_map[previously_occupied_by]].remove(move)
                            turn_to_move = "b"

                            evaluate = search(depth - 1)
                            if evaluate > best_eval:
                                best_move = [p, move, promotion]
                            best_eval = max(evaluate, best_eval)

                            board[move][1] = previously_occupied_by
                            board[p][1] = 9
                            white_occupancy[segment_map[promotion]].remove(move)
                            white_occupancy[0].append(p)
                            if previously_occupied_by != 0:
                                black_occupancy[segment_map[previously_occupied_by]].append(move)
                else:
                    for move in legal_white_pawn_moves(p, check, pins, check_resolve):
                        previously_occupied_by = board[move][1]

                        board[move][1] = 9
                        board[p][1] = 0
                        white_occupancy[0].remove(p)
                        white_occupancy[0].append(move)
                        if previously_occupied_by != 0:
                            black_occupancy[segment_map[previously_occupied_by]].remove(move)
                        turn_to_move = "b"

                        evaluate = search(depth - 1)
                        if evaluate > best_eval:
                            best_move = [p, move]
                        best_eval = max(evaluate, best_eval)

                        board[move][1] = previously_occupied_by
                        board[p][1] = 9
                        white_occupancy[0].remove(move)
                        white_occupancy[0].append(p)
                        if previously_occupied_by != 0:
                            black_occupancy[segment_map[previously_occupied_by]].append(move)
            previous_occupancy_state = copy.deepcopy(white_occupancy[1])
            for n in previous_occupancy_state:
                for move in legal_white_knight_moves(n, check, pins, check_resolve):
                    previously_occupied_by = board[move][1]

                    board[move][1] = 10
                    board[n][1] = 0
                    white_occupancy[1].remove(n)
                    white_occupancy[1].append(move)
                    if previously_occupied_by != 0:
                        black_occupancy[segment_map[previously_occupied_by]].remove(move)
                    turn_to_move = "b"

                    evaluate = search(depth - 1)
                    if evaluate > best_eval:
                        best_move = [n, move]
                    best_eval = max(evaluate, best_eval)

                    board[move][1] = previously_occupied_by
                    board[n][1] = 10
                    white_occupancy[1].remove(move)
                    white_occupancy[1].append(n)
                    if previously_occupied_by != 0:
                        black_occupancy[segment_map[previously_occupied_by]].append(move)
            previous_occupancy_state = copy.deepcopy(white_occupancy[2])
            for b in previous_occupancy_state:
                for move in legal_white_bishop_moves(b, check, pins, check_resolve):
                    previously_occupied_by = board[move][1]

                    board[move][1] = 11
                    board[b][1] = 0
                    white_occupancy[2].remove(b)
                    white_occupancy[2].append(move)
                    if previously_occupied_by != 0:
                        black_occupancy[segment_map[previously_occupied_by]].remove(move)
                    turn_to_move = "b"

                    evaluate = search(depth - 1)
                    if evaluate > best_eval:
                        best_move = [b, move]
                    best_eval = max(evaluate, best_eval)

                    board[move][1] = previously_occupied_by
                    board[b][1] = 11
                    white_occupancy[2].remove(move)
                    white_occupancy[2].append(b)
                    if previously_occupied_by != 0:
                        black_occupancy[segment_map[previously_occupied_by]].append(move)
            previous_occupancy_state = copy.deepcopy(white_occupancy[3])
            for r in previous_occupancy_state:
                for move in legal_white_rook_moves(r, check, pins, check_resolve):
                    previously_occupied_by = board[move][1]

                    board[move][1] = 12
                    board[r][1] = 0
                    white_occupancy[3].remove(r)
                    white_occupancy[3].append(move)
                    if previously_occupied_by != 0:
                        black_occupancy[segment_map[previously_occupied_by]].remove(move)
                    turn_to_move = "b"

                    evaluate = search(depth - 1)
                    if evaluate > best_eval:
                        best_move = [r, move]
                    best_eval = max(evaluate, best_eval)

                    board[move][1] = previously_occupied_by
                    board[r][1] = 12
                    white_occupancy[3].remove(move)
                    white_occupancy[3].append(r)
                    if previously_occupied_by != 0:
                        black_occupancy[segment_map[previously_occupied_by]].append(move)
            previous_occupancy_state = copy.deepcopy(white_occupancy[4])
            for q in previous_occupancy_state:
                for move in legal_white_queen_moves(q, check, pins, check_resolve):
                    previously_occupied_by = board[move][1]

                    board[move][1] = 13
                    board[q][1] = 0
                    white_occupancy[4].remove(q)
                    white_occupancy[4].append(move)
                    if previously_occupied_by != 0:
                        black_occupancy[segment_map[previously_occupied_by]].remove(move)
                    turn_to_move = "b"

                    evaluate = search(depth - 1)
                    if evaluate > best_eval:
                        best_move = [q, move]
                    best_eval = max(evaluate, best_eval)

                    board[move][1] = previously_occupied_by
                    board[q][1] = 13
                    white_occupancy[4].remove(move)
                    white_occupancy[4].append(q)
                    if previously_occupied_by != 0:
                        black_occupancy[segment_map[previously_occupied_by]].append(move)
        for k in white_occupancy[5]:
            for move in legal_white_king_moves(k, attacked):
                previously_occupied_by = board[move][1]

                white_king_pos = move

                board[move][1] = 14
                board[k][1] = 0
                white_occupancy[5] = [move]
                if previously_occupied_by != 0:
                    black_occupancy[segment_map[previously_occupied_by]].remove(move)
                turn_to_move = "b"

                evaluate = search(depth - 1)
                if evaluate > best_eval:
                    best_move = [k, move]
                best_eval = max(evaluate, best_eval)

                white_king_pos = k

                board[move][1] = previously_occupied_by
                board[k][1] = 14
                white_occupancy[5] = [k]
                if previously_occupied_by != 0:
                    black_occupancy[segment_map[previously_occupied_by]].append(move)
    else:
        best_eval = 1000
        # --------------------------------------------------
        # --------------------------------------------------
        if attacked[black_king_pos] == 1:
            check = True
            pins, check_resolve = pin_n_check_resolves(True)
        else:
            check = False
            pins = pin_n_check_resolves(False)
            check_resolve = ""
        if attacked[black_king_pos] > 1:
            doublecheck = True
        else:
            doublecheck = False
        # --------------------------------------------------
        # --------------------------------------------------
        if not doublecheck:
            previous_occupancy_state = copy.deepcopy(black_occupancy[0])
            for p in previous_occupancy_state:
                if 7 < p < 16:
                    for move in legal_black_pawn_moves(p, check, pins, check_resolve):
                        for promotion in range(18, 22):
                            previously_occupied_by = board[move][1]

                            board[move][1] = promotion
                            board[p][1] = 0
                            black_occupancy[0].remove(p)
                            black_occupancy[segment_map[promotion]].append(move)
                            if previously_occupied_by != 0:
                                white_occupancy[segment_map[previously_occupied_by]].remove(move)
                            turn_to_move = "w"

                            evaluate = search(depth - 1)
                            if evaluate < best_eval:
                                best_move = [p, move, promotion]
                            best_eval = min(evaluate, best_eval)

                            board[move][1] = previously_occupied_by
                            board[p][1] = 17
                            black_occupancy[segment_map[promotion]].remove(move)
                            black_occupancy[0].append(p)
                            if previously_occupied_by != 0:
                                white_occupancy[segment_map[previously_occupied_by]].append(move)
                else:
                    for move in legal_black_pawn_moves(p, check, pins, check_resolve):
                        previously_occupied_by = board[move][1]

                        board[move][1] = 17
                        board[p][1] = 0
                        black_occupancy[0].remove(p)
                        black_occupancy[0].append(move)
                        if previously_occupied_by != 0:
                            white_occupancy[segment_map[previously_occupied_by]].remove(move)
                        turn_to_move = "w"

                        evaluate = search(depth - 1)
                        if evaluate < best_eval:
                            best_move = [p, move]
                        best_eval = min(evaluate, best_eval)

                        board[move][1] = previously_occupied_by
                        board[p][1] = 17
                        black_occupancy[0].remove(move)
                        black_occupancy[0].append(p)
                        if previously_occupied_by != 0:
                            white_occupancy[segment_map[previously_occupied_by]].append(move)
            previous_occupancy_state = copy.deepcopy(black_occupancy[1])
            for n in previous_occupancy_state:
                for move in legal_black_knight_moves(n, check, pins, check_resolve):
                    previously_occupied_by = board[move][1]

                    board[move][1] = 18
                    board[n][1] = 0
                    black_occupancy[1].remove(n)
                    black_occupancy[1].append(move)
                    if previously_occupied_by != 0:
                        white_occupancy[segment_map[previously_occupied_by]].remove(move)
                    turn_to_move = "w"

                    evaluate = search(depth - 1)
                    if evaluate < best_eval:
                        best_move = [n, move]
                    best_eval = min(evaluate, best_eval)

                    board[move][1] = previously_occupied_by
                    board[n][1] = 18
                    black_occupancy[1].remove(move)
                    black_occupancy[1].append(n)
                    if previously_occupied_by != 0:
                        white_occupancy[segment_map[previously_occupied_by]].append(move)
            previous_occupancy_state = copy.deepcopy(black_occupancy[2])
            for b in previous_occupancy_state:
                for move in legal_black_bishop_moves(b, check, pins, check_resolve):
                    previously_occupied_by = board[move][1]

                    board[move][1] = 19
                    board[b][1] = 0
                    black_occupancy[2].remove(b)
                    black_occupancy[2].append(move)
                    if previously_occupied_by != 0:
                        white_occupancy[segment_map[previously_occupied_by]].remove(move)
                    turn_to_move = "w"

                    evaluate = search(depth - 1)
                    if evaluate < best_eval:
                        best_move = [b, move]
                    best_eval = min(evaluate, best_eval)

                    board[move][1] = previously_occupied_by
                    board[b][1] = 19
                    black_occupancy[2].remove(move)
                    black_occupancy[2].append(b)
                    if previously_occupied_by != 0:
                        white_occupancy[segment_map[previously_occupied_by]].append(move)
            previous_occupancy_state = copy.deepcopy(black_occupancy[3])
            for r in previous_occupancy_state:
                for move in legal_black_rook_moves(r, check, pins, check_resolve):
                    previously_occupied_by = board[move][1]

                    board[move][1] = 20
                    board[r][1] = 0
                    black_occupancy[3].remove(r)
                    black_occupancy[3].append(move)
                    if previously_occupied_by != 0:
                        white_occupancy[segment_map[previously_occupied_by]].remove(move)
                    turn_to_move = "w"

                    evaluate = search(depth - 1)
                    if evaluate < best_eval:
                        best_move = [r, move]
                    best_eval = min(evaluate, best_eval)

                    board[move][1] = previously_occupied_by
                    board[r][1] = 20
                    black_occupancy[3].remove(move)
                    black_occupancy[3].append(r)
                    if previously_occupied_by != 0:
                        white_occupancy[segment_map[previously_occupied_by]].append(move)
            previous_occupancy_state = copy.deepcopy(black_occupancy[4])
            for q in previous_occupancy_state:
                for move in legal_black_queen_moves(q, check, pins, check_resolve):
                    previously_occupied_by = board[move][1]

                    board[move][1] = 21
                    board[q][1] = 0
                    black_occupancy[4].remove(q)
                    black_occupancy[4].append(move)
                    if previously_occupied_by != 0:
                        white_occupancy[segment_map[previously_occupied_by]].remove(move)
                    turn_to_move = "w"

                    evaluate = search(depth - 1)
                    if evaluate < best_eval:
                        best_move = [q, move]
                    best_eval = min(evaluate, best_eval)

                    board[move][1] = previously_occupied_by
                    board[q][1] = 21
                    black_occupancy[4].remove(move)
                    black_occupancy[4].append(q)
                    if previously_occupied_by != 0:
                        white_occupancy[segment_map[previously_occupied_by]].append(move)
        for k in black_occupancy[5]:
            for move in legal_black_king_moves(k, attacked):
                previously_occupied_by = board[move][1]

                black_king_pos = move

                board[move][1] = 22
                board[k][1] = 0
                black_occupancy[5] = [move]
                if previously_occupied_by != 0:
                    white_occupancy[segment_map[previously_occupied_by]].remove(move)
                turn_to_move = "w"

                evaluate = search(depth - 1)
                if evaluate < best_eval:
                    best_move = [k, move]
                best_eval = min(evaluate, best_eval)

                black_king_pos = k

                board[move][1] = previously_occupied_by
                board[k][1] = 22
                black_occupancy[5] = [k]
                if previously_occupied_by != 0:
                    white_occupancy[segment_map[previously_occupied_by]].append(move)
    if depth == 4:
        return best_move
    else:
        return best_eval


# Main loop variables --------------------------------------------------------------------------------------------------
white_king_pos = DEFAULT_int
black_king_pos = DEFAULT_int
turn_to_move = "w"
en_passant_target = DEFAULT_int
# ------------------------------------------------------------
fen_load = True
picked = False
mouse_pos = pygame.mouse.get_pos()
mouse_clicked_on = DEFAULT_tup
mouse_unclicked_on = DEFAULT_tup

# Generating the possible squares a piece can move to before the Main loop
initialize_white_pawn_moves()
initialize_black_pawn_moves()
initialize_knight_moves()
initialize_bishop_moves()
initialize_rook_moves()
initialize_queen_moves()
initialize_king_moves()

# Booleans determining whether the king or relative rooks have moved for castling
castle_conditions = {"w_k_moved": False, "w_q_r_moved": False, "w_k_r_moved": False,
                     "b_k_moved": False, "b_q_r_moved": False, "b_k_r_moved": False}

AI_to_move = False
while True:  # main loop
    window.fill((31, 31, 31))
    # Load Starting FEN once ---------------------------------
    if fen_load:
        load_fen()
        previous_board_state = copy.deepcopy(board)
        fen_load = False

    # Choosing promotion if there is one to be made by a Human Player
    if pawn_to_promote():
        promote_pawn(mouse_clicked_on, mouse_unclicked_on)

    # In loop upper precedence variables ---------------------
    update_king_position()
    initialize_white_occupancy()
    initialize_black_occupancy()
    keep_mouse_boundary()

    # Checking if the relevant pieces have moved to prevent castling
    update_castle_rights()

    if AI_to_move and not pawn_to_promote():
        t = time.time()
        previous_board_state = copy.deepcopy(board)
        optimal_move = search(4)
        if len(optimal_move) == 2:
            home_square, new_square = optimal_move[0], optimal_move[1]
            board[new_square][1] = board[home_square][1]
            board[home_square][1] = 0
        if len(optimal_move) == 3:
            home_square, new_square, promoted = optimal_move[0], optimal_move[1], optimal_move[2]
            board[new_square][1] = promoted
            board[home_square][1] = 0
        AI_to_move = False
        if previous_board_state != board:
            turn_to_move = "w"
        t = time.time() - t
        if t < 61:
            print("That took", t, "seconds.")
        else:
            print("That took", int(t // 60), "minutes and", int((t / 60 - t // 60) * 60), "seconds.")

    # Drag and drop implementation of piece movement
    if not picked and mouse_clicked_on != DEFAULT_tup and mouse_unclicked_on != DEFAULT_tup and not AI_to_move:
        previous_board_state = copy.deepcopy(board)
        move_piece()
        if previous_board_state != board:
            AI_to_move = True

        mouse_clicked_on, mouse_unclicked_on = DEFAULT_tup, DEFAULT_tup
    # Draw game objects ---------------------------------------------
    draw_board()
    render_pieces(get_square_index(mouse_clicked_on))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_clicked_on = pygame.mouse.get_pos()
            picked = True
        if event.type == MOUSEBUTTONUP:
            mouse_unclicked_on = pygame.mouse.get_pos()
            picked = False
    pygame.display.update()
    clock.tick(FPS)
