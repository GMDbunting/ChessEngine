import pygame
import sys
from pygame.locals import *
import ctypes


# Window display variables -------------------------------------------
def convert_to_supported_resolution(x, y):
    res_x = int(x / 8) * 8
    res_y = int(y / 8) * 8
    print("Window resolution:", res_x, res_y)
    return res_x, res_y


disp_x, disp_y = convert_to_supported_resolution(900, 900)
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
b_img = pygame.image.load('images\\boardaswhite.png').convert()
board_img = pygame.transform.scale(b_img, (board_size, board_size)).convert()
w_p_img = pygame.image.load('images\\wpawn.png').convert_alpha()
w_pawn_img = pygame.transform.smoothscale(w_p_img, (square_size*0.87, square_size*0.87)).convert_alpha()
b_p_img = pygame.image.load('images\\bpawn.png').convert_alpha()
b_pawn_img = pygame.transform.smoothscale(b_p_img, (square_size*0.87, square_size*0.87)).convert_alpha()
w_n_img = pygame.image.load('images\\wknight.png').convert_alpha()
w_knight_img = pygame.transform.smoothscale(w_n_img, (square_size*scale, square_size*scale)).convert_alpha()
b_n_img = pygame.image.load('images\\bknight.png').convert_alpha()
b_knight_img = pygame.transform.smoothscale(b_n_img, (square_size*scale, square_size*scale)).convert_alpha()
w_b_img = pygame.image.load('images\\wbishop.png').convert_alpha()
w_bishop_img = pygame.transform.smoothscale(w_b_img, (square_size*scale, square_size*scale)).convert_alpha()
b_b_img = pygame.image.load('images\\bbishop.png').convert_alpha()
b_bishop_img = pygame.transform.smoothscale(b_b_img, (square_size*scale, square_size*scale)).convert_alpha()
w_r_img = pygame.image.load('images\\wrook.png').convert_alpha()
w_rook_img = pygame.transform.smoothscale(w_r_img, (square_size*scale, square_size*scale)).convert_alpha()
b_r_img = pygame.image.load('images\\brook.png').convert_alpha()
b_rook_img = pygame.transform.smoothscale(b_r_img, (square_size*scale, square_size*scale)).convert_alpha()
w_q_img = pygame.image.load('images\\wqueen.png').convert_alpha()
w_queen_img = pygame.transform.smoothscale(w_q_img, (square_size*scale, square_size*scale)).convert_alpha()
b_q_img = pygame.image.load('images\\bqueen.png').convert_alpha()
b_queen_img = pygame.transform.smoothscale(b_q_img, (square_size*scale, square_size*scale)).convert_alpha()
w_k_img = pygame.image.load('images\\wking.png').convert_alpha()
w_king_img = pygame.transform.smoothscale(w_k_img, (square_size*scale, square_size*scale)).convert_alpha()
b_k_img = pygame.image.load('images\\bking.png').convert_alpha()
b_king_img = pygame.transform.smoothscale(b_k_img, (square_size*scale, square_size*scale)).convert_alpha()
sqr_highlight0 = pygame.image.load('images\\highlight0.png').convert_alpha()
sqr_highlight0 = pygame.transform.smoothscale(sqr_highlight0, (square_size, square_size)).convert_alpha()
sqr_highlight1 = pygame.image.load('images\\highlight1.png').convert_alpha()
sqr_highlight1 = pygame.transform.smoothscale(sqr_highlight1, (square_size, square_size)).convert_alpha()
choose_piece_img = pygame.image.load('images\\ChoosePieceHighlight.png').convert()
choose_piece_img = pygame.transform.scale(choose_piece_img, (square_size, square_size * 4)).convert()

# Representation of board in code ------------------------------------
board = []
occupied_square = []
for squ_on_board in range(64):
    board.append([squ_on_board, 0])

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
    if file in range(1, 9) and rank in range(1, 9):
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
def piece_possible_squares():
    n_arr = []
    b_arr = []
    r_arr = []
    q_arr = []
    k_arr = []
    wp_arr = []
    bp_arr = []
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
        n_arr.append(temp_arr)
        temp_arr = []

    # Generating all possible squares the bishop can slide to from each square
    for b_sqr in range(64):
        b_file, b_rank = get_file_n_rank(b_sqr)

        b_f, b_r = b_file, b_rank
        while b_f in range(1, 9) and b_r in range(1, 9):
            b_f += 1
            b_r += 1
            if b_f in range(1, 9) and b_r in range(1, 9):
                temp_arr.append(get_square_index(file=b_f, rank=b_r))
        b_f, b_r = b_file, b_rank
        while b_f in range(1, 9) and b_r in range(1, 9):
            b_f += 1
            b_r -= 1
            if b_f in range(1, 9) and b_r in range(1, 9):
                temp_arr.append(get_square_index(file=b_f, rank=b_r))
        b_f, b_r = b_file, b_rank
        while b_f in range(1, 9) and b_r in range(1, 9):
            b_f -= 1
            b_r += 1
            if b_f in range(1, 9) and b_r in range(1, 9):
                temp_arr.append(get_square_index(file=b_f, rank=b_r))
        b_f, b_r = b_file, b_rank
        while b_f in range(1, 9) and b_r in range(1, 9):
            b_f -= 1
            b_r -= 1
            if b_f in range(1, 9) and b_r in range(1, 9):
                temp_arr.append(get_square_index(file=b_f, rank=b_r))
        b_arr.append(temp_arr)
        temp_arr = []

    # Generating all possible squares the rook can slide to from each square
    for r_sqr in range(64):
        r_file, r_rank = get_file_n_rank(r_sqr)

        r_f, r_r = r_file, r_rank
        while r_f in range(1, 9) and r_r in range(1, 9):
            r_f += 1
            r_r += 0
            if r_f in range(1, 9) and r_r in range(1, 9):
                temp_arr.append(get_square_index(file=r_f, rank=r_r))
        r_f, r_r = r_file, r_rank
        while r_f in range(1, 9) and r_r in range(1, 9):
            r_f += 0
            r_r -= 1
            if r_f in range(1, 9) and r_r in range(1, 9):
                temp_arr.append(get_square_index(file=r_f, rank=r_r))
        r_f, r_r = r_file, r_rank
        while r_f in range(1, 9) and r_r in range(1, 9):
            r_f -= 1
            r_r += 0
            if r_f in range(1, 9) and r_r in range(1, 9):
                temp_arr.append(get_square_index(file=r_f, rank=r_r))
        r_f, r_r = r_file, r_rank
        while r_f in range(1, 9) and r_r in range(1, 9):
            r_f += 0
            r_r += 1
            if r_f in range(1, 9) and r_r in range(1, 9):
                temp_arr.append(get_square_index(file=r_f, rank=r_r))
        r_arr.append(temp_arr)
        temp_arr = []

    # Generating all possible squares the queen can slide to from each square
    for q_sqr in range(64):
        q_file, q_rank = get_file_n_rank(q_sqr)

        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 1
            q_r += 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr.append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 1
            q_r -= 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr.append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f -= 1
            q_r += 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr.append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f -= 1
            q_r -= 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr.append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 1
            q_r += 0
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr.append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 0
            q_r -= 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr.append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f -= 1
            q_r += 0
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr.append(get_square_index(file=q_f, rank=q_r))
        q_f, q_r = q_file, q_rank
        while q_f in range(1, 9) and q_r in range(1, 9):
            q_f += 0
            q_r += 1
            if q_f in range(1, 9) and q_r in range(1, 9):
                temp_arr.append(get_square_index(file=q_f, rank=q_r))
        q_arr.append(temp_arr)
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
        k_arr.append(temp_arr)
        temp_arr = []

    # Generating all possible squares white pawns can move to from each square
    for wp_sqr in range(64):
        if wp_sqr not in range(8):
            wp_file, wp_rank = get_file_n_rank(wp_sqr)

            wp_f, wp_r = wp_file + 1, wp_rank + 1
            if wp_f in range(1, 9) and wp_r in range(1, 9):
                temp_arr.append(get_square_index(file=wp_f, rank=wp_r))
            wp_f, wp_r = wp_file + 0, wp_rank + 1
            if wp_f in range(1, 9) and wp_r in range(1, 9):
                temp_arr.append(get_square_index(file=wp_f, rank=wp_r))
            if wp_sqr in range(8, 16):
                wp_f, wp_r = wp_file + 0, wp_rank + 2
                temp_arr.append(get_square_index(file=wp_f, rank=wp_r))
            wp_f, wp_r = wp_file - 1, wp_rank + 1
            if wp_f in range(1, 9) and wp_r in range(1, 9):
                temp_arr.append(get_square_index(file=wp_f, rank=wp_r))
            wp_arr.append(temp_arr)
            temp_arr = []
        else:
            wp_arr.append([])

    # Generating all possible squares black pawns can move to from each square
    for bp_sqr in range(64):
        if bp_sqr not in range(56, 64):
            bp_file, bp_rank = get_file_n_rank(bp_sqr)

            bp_f, bp_r = bp_file - 1, bp_rank - 1
            if bp_f in range(1, 9) and bp_r in range(1, 9):
                temp_arr.append(get_square_index(file=bp_f, rank=bp_r))
            bp_f, bp_r = bp_file + 0, bp_rank - 1
            if bp_f in range(1, 9) and bp_r in range(1, 9):
                temp_arr.append(get_square_index(file=bp_f, rank=bp_r))
            if bp_sqr in range(48, 56):
                bp_f, bp_r = bp_file + 0, bp_rank - 2
                temp_arr.append(get_square_index(file=bp_f, rank=bp_r))
            bp_f, bp_r = bp_file + 1, bp_rank - 1
            if bp_f in range(1, 9) and bp_r in range(1, 9):
                temp_arr.append(get_square_index(file=bp_f, rank=bp_r))
            bp_arr.append(temp_arr)
            temp_arr = []
        else:
            bp_arr.append([])

    return [n_arr, b_arr, r_arr, q_arr, k_arr, wp_arr, bp_arr]


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


