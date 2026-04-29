import numpy as np
import sys
import pygame as pg
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import game
import subprocess

PopIt = game(sys.argv[1], sys.argv[2])

number = 3
# length = 3
gameBoard = PopIt.board(number)

def check_win(gameBoard):
    return np.all(gameBoard == 1)

def valid_move(gameBoard, r_initial, r, c):
    if r == r_initial:
        if gameBoard[r][c] == 0:
            return True
    
    return False

def make_move(gameBoard, r, c):
    gameBoard[r][c] = 1

def actions(gameBoard, r_initial):
    possible_moves = []
    for r in range(number):
        valid_positions = []
        for c in range(number):
            if valid_move(gameBoard, r, r, c):
                valid_positions.append(c)
        for i in range(1, len(valid_positions)+1):
            possible_moves.append((r, valid_positions[:i], i))
    return possible_moves

def result(gameBoard, action):
    new_board = gameBoard.copy()
    for i in range(action[2]):
        make_move(new_board, action[0], action[1][i])
    return new_board

def terminal(gameBoard):
    return check_win(gameBoard)

def utility(gameBoard, maximising_player):
    if check_win(gameBoard):
        return 1 if maximising_player else -1
    else:
        return 0
    
def minimax(gameBoard, r_initial, maximizing_player):
    if terminal(gameBoard):
        return utility(gameBoard, maximizing_player), None
    
    if maximizing_player:
        max_eval = float('-inf')
        best_action = None
        for action in actions(gameBoard, r_initial):
            eval, _ = minimax(result(gameBoard, action), r_initial, False)
            if eval > max_eval:
                max_eval = eval
                best_action = action
        return max_eval, best_action
    else:
        min_eval = float('inf')
        best_action = None
        for action in actions(gameBoard, r_initial):
            eval, _ = minimax(result(gameBoard, action), r_initial, True)
            if eval < min_eval:
                min_eval = eval
                best_action = action
        return min_eval, best_action
    
def ai_move(gameBoard, r_initial):
    _, best_action = minimax(gameBoard, r_initial, False)
    for i in range(best_action[2]):
        gameBoard[best_action[0]][best_action[1][i]] = 1

pg.init()

screenwidth, screenheight = 800, 600
screen = pg.display.set_mode((screenwidth, screenheight))
pg.display.set_caption("Pop It")
clock = pg.time.Clock()

boardsize = int(min(screenwidth, screenheight) * 0.8)
boardx = (screenwidth - boardsize) // 2
boardy = (screenheight - boardsize) // 2
cell = boardsize // number

popsize = int(cell * 0.85)
popoffset = (cell - popsize) // 2


board_img = pg.image.load("Media/images/boards/gemini.png").convert_alpha()
board_img = pg.transform.scale(board_img, (boardsize, boardsize))

popped_img = pg.image.load("Media/images/Symbols/c.png").convert_alpha()
popped_img = pg.transform.scale(popped_img, (popsize, popsize))

checked_img = pg.image.load("Media/images/Symbols/final.png").convert_alpha()
checked_img = pg.transform.scale(checked_img, (60, 60))

# checkbox rects
CB_SIZE = 100
p1_checkbox = pg.Rect(15, screenheight // 2 - CB_SIZE // 2, CB_SIZE, CB_SIZE)
p2_checkbox = pg.Rect(screenwidth - CB_SIZE - 15, screenheight // 2 - CB_SIZE // 2, CB_SIZE, CB_SIZE)

checked_img = pg.image.load("Media/images/Symbols/final.png").convert_alpha()
checked_img = pg.transform.scale(checked_img, (CB_SIZE, CB_SIZE))

font = pg.font.SysFont("georgia", 28, bold=True)

def draw_board():
    screen.blit(board_img, (boardx, boardy))
    for r in range(number):
        for c in range(number):
            if gameBoard[r][c] == 1:
                x = boardx + c * cell + popoffset
                y = boardy + r * cell + popoffset
                screen.blit(popped_img, (x, y))

def draw_board_checkbox():
    mx, my = pg.mouse.get_pos()

    p1_label = font.render(PopIt.player1, True, (20, 20, 60))
    p1_label_x = p1_checkbox.centerx - p1_label.get_width() // 2
    screen.blit(p1_label, (p1_label_x, p1_checkbox.y - 35))

    p2_label = font.render(PopIt.player2, True, (20, 20, 60))
    p2_label_x = p2_checkbox.centerx - p2_label.get_width() // 2
    screen.blit(p2_label, (p2_label_x, p2_checkbox.y - 35))

    if moved and PopIt.turn == 1:
        if p1_checkbox.collidepoint(mx, my):
            hover_img = pg.transform.scale(checked_img, (CB_SIZE + 10, CB_SIZE + 10))
            screen.blit(hover_img, (p1_checkbox.x - 5, p1_checkbox.y - 5))
        else:
            screen.blit(checked_img, p1_checkbox.topleft)

    elif moved and PopIt.turn == 2:
        if p2_checkbox.collidepoint(mx, my):
            hover_img = pg.transform.scale(checked_img, (CB_SIZE + 10, CB_SIZE + 10))
            screen.blit(hover_img, (p2_checkbox.x - 5, p2_checkbox.y - 5))
        else:
            screen.blit(checked_img, p2_checkbox.topleft)

marker      = 0
initial_row = 0
moved       = False
running     = True

while running:
    clock.tick(30)

    screen.fill((173, 216, 230))
    draw_board()
    draw_board_checkbox()

    if check_win():
        pg.display.update()
        pg.time.delay(1000)
        sys.exit(PopIt.turn)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos


            if PopIt.turn == 2:
                ai_move(gameBoard, initial_row)
                moved = True

            if p1_checkbox.collidepoint(x, y) and PopIt.turn == 1 and moved:
                marker = 0
                moved = False
                PopIt.switch_turn()

            # elif p2_checkbox.collidepoint(x, y) and PopIt.turn == 2 and moved:
            #     marker = 0
            #     moved = False
            #     PopIt.switch_turn()

            else:
                c = (x - boardx) // cell
                r = (y - boardy) // cell

                if 0 <= r < number and 0 <= c < number:
                    if marker == 0:
                        initial_row = r
                        marker = 1
                    if valid_move(gameBoard,initial_row, r, c):
                        make_move(gameBoard,r, c)
                        moved = True
    

    pg.display.update()