def get_occupied_squares():
    final_occupied = []
    for sqr in board:
        if sqr[1] != 0:
            final_occupied.append(sqr)
    return final_occupied


def draw_board():
    window.blit(board_img, (b_pos_x, b_pos_y))


def draw_piece(piece, square_index, specific=False, coord=(0, 0)):
    if piece != 0:
        img = b_king_img
        p_coord = DEFAULT_tup
        for pni in piece_and_img:
            if pni[0] == piece:
                img = pni[1]
        if specific:
            p_coord = (coord[0] - (square_size * 1.021 / 2), coord[1] - (square_size * 1.021 / 2))
            img = pygame.transform.smoothscale(img, (square_size*1.021, square_size*1.021)).convert_alpha()
        if not specific:
            piece_coord_x = get_square_coord(square_index)[0] + ((1 - scale) * square_size / 2) + 1
            piece_coord_y = get_square_coord(square_index)[1] + ((1 - scale) * square_size / 2) + 1
            p_coord = [piece_coord_x, piece_coord_y]
            if piece == 9:
                p_coord[0] = get_square_coord(square_index)[0] + ((1 - 0.87) * square_size / 2) + 1
                p_coord[1] = piece_coord_y + (square_size * 0.015)
            if piece == 17:
                p_coord[0] = get_square_coord(square_index)[0] + ((1 - 0.87) * square_size / 2) + 1
                p_coord[1] = piece_coord_y + (square_size * 0.015)
        window.blit(img, p_coord)


def render_pieces(omit=DEFAULT_int):
    omit_square = omit
    if omit != DEFAULT_int and board[omit][1] != 0:
        s_x = get_square_coord(omit_square)[0]
        s_y = get_square_coord(omit_square)[1]
        window.blit(sqr_highlight0, (s_x, s_y))
        # Don't Highlight any moves if there is a pawn to promote
        if not pawn_to_promote():
            for piece in range(6):
                if piece == 0 and (board[omit][1] == 10 or board[omit][1] == 18):
                    for sqr in legal_moves(omit, board[omit][1]):
                        window.blit(sqr_highlight0, get_square_coord(sqr))
                        window.blit(sqr_highlight1, get_square_coord(sqr))
                if piece == 1 and (board[omit][1] == 11 or board[omit][1] == 19):
                    for sqr in legal_moves(omit, board[omit][1]):
                        window.blit(sqr_highlight0, get_square_coord(sqr))
                        window.blit(sqr_highlight1, get_square_coord(sqr))
                if piece == 2 and (board[omit][1] == 12 or board[omit][1] == 20):
                    for sqr in legal_moves(omit, board[omit][1]):
                        window.blit(sqr_highlight0, get_square_coord(sqr))
                        window.blit(sqr_highlight1, get_square_coord(sqr))
                if piece == 3 and (board[omit][1] == 13 or board[omit][1] == 21):
                    for sqr in legal_moves(omit, board[omit][1]):
                        window.blit(sqr_highlight0, get_square_coord(sqr))
                        window.blit(sqr_highlight1, get_square_coord(sqr))
                if piece == 4 and (board[omit][1] == 14 or board[omit][1] == 22):
                    for sqr in legal_moves(omit, board[omit][1]):
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
                if piece == 5 and (board[omit][1] == 9 or board[omit][1] == 17):
                    for sqr in legal_moves(omit, board[omit][1]):
                        window.blit(sqr_highlight0, get_square_coord(sqr))
                        window.blit(sqr_highlight1, get_square_coord(sqr))
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
                    window.blit(choose_piece_img, get_square_coord(sqr+24))
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
    if mouse_pos[0] > b_pos_x + board_size-1:
        mouse_pos = (b_pos_x + board_size-1, mouse_pos[1])
    if mouse_pos[1] < b_pos_y:
        mouse_pos = (mouse_pos[0], b_pos_y)
    if mouse_pos[1] > b_pos_y + board_size-1:
        mouse_pos = (mouse_pos[0], b_pos_y + board_size-1)
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
    global king_pos
    for sqr in board:
        if turn_to_move == "w":
            if sqr[1] == 14:
                king_pos = sqr[0]
                break
        if turn_to_move == "b":
            if sqr[1] == 22:
                king_pos = sqr[0]
                break


def attacked_squares():
    attacked = [0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0]
    if turn_to_move == "w":
        k_fl, k_rnk = get_file_n_rank(king_pos)
        right_k = get_square_index(file=k_fl+1, rank=k_rnk)
        right_up_k = get_square_index(file=k_fl+1, rank=k_rnk+1)
        up_k = get_square_index(file=k_fl, rank=k_rnk+1)
        left_up_k = get_square_index(file=k_fl-1, rank=k_rnk+1)
        left_k = get_square_index(file=k_fl-1, rank=k_rnk)
        left_down_k = get_square_index(file=k_fl-1, rank=k_rnk-1)
        down_k = get_square_index(file=k_fl, rank=k_rnk-1)
        right_down_k = get_square_index(file=k_fl+1, rank=k_rnk-1)
        for p_n_pos in board:
            if p_n_pos[1] == 0:
                continue
            square, piece = p_n_pos[0], p_n_pos[1]
            # ------------------------------------------------------------------
            if piece == 17:
                for move in possible_sqr[6][square]:
                    if get_file_n_rank(square)[0] == get_file_n_rank(move)[0]:
                        continue
                    if attacked[move] == 0:
                        attacked[move] = 1
                    else:
                        attacked[move] = 2
            # ------------------------------------------------------------------
            if piece == 18:
                for move in possible_sqr[0][square]:
                    if attacked[move] == 0:
                        attacked[move] = 1
                    else:
                        attacked[move] = 2
            # ------------------------------------------------------------------
            if piece == 19:
                fl, rnk = get_file_n_rank(square)
                right_up, left_up, left_down, right_down = True, True, True, True
                for move in possible_sqr[1][square]:
                    temp_fl, temp_rnk = get_file_n_rank(move)
                    if temp_fl > fl and temp_rnk > rnk and right_up:
                        if (move == king_pos) and (right_up_k != DEFAULT_int):
                            attacked[right_up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right_up = False
                    if temp_fl < fl and temp_rnk > rnk and left_up:
                        if (move == king_pos) and (left_up_k != DEFAULT_int):
                            attacked[left_up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left_up = False
                    if temp_fl < fl and temp_rnk < rnk and left_down:
                        if (move == king_pos) and (left_down_k != DEFAULT_int):
                            attacked[left_down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left_down = False
                    if temp_fl > fl and temp_rnk < rnk and right_down:
                        if (move == king_pos) and (right_down_k != DEFAULT_int):
                            attacked[right_down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right_down = False
            # ------------------------------------------------------------------
            if piece == 20:
                fl, rnk = get_file_n_rank(square)
                right, up, left, down = True, True, True, True
                for move in possible_sqr[2][square]:
                    temp_fl, temp_rnk = get_file_n_rank(move)
                    if temp_fl > fl and temp_rnk == rnk and right:
                        if (move == king_pos) and (right_k != DEFAULT_int):
                            attacked[right_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right = False
                    if temp_fl == fl and temp_rnk > rnk and up:
                        if (move == king_pos) and (up_k != DEFAULT_int):
                            attacked[up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            up = False
                    if temp_fl < fl and temp_rnk == rnk and left:
                        if (move == king_pos) and (left_k != DEFAULT_int):
                            attacked[left_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left = False
                    if temp_fl == fl and temp_rnk < rnk and down:
                        if (move == king_pos) and (down_k != DEFAULT_int):
                            attacked[down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            down = False
            # ------------------------------------------------------------------
            if piece == 21:
                fl, rnk = get_file_n_rank(square)
                right_up, left_up, left_down, right_down = True, True, True, True
                right, up, left, down = True, True, True, True
                for move in possible_sqr[3][square]:
                    temp_fl, temp_rnk = get_file_n_rank(move)
                    if temp_fl > fl and temp_rnk > rnk and right_up:
                        if (move == king_pos) and (right_up_k != DEFAULT_int):
                            attacked[right_up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right_up = False
                    if temp_fl < fl and temp_rnk > rnk and left_up:
                        if (move == king_pos) and (left_up_k != DEFAULT_int):
                            attacked[left_up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left_up = False
                    if temp_fl < fl and temp_rnk < rnk and left_down:
                        if (move == king_pos) and (left_down_k != DEFAULT_int):
                            attacked[left_down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left_down = False
                    if temp_fl > fl and temp_rnk < rnk and right_down:
                        if (move == king_pos) and (right_down_k != DEFAULT_int):
                            attacked[right_down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right_down = False
                    if temp_fl > fl and temp_rnk == rnk and right:
                        if (move == king_pos) and (right_k != DEFAULT_int):
                            attacked[right_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right = False
                    if temp_fl == fl and temp_rnk > rnk and up:
                        if (move == king_pos) and (up_k != DEFAULT_int):
                            attacked[up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            up = False
                    if temp_fl < fl and temp_rnk == rnk and left:
                        if (move == king_pos) and (left_k != DEFAULT_int):
                            attacked[left_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left = False
                    if temp_fl == fl and temp_rnk < rnk and down:
                        if (move == king_pos) and (down_k != DEFAULT_int):
                            attacked[down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            down = False
            # ------------------------------------------------------------------
            if piece == 22:
                for move in possible_sqr[4][square]:
                    if attacked[move] == 0:
                        attacked[move] = 1
                    else:
                        attacked[move] = 2
    if turn_to_move == "b":
        k_fl, k_rnk = get_file_n_rank(king_pos)
        right_k = get_square_index(file=k_fl + 1, rank=k_rnk)
        right_up_k = get_square_index(file=k_fl + 1, rank=k_rnk + 1)
        up_k = get_square_index(file=k_fl, rank=k_rnk + 1)
        left_up_k = get_square_index(file=k_fl - 1, rank=k_rnk + 1)
        left_k = get_square_index(file=k_fl - 1, rank=k_rnk)
        left_down_k = get_square_index(file=k_fl - 1, rank=k_rnk - 1)
        down_k = get_square_index(file=k_fl, rank=k_rnk - 1)
        right_down_k = get_square_index(file=k_fl + 1, rank=k_rnk - 1)
        for p_n_pos in board:
            if p_n_pos[1] == 0:
                continue
            square, piece = p_n_pos[0], p_n_pos[1]
            # ------------------------------------------------------------------
            if piece == 9:
                for move in possible_sqr[5][square]:
                    if get_file_n_rank(square)[0] == get_file_n_rank(move)[0]:
                        continue
                    if attacked[move] == 0:
                        attacked[move] = 1
                    else:
                        attacked[move] = 2
            # ------------------------------------------------------------------
            if piece == 10:
                for move in possible_sqr[0][square]:
                    if attacked[move] == 0:
                        attacked[move] = 1
                    else:
                        attacked[move] = 2
            # ------------------------------------------------------------------
            if piece == 11:
                fl, rnk = get_file_n_rank(square)
                right_up, left_up, left_down, right_down = True, True, True, True
                for move in possible_sqr[1][square]:
                    temp_fl, temp_rnk = get_file_n_rank(move)
                    if temp_fl > fl and temp_rnk > rnk and right_up:
                        if (move == king_pos) and (right_up_k != DEFAULT_int):
                            attacked[right_up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right_up = False
                    if temp_fl < fl and temp_rnk > rnk and left_up:
                        if (move == king_pos) and (left_up_k != DEFAULT_int):
                            attacked[left_up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left_up = False
                    if temp_fl < fl and temp_rnk < rnk and left_down:
                        if (move == king_pos) and (left_down_k != DEFAULT_int):
                            attacked[left_down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left_down = False
                    if temp_fl > fl and temp_rnk < rnk and right_down:
                        if (move == king_pos) and (right_down_k != DEFAULT_int):
                            attacked[right_down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right_down = False
            # ------------------------------------------------------------------
            if piece == 12:
                fl, rnk = get_file_n_rank(square)
                right, up, left, down = True, True, True, True
                for move in possible_sqr[2][square]:
                    temp_fl, temp_rnk = get_file_n_rank(move)
                    if temp_fl > fl and temp_rnk == rnk and right:
                        if (move == king_pos) and (right_k != DEFAULT_int):
                            attacked[right_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right = False
                    if temp_fl == fl and temp_rnk > rnk and up:
                        if (move == king_pos) and (up_k != DEFAULT_int):
                            attacked[up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            up = False
                    if temp_fl < fl and temp_rnk == rnk and left:
                        if (move == king_pos) and (left_k != DEFAULT_int):
                            attacked[left_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left = False
                    if temp_fl == fl and temp_rnk < rnk and down:
                        if (move == king_pos) and (down_k != DEFAULT_int):
                            attacked[down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            down = False
            # ------------------------------------------------------------------
            if piece == 13:
                fl, rnk = get_file_n_rank(square)
                right_up, left_up, left_down, right_down = True, True, True, True
                right, up, left, down = True, True, True, True
                for move in possible_sqr[3][square]:
                    temp_fl, temp_rnk = get_file_n_rank(move)
                    if temp_fl > fl and temp_rnk > rnk and right_up:
                        if (move == king_pos) and (right_up_k != DEFAULT_int):
                            attacked[right_up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right_up = False
                    if temp_fl < fl and temp_rnk > rnk and left_up:
                        if (move == king_pos) and (left_up_k != DEFAULT_int):
                            attacked[left_up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left_up = False
                    if temp_fl < fl and temp_rnk < rnk and left_down:
                        if (move == king_pos) and (left_down_k != DEFAULT_int):
                            attacked[left_down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left_down = False
                    if temp_fl > fl and temp_rnk < rnk and right_down:
                        if (move == king_pos) and (right_down_k != DEFAULT_int):
                            attacked[right_down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right_down = False
                    if temp_fl > fl and temp_rnk == rnk and right:
                        if (move == king_pos) and (right_k != DEFAULT_int):
                            attacked[right_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            right = False
                    if temp_fl == fl and temp_rnk > rnk and up:
                        if (move == king_pos) and (up_k != DEFAULT_int):
                            attacked[up_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            up = False
                    if temp_fl < fl and temp_rnk == rnk and left:
                        if (move == king_pos) and (left_k != DEFAULT_int):
                            attacked[left_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            left = False
                    if temp_fl == fl and temp_rnk < rnk and down:
                        if (move == king_pos) and (down_k != DEFAULT_int):
                            attacked[down_k] = 1
                        if attacked[move] == 0:
                            attacked[move] = 1
                        else:
                            attacked[move] = 2
                        if board[move][1] != 0:
                            down = False
            # ------------------------------------------------------------------
            if piece == 14:
                for move in possible_sqr[4][square]:
                    if attacked[move] == 0:
                        attacked[move] = 1
                    else:
                        attacked[move] = 2
    return attacked


def check_resolves():
    fl, rnk = get_file_n_rank(king_pos)
    resolves = []
    if turn_to_move == "w":
        for sqr in possible_sqr[4][king_pos]:
            temp_fl, temp_rnk = get_file_n_rank(sqr)
            piece = board[sqr][1]
            if piece == 17:
                if temp_fl > fl and temp_rnk > rnk:
                    resolves.append(sqr)
                    if en_passant_target == sqr + 8:
                        resolves.append(en_passant_target)
                if temp_fl < fl and temp_rnk > rnk:
                    resolves.append(sqr)
                    if en_passant_target == sqr + 8:
                        resolves.append(en_passant_target)
        for sqr in possible_sqr[0][king_pos]:
            piece = board[sqr][1]
            if piece == 18:
                resolves.append(sqr)
                break
        right_up, left_up, left_down, right_down = True, True, True, True
        right, up, left, down = True, True, True, True
        for sqr in possible_sqr[3][king_pos]:
            temp_fl, temp_rnk = get_file_n_rank(sqr)
            piece = board[sqr][1]
            if piece != 0:
                if temp_fl > fl and temp_rnk > rnk and right_up:
                    if piece == 19 or piece == 21:
                        while (temp_fl != fl) and (temp_rnk != rnk):
                            resolves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                            temp_fl -= 1
                            temp_rnk -= 1
                        break
                    right_up = False
                if temp_fl < fl and temp_rnk > rnk and left_up:
                    if piece == 19 or piece == 21:
                        while (temp_fl != fl) and (temp_rnk != rnk):
                            resolves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                            temp_fl += 1
                            temp_rnk -= 1
                        break
                    left_up = False
                if temp_fl < fl and temp_rnk < rnk and left_down:
                    if piece == 19 or piece == 21:
                        while (temp_fl != fl) and (temp_rnk != rnk):
                            resolves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                            temp_fl += 1
                            temp_rnk += 1
                        break
                    left_down = False
                if temp_fl > fl and temp_rnk < rnk and right_down:
                    if piece == 19 or piece == 21:
                        while (temp_fl != fl) and (temp_rnk != rnk):
                            resolves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                            temp_fl -= 1
                            temp_rnk += 1
                        break
                    right_down = False
                if temp_fl > fl and temp_rnk == rnk and right:
                    if piece == 20 or piece == 21:
                        while temp_fl != fl:
                            resolves.append(get_square_index(file=temp_fl, rank=rnk))
                            temp_fl -= 1
                        break
                    right = False
                if temp_fl == fl and temp_rnk > rnk and up:
                    if piece == 20 or piece == 21:
                        while temp_rnk != rnk:
                            resolves.append(get_square_index(file=fl, rank=temp_rnk))
                            temp_rnk -= 1
                        break
                    up = False
                if temp_fl < fl and temp_rnk == rnk and left:
                    if piece == 20 or piece == 21:
                        while temp_fl != fl:
                            resolves.append(get_square_index(file=temp_fl, rank=rnk))
                            temp_fl += 1
                        break
                    left = False
                if temp_fl == fl and temp_rnk < rnk and down:
                    if piece == 20 or piece == 21:
                        while temp_rnk != rnk:
                            resolves.append(get_square_index(file=fl, rank=temp_rnk))
                            temp_rnk += 1
                        break
                    down = False
    if turn_to_move == "b":
        for sqr in possible_sqr[4][king_pos]:
            temp_fl, temp_rnk = get_file_n_rank(sqr)
            piece = board[sqr][1]
            if piece == 9:
                if temp_fl > fl and temp_rnk < rnk:
                    resolves.append(sqr)
                    if en_passant_target == sqr - 8:
                        resolves.append(en_passant_target)
                if temp_fl < fl and temp_rnk < rnk:
                    resolves.append(sqr)
                    if en_passant_target == sqr - 8:
                        resolves.append(en_passant_target)
        for sqr in possible_sqr[0][king_pos]:
            piece = board[sqr][1]
            if piece == 10:
                resolves.append(sqr)
                break
        right_up, left_up, left_down, right_down = True, True, True, True
        right, up, left, down = True, True, True, True
        for sqr in possible_sqr[3][king_pos]:
            temp_fl, temp_rnk = get_file_n_rank(sqr)
            piece = board[sqr][1]
            if piece != 0:
                if temp_fl > fl and temp_rnk > rnk and right_up:
                    if piece == 11 or piece == 13:
                        while (temp_fl != fl) and (temp_rnk != rnk):
                            resolves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                            temp_fl -= 1
                            temp_rnk -= 1
                        break
                    right_up = False
                if temp_fl < fl and temp_rnk > rnk and left_up:
                    if piece == 11 or piece == 13:
                        while (temp_fl != fl) and (temp_rnk != rnk):
                            resolves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                            temp_fl += 1
                            temp_rnk -= 1
                        break
                    left_up = False
                if temp_fl < fl and temp_rnk < rnk and left_down:
                    if piece == 11 or piece == 13:
                        while (temp_fl != fl) and (temp_rnk != rnk):
                            resolves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                            temp_fl += 1
                            temp_rnk += 1
                        break
                    left_down = False
                if temp_fl > fl and temp_rnk < rnk and right_down:
                    if piece == 11 or piece == 13:
                        while (temp_fl != fl) and (temp_rnk != rnk):
                            resolves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                            temp_fl -= 1
                            temp_rnk += 1
                        break
                    right_down = False
                if temp_fl > fl and temp_rnk == rnk and right:
                    if piece == 12 or piece == 13:
                        while temp_fl != fl:
                            resolves.append(get_square_index(file=temp_fl, rank=rnk))
                            temp_fl -= 1
                        break
                    right = False
                if temp_fl == fl and temp_rnk > rnk and up:
                    if piece == 12 or piece == 13:
                        while temp_rnk != rnk:
                            resolves.append(get_square_index(file=fl, rank=temp_rnk))
                            temp_rnk -= 1
                        break
                    up = False
                if temp_fl < fl and temp_rnk == rnk and left:
                    if piece == 12 or piece == 13:
                        while temp_fl != fl:
                            resolves.append(get_square_index(file=temp_fl, rank=rnk))
                            temp_fl += 1
                        break
                    left = False
                if temp_fl == fl and temp_rnk < rnk and down:
                    if piece == 12 or piece == 13:
                        while temp_rnk != rnk:
                            resolves.append(get_square_index(file=fl, rank=temp_rnk))
                            temp_rnk += 1
                        break
                    down = False
    return resolves


def piece_pins():
    fl, rnk = get_file_n_rank(king_pos)
    right_up, left_up, left_down, right_down = True, True, True, True
    right, up, left, down = True, True, True, True
    po_ru_p, po_lu_p, po_ld_p, po_rd_p = DEFAULT_int, DEFAULT_int, DEFAULT_int, DEFAULT_int
    po_r_p, po_u_p, po_l_p, po_d_p = DEFAULT_int, DEFAULT_int, DEFAULT_int, DEFAULT_int
    ru_pin_moves, lu_pin_moves, ld_pin_moves, rd_pin_moves = [], [], [], []
    r_pin_moves, u_pin_moves, l_pin_moves, d_pin_moves = [], [], [], []

    if turn_to_move == "w":
        for sqr in possible_sqr[3][king_pos]:
            temp_fl, temp_rnk = get_file_n_rank(sqr)
            piece = board[sqr][1]
            # ---------------------------------------------------------------------------
            if temp_fl > fl and temp_rnk > rnk and right_up:
                if piece != 0 and po_ru_p != DEFAULT_int:
                    right_up = False
                if piece > 16 and piece != 0 and po_ru_p == DEFAULT_int:
                    right_up = False
                if piece < 14 and piece != 0 and po_ru_p == DEFAULT_int:
                    po_ru_p = sqr
                if (piece == 19 or piece == 21) and po_ru_p != DEFAULT_int:
                    while temp_fl != fl and temp_rnk != rnk:
                        ru_pin_moves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                        temp_fl -= 1
                        temp_rnk -= 1
            # ---------------------------------------------------------------------------
            if temp_fl < fl and temp_rnk > rnk and left_up:
                if piece != 0 and po_lu_p != DEFAULT_int:
                    left_up = False
                if piece > 16 and piece != 0 and po_lu_p == DEFAULT_int:
                    left_up = False
                if piece < 14 and piece != 0 and po_lu_p == DEFAULT_int:
                    po_lu_p = sqr
                if (piece == 19 or piece == 21) and po_lu_p != DEFAULT_int:
                    while temp_fl != fl and temp_rnk != rnk:
                        lu_pin_moves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                        temp_fl += 1
                        temp_rnk -= 1
            # ---------------------------------------------------------------------------
            if temp_fl < fl and temp_rnk < rnk and left_down:
                if piece != 0 and po_ld_p != DEFAULT_int:
                    left_down = False
                if piece > 16 and piece != 0 and po_ld_p == DEFAULT_int:
                    left_down = False
                if piece < 14 and piece != 0 and po_ld_p == DEFAULT_int:
                    po_ld_p = sqr
                if (piece == 19 or piece == 21) and po_ld_p != DEFAULT_int:
                    while temp_fl != fl and temp_rnk != rnk:
                        ld_pin_moves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                        temp_fl += 1
                        temp_rnk += 1
            # ---------------------------------------------------------------------------
            if temp_fl > fl and temp_rnk < rnk and right_down:
                if piece != 0 and po_rd_p != DEFAULT_int:
                    right_down = False
                if piece > 16 and piece != 0 and po_rd_p == DEFAULT_int:
                    right_down = False
                if piece < 14 and piece != 0 and po_rd_p == DEFAULT_int:
                    po_rd_p = sqr
                if (piece == 19 or piece == 21) and po_rd_p != DEFAULT_int:
                    while temp_fl != fl and temp_rnk != rnk:
                        rd_pin_moves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                        temp_fl -= 1
                        temp_rnk += 1
            # ---------------------------------------------------------------------------
            if temp_fl > fl and temp_rnk == rnk and right:
                if piece != 0 and po_r_p != DEFAULT_int:
                    right = False
                if piece > 16 and piece != 0 and po_r_p == DEFAULT_int:
                    right = False
                if piece < 14 and piece != 0 and po_r_p == DEFAULT_int:
                    po_r_p = sqr
                if (piece == 20 or piece == 21) and po_r_p != DEFAULT_int:
                    while temp_fl != fl:
                        r_pin_moves.append(get_square_index(file=temp_fl, rank=rnk))
                        temp_fl -= 1
            # ---------------------------------------------------------------------------
            if temp_fl == fl and temp_rnk > rnk and up:
                if piece != 0 and po_u_p != DEFAULT_int:
                    up = False
                if piece > 16 and piece != 0 and po_u_p == DEFAULT_int:
                    up = False
                if piece < 14 and piece != 0 and po_u_p == DEFAULT_int:
                    po_u_p = sqr
                if (piece == 20 or piece == 21) and po_u_p != DEFAULT_int:
                    while temp_rnk != rnk:
                        u_pin_moves.append(get_square_index(file=fl, rank=temp_rnk))
                        temp_rnk -= 1
            # ---------------------------------------------------------------------------
            if temp_fl < fl and temp_rnk == rnk and left:
                if piece != 0 and po_l_p != DEFAULT_int:
                    left = False
                if piece > 16 and piece != 0 and po_l_p == DEFAULT_int:
                    left = False
                if piece < 14 and piece != 0 and po_l_p == DEFAULT_int:
                    po_l_p = sqr
                if (piece == 20 or piece == 21) and po_l_p != DEFAULT_int:
                    while temp_fl != fl:
                        l_pin_moves.append(get_square_index(file=temp_fl, rank=rnk))
                        temp_fl += 1
            # ---------------------------------------------------------------------------
            if temp_fl == fl and temp_rnk < rnk and down:
                if piece != 0 and po_d_p != DEFAULT_int:
                    down = False
                if piece > 16 and piece != 0 and po_d_p == DEFAULT_int:
                    down = False
                if piece < 14 and piece != 0 and po_d_p == DEFAULT_int:
                    po_d_p = sqr
                if (piece == 20 or piece == 21) and po_d_p != DEFAULT_int:
                    while temp_rnk != rnk:
                        d_pin_moves.append(get_square_index(file=fl, rank=temp_rnk))
                        temp_rnk += 1

    if turn_to_move == "b":
        for sqr in possible_sqr[3][king_pos]:
            temp_fl, temp_rnk = get_file_n_rank(sqr)
            piece = board[sqr][1]
            # ---------------------------------------------------------------------------
            if temp_fl > fl and temp_rnk > rnk and right_up:
                if piece != 0 and po_ru_p != DEFAULT_int:
                    right_up = False
                if piece <= 14 and piece != 0 and po_ru_p == DEFAULT_int:
                    right_up = False
                if piece > 16 and piece != 0 and po_ru_p == DEFAULT_int:
                    po_ru_p = sqr
                if (piece == 11 or piece == 13) and po_ru_p != DEFAULT_int:
                    while temp_fl != fl and temp_rnk != rnk:
                        ru_pin_moves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                        temp_fl -= 1
                        temp_rnk -= 1
            # ---------------------------------------------------------------------------
            if temp_fl < fl and temp_rnk > rnk and left_up:
                if piece != 0 and po_lu_p != DEFAULT_int:
                    left_up = False
                if piece <= 14 and piece != 0 and po_lu_p == DEFAULT_int:
                    left_up = False
                if piece > 16 and piece != 0 and po_lu_p == DEFAULT_int:
                    po_lu_p = sqr
                if (piece == 11 or piece == 13) and po_lu_p != DEFAULT_int:
                    while temp_fl != fl and temp_rnk != rnk:
                        lu_pin_moves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                        temp_fl += 1
                        temp_rnk -= 1
            # ---------------------------------------------------------------------------
            if temp_fl < fl and temp_rnk < rnk and left_down:
                if piece != 0 and po_ld_p != DEFAULT_int:
                    left_down = False
                if piece <= 14 and piece != 0 and piece != 0 and po_ld_p == DEFAULT_int:
                    left_down = False
                if piece > 16 and piece != 0 and po_ld_p == DEFAULT_int:
                    po_ld_p = sqr
                if (piece == 11 or piece == 13) and po_ld_p != DEFAULT_int:
                    while temp_fl != fl and temp_rnk != rnk:
                        ld_pin_moves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                        temp_fl += 1
                        temp_rnk += 1
            # ---------------------------------------------------------------------------
            if temp_fl > fl and temp_rnk < rnk and right_down:
                if piece != 0 and po_rd_p != DEFAULT_int:
                    right_down = False
                if piece <= 14 and piece != 0 and po_rd_p == DEFAULT_int:
                    right_down = False
                if piece > 16 and piece != 0 and po_rd_p == DEFAULT_int:
                    po_rd_p = sqr
                if (piece == 11 or piece == 13) and po_rd_p != DEFAULT_int:
                    while temp_fl != fl and temp_rnk != rnk:
                        rd_pin_moves.append(get_square_index(file=temp_fl, rank=temp_rnk))
                        temp_fl -= 1
                        temp_rnk += 1
            # ---------------------------------------------------------------------------
            if temp_fl > fl and temp_rnk == rnk and right:
                if piece != 0 and po_r_p != DEFAULT_int:
                    right = False
                if piece <= 14 and piece != 0 and po_r_p == DEFAULT_int:
                    right = False
                if piece > 16 and piece != 0 and po_r_p == DEFAULT_int:
                    po_r_p = sqr
                if (piece == 12 or piece == 13) and po_r_p != DEFAULT_int:
                    while temp_fl != fl:
                        r_pin_moves.append(get_square_index(file=temp_fl, rank=rnk))
                        temp_fl -= 1
            # ---------------------------------------------------------------------------
            if temp_fl == fl and temp_rnk > rnk and up:
                if piece != 0 and po_u_p != DEFAULT_int:
                    up = False
                if piece <= 14 and piece != 0 and po_u_p == DEFAULT_int:
                    up = False
                if piece > 16 and piece != 0 and po_u_p == DEFAULT_int:
                    po_u_p = sqr
                if (piece == 12 or piece == 13) and po_u_p != DEFAULT_int:
                    while temp_rnk != rnk:
                        u_pin_moves.append(get_square_index(file=fl, rank=temp_rnk))
                        temp_rnk -= 1
            # ---------------------------------------------------------------------------
            if temp_fl < fl and temp_rnk == rnk and left:
                if piece != 0 and po_l_p != DEFAULT_int:
                    left = False
                if piece <= 14 and piece != 0 and po_l_p == DEFAULT_int:
                    left = False
                if piece > 16 and piece != 0 and po_l_p == DEFAULT_int:
                    po_l_p = sqr
                if (piece == 12 or piece == 13) and po_l_p != DEFAULT_int:
                    while temp_fl != fl:
                        l_pin_moves.append(get_square_index(file=temp_fl, rank=rnk))
                        temp_fl += 1
            # ---------------------------------------------------------------------------
            if temp_fl == fl and temp_rnk < rnk and down:
                if piece != 0 and po_d_p != DEFAULT_int:
                    down = False
                if piece <= 14 and piece != 0 and po_d_p == DEFAULT_int:
                    down = False
                if piece > 16 and piece != 0 and po_d_p == DEFAULT_int:
                    po_d_p = sqr
                if (piece == 12 or piece == 13) and po_d_p != DEFAULT_int:
                    while temp_rnk != rnk:
                        d_pin_moves.append(get_square_index(file=fl, rank=temp_rnk))
                        temp_rnk += 1

    pin = [po_ru_p, po_lu_p, po_ld_p, po_rd_p,
           po_r_p, po_u_p, po_l_p, po_d_p]
    resolve = [ru_pin_moves, lu_pin_moves, ld_pin_moves, rd_pin_moves,
               r_pin_moves, u_pin_moves, l_pin_moves, d_pin_moves]

    pin_n_resolve = []
    for val in range(8):
        if not resolve[val]:
            pin_n_resolve.append([DEFAULT_int, resolve[val]])
        else:
            pin_n_resolve.append([pin[val], resolve[val]])
    return pin_n_resolve


def legal_moves(square, piece):
    global board
    attacked, check, doublecheck = attacked_squares(), False, False
    if attacked[king_pos] != 0:
        if attacked[king_pos] == 1:
            check = True
        else:
            doublecheck = True
    pins = piece_pins()
    resolve_squares = []
    if check:
        resolve_squares = check_resolves()
    legal_piece_moves = []

    # Legal moves for white pieces
    if piece != 0 and turn_to_move == "w":
        # -----------------------------------------------------------------
        if piece == 9:
            wp_fl = get_file_n_rank(square)[0]
            up = True
            for wp_sqr in possible_sqr[5][square]:
                if en_passant_target == wp_sqr:
                    legal_piece_moves.append(en_passant_target)
                    if 32 <= king_pos <= 39:
                        left_dir = True
                        right_dir = True
                        board[en_passant_target][1] = 9
                        board[square][1] = 0
                        board[en_passant_target - 8][1] = 0
                        temp_kng_fl, kng_rnk = get_file_n_rank(king_pos)
                        while temp_kng_fl > 1 and left_dir:
                            temp_kng_fl -= 1
                            check_for_piece = get_square_index(file=temp_kng_fl, rank=kng_rnk)
                            if board[check_for_piece][1] != 0:
                                if board[check_for_piece][1] == 20 or board[check_for_piece][1] == 21:
                                    legal_piece_moves.remove(en_passant_target)
                                left_dir = False
                        temp_kng_fl, kng_rnk = get_file_n_rank(king_pos)
                        while temp_kng_fl < 8 and right_dir:
                            temp_kng_fl += 1
                            check_for_piece = get_square_index(file=temp_kng_fl, rank=kng_rnk)
                            if board[check_for_piece][1] != 0:
                                if board[check_for_piece][1] == 20 or board[check_for_piece][1] == 21:
                                    legal_piece_moves.remove(en_passant_target)
                                right_dir = False
                        board[en_passant_target][1] = 0
                        board[square][1] = 9
                        board[en_passant_target - 8][1] = 17
                temp_wp_fl = get_file_n_rank(wp_sqr)[0]
                if board[wp_sqr][1] != 0 and wp_fl == temp_wp_fl:
                    up = False
                if board[wp_sqr][1] > 16 and board[wp_sqr][1] != 0 and wp_fl != temp_wp_fl:
                    legal_piece_moves.append(wp_sqr)
                if board[wp_sqr][1] == 0 and wp_fl == temp_wp_fl and up:
                    legal_piece_moves.append(wp_sqr)
            # For Piece pins
            temp_hold = []
            for wp_pin in pins:
                if wp_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in wp_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for wp_resolve in legal_piece_moves:
                    if wp_resolve in resolve_squares:
                        temp_hold.append(wp_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 10:
            for wn_sqr in possible_sqr[0][square]:
                if board[wn_sqr][1] > 14 or board[wn_sqr][1] == 0:
                    legal_piece_moves.append(wn_sqr)
            # For Piece pins
            temp_hold = []
            for wn_pin in pins:
                if wn_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in wn_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for wn_resolve in legal_piece_moves:
                    if wn_resolve in resolve_squares:
                        temp_hold.append(wn_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 11:
            fl, rnk = get_file_n_rank(square)
            right_up, left_up, left_down, right_down = True, True, True, True
            for wb_sqr in possible_sqr[1][square]:
                temp_fl, temp_rnk = get_file_n_rank(wb_sqr)
                if board[wb_sqr][1] <= 14 and board[wb_sqr][1] != 0:
                    if temp_fl > fl and temp_rnk > rnk:
                        right_up = False
                    if temp_fl < fl and temp_rnk > rnk:
                        left_up = False
                    if temp_fl < fl and temp_rnk < rnk:
                        left_down = False
                    if temp_fl > fl and temp_rnk < rnk:
                        right_down = False
                if board[wb_sqr][1] > 16 and board[wb_sqr][1] != 0:
                    if right_up and temp_fl > fl and temp_rnk > rnk:
                        legal_piece_moves.append(wb_sqr)
                        right_up = False
                    if left_up and temp_fl < fl and temp_rnk > rnk:
                        legal_piece_moves.append(wb_sqr)
                        left_up = False
                    if left_down and temp_fl < fl and temp_rnk < rnk:
                        legal_piece_moves.append(wb_sqr)
                        left_down = False
                    if right_down and temp_fl > fl and temp_rnk < rnk:
                        legal_piece_moves.append(wb_sqr)
                        right_down = False
                if board[wb_sqr][1] == 0:
                    if right_up and temp_fl > fl and temp_rnk > rnk:
                        legal_piece_moves.append(wb_sqr)
                    if left_up and temp_fl < fl and temp_rnk > rnk:
                        legal_piece_moves.append(wb_sqr)
                    if left_down and temp_fl < fl and temp_rnk < rnk:
                        legal_piece_moves.append(wb_sqr)
                    if right_down and temp_fl > fl and temp_rnk < rnk:
                        legal_piece_moves.append(wb_sqr)
            # For Piece pins
            temp_hold = []
            for wb_pin in pins:
                if wb_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in wb_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for wb_resolve in legal_piece_moves:
                    if wb_resolve in resolve_squares:
                        temp_hold.append(wb_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 12:
            fl, rnk = get_file_n_rank(square)
            right, left, up, down = True, True, True, True
            for wr_sqr in possible_sqr[2][square]:
                temp_fl, temp_rnk = get_file_n_rank(wr_sqr)
                if board[wr_sqr][1] <= 14 and board[wr_sqr][1] != 0:
                    if temp_fl > fl and temp_rnk == rnk:
                        right = False
                    if temp_fl == fl and temp_rnk > rnk:
                        up = False
                    if temp_fl < fl and temp_rnk == rnk:
                        left = False
                    if temp_fl == fl and temp_rnk < rnk:
                        down = False
                if board[wr_sqr][1] > 16 and board[wr_sqr][1] != 0:
                    if right and temp_fl > fl and temp_rnk == rnk:
                        legal_piece_moves.append(wr_sqr)
                        right = False
                    if up and temp_fl == fl and temp_rnk > rnk:
                        legal_piece_moves.append(wr_sqr)
                        up = False
                    if left and temp_fl < fl and temp_rnk == rnk:
                        legal_piece_moves.append(wr_sqr)
                        left = False
                    if down and temp_fl == fl and temp_rnk < rnk:
                        legal_piece_moves.append(wr_sqr)
                        down = False
                if board[wr_sqr][1] == 0:
                    if right and temp_fl > fl and temp_rnk == rnk:
                        legal_piece_moves.append(wr_sqr)
                    if up and temp_fl == fl and temp_rnk > rnk:
                        legal_piece_moves.append(wr_sqr)
                    if left and temp_fl < fl and temp_rnk == rnk:
                        legal_piece_moves.append(wr_sqr)
                    if down and temp_fl == fl and temp_rnk < rnk:
                        legal_piece_moves.append(wr_sqr)
            # For Piece pins
            temp_hold = []
            for wr_pin in pins:
                if wr_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in wr_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for wr_resolve in legal_piece_moves:
                    if wr_resolve in resolve_squares:
                        temp_hold.append(wr_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 13:
            fl, rnk = get_file_n_rank(square)
            right_up, left_up, left_down, right_down = True, True, True, True
            right, left, up, down = True, True, True, True
            for wq_sqr in possible_sqr[3][square]:
                temp_fl, temp_rnk = get_file_n_rank(wq_sqr)
                if board[wq_sqr][1] <= 14 and board[wq_sqr][1] != 0:
                    if temp_fl > fl and temp_rnk > rnk:
                        right_up = False
                    if temp_fl < fl and temp_rnk > rnk:
                        left_up = False
                    if temp_fl < fl and temp_rnk < rnk:
                        left_down = False
                    if temp_fl > fl and temp_rnk < rnk:
                        right_down = False
                if board[wq_sqr][1] > 16 and board[wq_sqr][1] != 0:
                    if right_up and temp_fl > fl and temp_rnk > rnk:
                        legal_piece_moves.append(wq_sqr)
                        right_up = False
                    if left_up and temp_fl < fl and temp_rnk > rnk:
                        legal_piece_moves.append(wq_sqr)
                        left_up = False
                    if left_down and temp_fl < fl and temp_rnk < rnk:
                        legal_piece_moves.append(wq_sqr)
                        left_down = False
                    if right_down and temp_fl > fl and temp_rnk < rnk:
                        legal_piece_moves.append(wq_sqr)
                        right_down = False
                if board[wq_sqr][1] == 0:
                    if right_up and temp_fl > fl and temp_rnk > rnk:
                        legal_piece_moves.append(wq_sqr)
                    if left_up and temp_fl < fl and temp_rnk > rnk:
                        legal_piece_moves.append(wq_sqr)
                    if left_down and temp_fl < fl and temp_rnk < rnk:
                        legal_piece_moves.append(wq_sqr)
                    if right_down and temp_fl > fl and temp_rnk < rnk:
                        legal_piece_moves.append(wq_sqr)
                if board[wq_sqr][1] <= 14 and board[wq_sqr][1] != 0:
                    if temp_fl > fl and temp_rnk == rnk:
                        right = False
                    if temp_fl == fl and temp_rnk > rnk:
                        up = False
                    if temp_fl < fl and temp_rnk == rnk:
                        left = False
                    if temp_fl == fl and temp_rnk < rnk:
                        down = False
                if board[wq_sqr][1] > 16 and board[wq_sqr][1] != 0:
                    if right and temp_fl > fl and temp_rnk == rnk:
                        legal_piece_moves.append(wq_sqr)
                        right = False
                    if up and temp_fl == fl and temp_rnk > rnk:
                        legal_piece_moves.append(wq_sqr)
                        up = False
                    if left and temp_fl < fl and temp_rnk == rnk:
                        legal_piece_moves.append(wq_sqr)
                        left = False
                    if down and temp_fl == fl and temp_rnk < rnk:
                        legal_piece_moves.append(wq_sqr)
                        down = False
                if board[wq_sqr][1] == 0:
                    if right and temp_fl > fl and temp_rnk == rnk:
                        legal_piece_moves.append(wq_sqr)
                    if up and temp_fl == fl and temp_rnk > rnk:
                        legal_piece_moves.append(wq_sqr)
                    if left and temp_fl < fl and temp_rnk == rnk:
                        legal_piece_moves.append(wq_sqr)
                    if down and temp_fl == fl and temp_rnk < rnk:
                        legal_piece_moves.append(wq_sqr)
            # For Piece pins
            temp_hold = []
            for wq_pin in pins:
                if wq_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in wq_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for wq_resolve in legal_piece_moves:
                    if wq_resolve in resolve_squares:
                        temp_hold.append(wq_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 14:
            for wk_sqr in possible_sqr[4][square]:
                if board[wk_sqr][1] > 14 or board[wk_sqr][1] == 0:
                    if attacked[wk_sqr] == 0:
                        legal_piece_moves.append(wk_sqr)

    # Legal moves for black pieces
    if piece != 0 and turn_to_move == "b":
        # -----------------------------------------------------------------
        if piece == 17:
            bp_fl = get_file_n_rank(square)[0]
            down = True
            for bp_sqr in possible_sqr[6][square]:
                if en_passant_target == bp_sqr:
                    legal_piece_moves.append(en_passant_target)
                    if 24 <= king_pos <= 31:
                        left_dir = True
                        right_dir = True
                        board[en_passant_target][1] = 17
                        board[square][1] = 0
                        board[en_passant_target + 8][1] = 0
                        temp_kng_fl, kng_rnk = get_file_n_rank(king_pos)
                        while temp_kng_fl > 1 and left_dir:
                            temp_kng_fl -= 1
                            check_for_piece = get_square_index(file=temp_kng_fl, rank=kng_rnk)
                            if board[check_for_piece][1] != 0:
                                if board[check_for_piece][1] == 12 or board[check_for_piece][1] == 13:
                                    legal_piece_moves.remove(en_passant_target)
                                left_dir = False
                        temp_kng_fl, kng_rnk = get_file_n_rank(king_pos)
                        while temp_kng_fl < 8 and right_dir:
                            temp_kng_fl += 1
                            check_for_piece = get_square_index(file=temp_kng_fl, rank=kng_rnk)
                            if board[check_for_piece][1] != 0:
                                if board[check_for_piece][1] == 12 or board[check_for_piece][1] == 13:
                                    legal_piece_moves.remove(en_passant_target)
                                right_dir = False
                        board[en_passant_target][1] = 0
                        board[square][1] = 17
                        board[en_passant_target + 8][1] = 9
                temp_bp_fl = get_file_n_rank(bp_sqr)[0]
                if board[bp_sqr][1] != 0 and bp_fl == temp_bp_fl:
                    down = False
                if board[bp_sqr][1] < 16 and board[bp_sqr][1] != 0 and bp_fl != temp_bp_fl:
                    legal_piece_moves.append(bp_sqr)
                if board[bp_sqr][1] == 0 and bp_fl == temp_bp_fl and down:
                    legal_piece_moves.append(bp_sqr)
            # For Piece pins
            temp_hold = []
            for bp_pin in pins:
                if bp_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in bp_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for bp_resolve in legal_piece_moves:
                    if bp_resolve in resolve_squares:
                        temp_hold.append(bp_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 18:
            for bn_sqr in possible_sqr[0][square]:
                if board[bn_sqr][1] < 17 or board[bn_sqr][1] == 0:
                    legal_piece_moves.append(bn_sqr)
            # For Piece pins
            temp_hold = []
            for bn_pin in pins:
                if bn_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in bn_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for bn_resolve in legal_piece_moves:
                    if bn_resolve in resolve_squares:
                        temp_hold.append(bn_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 19:
            fl, rnk = get_file_n_rank(square)
            right_up, left_up, left_down, right_down = True, True, True, True
            for bb_sqr in possible_sqr[1][square]:
                temp_fl, temp_rnk = get_file_n_rank(bb_sqr)
                if board[bb_sqr][1] > 16 and board[bb_sqr][1] != 0:
                    if temp_fl > fl and temp_rnk > rnk:
                        right_up = False
                    if temp_fl < fl and temp_rnk > rnk:
                        left_up = False
                    if temp_fl < fl and temp_rnk < rnk:
                        left_down = False
                    if temp_fl > fl and temp_rnk < rnk:
                        right_down = False
                if board[bb_sqr][1] <= 14 and board[bb_sqr][1] != 0:
                    if right_up and temp_fl > fl and temp_rnk > rnk:
                        legal_piece_moves.append(bb_sqr)
                        right_up = False
                    if left_up and temp_fl < fl and temp_rnk > rnk:
                        legal_piece_moves.append(bb_sqr)
                        left_up = False
                    if left_down and temp_fl < fl and temp_rnk < rnk:
                        legal_piece_moves.append(bb_sqr)
                        left_down = False
                    if right_down and temp_fl > fl and temp_rnk < rnk:
                        legal_piece_moves.append(bb_sqr)
                        right_down = False
                if board[bb_sqr][1] == 0:
                    if right_up and temp_fl > fl and temp_rnk > rnk:
                        legal_piece_moves.append(bb_sqr)
                    if left_up and temp_fl < fl and temp_rnk > rnk:
                        legal_piece_moves.append(bb_sqr)
                    if left_down and temp_fl < fl and temp_rnk < rnk:
                        legal_piece_moves.append(bb_sqr)
                    if right_down and temp_fl > fl and temp_rnk < rnk:
                        legal_piece_moves.append(bb_sqr)
            # For Piece pins
            temp_hold = []
            for bb_pin in pins:
                if bb_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in bb_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for bb_resolve in legal_piece_moves:
                    if bb_resolve in resolve_squares:
                        temp_hold.append(bb_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 20:
            fl, rnk = get_file_n_rank(square)
            right, left, up, down = True, True, True, True
            for br_sqr in possible_sqr[2][square]:
                temp_fl, temp_rnk = get_file_n_rank(br_sqr)
                if board[br_sqr][1] > 16 and board[br_sqr][1] != 0:
                    if temp_fl > fl and temp_rnk == rnk:
                        right = False
                    if temp_fl == fl and temp_rnk > rnk:
                        up = False
                    if temp_fl < fl and temp_rnk == rnk:
                        left = False
                    if temp_fl == fl and temp_rnk < rnk:
                        down = False
                if board[br_sqr][1] <= 14 and board[br_sqr][1] != 0:
                    if right and temp_fl > fl and temp_rnk == rnk:
                        legal_piece_moves.append(br_sqr)
                        right = False
                    if up and temp_fl == fl and temp_rnk > rnk:
                        legal_piece_moves.append(br_sqr)
                        up = False
                    if left and temp_fl < fl and temp_rnk == rnk:
                        legal_piece_moves.append(br_sqr)
                        left = False
                    if down and temp_fl == fl and temp_rnk < rnk:
                        legal_piece_moves.append(br_sqr)
                        down = False
                if board[br_sqr][1] == 0:
                    if right and temp_fl > fl and temp_rnk == rnk:
                        legal_piece_moves.append(br_sqr)
                    if up and temp_fl == fl and temp_rnk > rnk:
                        legal_piece_moves.append(br_sqr)
                    if left and temp_fl < fl and temp_rnk == rnk:
                        legal_piece_moves.append(br_sqr)
                    if down and temp_fl == fl and temp_rnk < rnk:
                        legal_piece_moves.append(br_sqr)
            # For Piece pins
            temp_hold = []
            for br_pin in pins:
                if br_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in br_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for br_resolve in legal_piece_moves:
                    if br_resolve in resolve_squares:
                        temp_hold.append(br_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 21:
            fl, rnk = get_file_n_rank(square)
            right_up, left_up, left_down, right_down = True, True, True, True
            right, left, up, down = True, True, True, True
            for bq_sqr in possible_sqr[3][square]:
                temp_fl, temp_rnk = get_file_n_rank(bq_sqr)
                if board[bq_sqr][1] > 16 and board[bq_sqr][1] != 0:
                    if temp_fl > fl and temp_rnk > rnk:
                        right_up = False
                    if temp_fl < fl and temp_rnk > rnk:
                        left_up = False
                    if temp_fl < fl and temp_rnk < rnk:
                        left_down = False
                    if temp_fl > fl and temp_rnk < rnk:
                        right_down = False
                if board[bq_sqr][1] <= 14 and board[bq_sqr][1] != 0:
                    if right_up and temp_fl > fl and temp_rnk > rnk:
                        legal_piece_moves.append(bq_sqr)
                        right_up = False
                    if left_up and temp_fl < fl and temp_rnk > rnk:
                        legal_piece_moves.append(bq_sqr)
                        left_up = False
                    if left_down and temp_fl < fl and temp_rnk < rnk:
                        legal_piece_moves.append(bq_sqr)
                        left_down = False
                    if right_down and temp_fl > fl and temp_rnk < rnk:
                        legal_piece_moves.append(bq_sqr)
                        right_down = False
                if board[bq_sqr][1] == 0:
                    if right_up and temp_fl > fl and temp_rnk > rnk:
                        legal_piece_moves.append(bq_sqr)
                    if left_up and temp_fl < fl and temp_rnk > rnk:
                        legal_piece_moves.append(bq_sqr)
                    if left_down and temp_fl < fl and temp_rnk < rnk:
                        legal_piece_moves.append(bq_sqr)
                    if right_down and temp_fl > fl and temp_rnk < rnk:
                        legal_piece_moves.append(bq_sqr)
                if board[bq_sqr][1] > 16 and board[bq_sqr][1] != 0:
                    if temp_fl > fl and temp_rnk == rnk:
                        right = False
                    if temp_fl == fl and temp_rnk > rnk:
                        up = False
                    if temp_fl < fl and temp_rnk == rnk:
                        left = False
                    if temp_fl == fl and temp_rnk < rnk:
                        down = False
                if board[bq_sqr][1] <= 14 and board[bq_sqr][1] != 0:
                    if right and temp_fl > fl and temp_rnk == rnk:
                        legal_piece_moves.append(bq_sqr)
                        right = False
                    if up and temp_fl == fl and temp_rnk > rnk:
                        legal_piece_moves.append(bq_sqr)
                        up = False
                    if left and temp_fl < fl and temp_rnk == rnk:
                        legal_piece_moves.append(bq_sqr)
                        left = False
                    if down and temp_fl == fl and temp_rnk < rnk:
                        legal_piece_moves.append(bq_sqr)
                        down = False
                if board[bq_sqr][1] == 0:
                    if right and temp_fl > fl and temp_rnk == rnk:
                        legal_piece_moves.append(bq_sqr)
                    if up and temp_fl == fl and temp_rnk > rnk:
                        legal_piece_moves.append(bq_sqr)
                    if left and temp_fl < fl and temp_rnk == rnk:
                        legal_piece_moves.append(bq_sqr)
                    if down and temp_fl == fl and temp_rnk < rnk:
                        legal_piece_moves.append(bq_sqr)
            # For Piece pins
            temp_hold = []
            for bq_pin in pins:
                if bq_pin[0] == square:
                    for move in legal_piece_moves:
                        if move in bq_pin[1]:
                            temp_hold.append(move)
                    legal_piece_moves = temp_hold
            # For checks
            if check:
                temp_hold = []
                for bq_resolve in legal_piece_moves:
                    if bq_resolve in resolve_squares:
                        temp_hold.append(bq_resolve)
                legal_piece_moves = temp_hold
            # For double checks
            if doublecheck:
                legal_piece_moves = []
        # -----------------------------------------------------------------
        if piece == 22:
            for bk_sqr in possible_sqr[4][square]:
                if board[bk_sqr][1] < 16 or board[bk_sqr][1] == 0:
                    if attacked[bk_sqr] == 0:
                        legal_piece_moves.append(bk_sqr)
    return legal_piece_moves


def pawn_to_promote():
    for sqr in range(64):
        if (sqr in range(0, 8)) or (sqr in range(56, 64)):
            if board[sqr][1] == 9 or board[sqr][1] == 17:
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
    if attacked[king_pos] != 0:
        if attacked[king_pos] == 1:
            check = True
        else:
            double = True
    if turn_to_move == "w":
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
    if turn_to_move == "b":
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
    global turn_to_move
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


# When using saved mouse positions as input make sure to reset them after the piece is moved
def move_piece():
    from_index = get_square_index(mouse_clicked_on)
    to_index = get_square_index(mouse_unclicked_on)
    global board
    global turn_to_move
    global en_passant_target
    from_file, from_rank = get_file_n_rank(from_index)
    to_file, to_rank = get_file_n_rank(to_index)
    q_side_castle, k_side_castle = can_castle()

    # Do not move anything if there is a pawn on the back ranks
    if not pawn_to_promote():
        # Checking if a piece occupies the starting square
        piece = board[from_index][1]
        if piece != 0:
            # Checking if move is legal
            if to_index in legal_moves(from_index, board[from_index][1]):
                # Implementation of en passant capture
                if to_index == en_passant_target:
                    if piece == 9:
                        board[en_passant_target - 8][1] = 0
                    if piece == 17:
                        board[en_passant_target + 8][1] = 0
                # Set En passant target square
                if (piece == 9) and (to_rank == from_rank + 2) or (piece == 17) and (to_rank == from_rank - 2):
                    if (piece == 9) and (to_rank == from_rank + 2):
                        en_passant_target = get_square_index(file=from_file, rank=from_rank + 1)
                    if (piece == 17) and (to_rank == from_rank - 2):
                        en_passant_target = get_square_index(file=from_file, rank=from_rank - 1)
                else:
                    en_passant_target = DEFAULT_int
                # --------------------------------------------------------------------

                # Making move by replacing piece on chosen square
                board[to_index] = [to_index, piece]
                board[from_index][1] = 0
                # Switching player turn
                switch_turn()
            # Implementation of castling
            if turn_to_move == "w":
                if k_side_castle and from_index == 4 and (to_index == 6 or to_index == 7):
                    castle_king("king side")
                    switch_turn()
                    en_passant_target = DEFAULT_int
                if q_side_castle and from_index == 4 and (to_index == 2 or to_index == 0):
                    castle_king("queen side")
                    switch_turn()
                    en_passant_target = DEFAULT_int
            if turn_to_move == "b":
                if k_side_castle and from_index == 60 and (to_index == 62 or to_index == 63):
                    castle_king("king side")
                    switch_turn()
                    en_passant_target = DEFAULT_int
                if q_side_castle and from_index == 60 and (to_index == 58 or to_index == 56):
                    castle_king("queen side")
                    switch_turn()
                    en_passant_target = DEFAULT_int


# Main loop variables ----------------------------------------
king_pos = DEFAULT_int
turn_to_move = "w"
en_passant_target = DEFAULT_int
# ------------------------------------------------------------
fen_load = True
picked = False
mouse_pos = pygame.mouse.get_pos()
mouse_clicked_on = DEFAULT_tup
mouse_unclicked_on = DEFAULT_tup

# Generating the possible squares a piece can move to before the Main loop
possible_sqr = piece_possible_squares()

# Booleans determining whether the king or relative rooks have moved for castling
castle_conditions = {"w_k_moved": False, "w_q_r_moved": False, "w_k_r_moved": False,
                     "b_k_moved": False, "b_q_r_moved": False, "b_k_r_moved": False}

while True:  # main loop
    window.fill((31, 31, 31))
    # Load Starting FEN once ---------------------------------
    while fen_load:
        load_fen()
        fen_load = False

    # In loop upper precedence variables ---------------------
    update_king_position()
    occupied_square = get_occupied_squares()
    keep_mouse_boundary()

    # Choosing promotion if there is one to be made by a Human Player
    if pawn_to_promote():
        promote_pawn(mouse_clicked_on, mouse_unclicked_on)

    # Checking if the relevant pieces have moved to prevent castling
    update_castle_rights()

    # Drag and drop implementation of piece movement
    if not picked and mouse_clicked_on != DEFAULT_tup and mouse_unclicked_on != DEFAULT_tup:
        move_piece()
        mouse_clicked_on, mouse_unclicked_on = DEFAULT_tup, DEFAULT_tup

    # Draw game objects ---------------------------------------------
    draw_board()
    render_pieces(get_square_index(mouse_clicked_on))

    for event in pygame.event.get():
        if event.type == QUIT:
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
