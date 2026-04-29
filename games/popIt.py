import sys
import numpy as np
import pygame as pg
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import game

PopIt = game(sys.argv[1], sys.argv[2])
gameBoard = PopIt.board(6)

ROWS = 6
COLS = 6

def check_win():
    return np.all(gameBoard == 1)

def valid_move(gameBoard,r_initial, r, c):
    return r == r_initial and gameBoard[r][c] == 0

def make_move(gameBoard,r, c):
    gameBoard[r][c] = 1


pg.init()

screenwidth, screenheight = 800, 600
screen = pg.display.set_mode((screenwidth, screenheight))
pg.display.set_caption("Pop It")
clock = pg.time.Clock()

boardsize = int(min(screenwidth, screenheight) * 0.8)
boardx = (screenwidth - boardsize) // 2
boardy = (screenheight - boardsize) // 2
cell = boardsize // COLS

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
    for r in range(ROWS):
        for c in range(COLS):
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

            if p1_checkbox.collidepoint(x, y) and PopIt.turn == 1 and moved:
                marker = 0
                moved = False
                PopIt.switch_turn()

            elif p2_checkbox.collidepoint(x, y) and PopIt.turn == 2 and moved:
                marker = 0
                moved = False
                PopIt.switch_turn()

            else:
                c = (x - boardx) // cell
                r = (y - boardy) // cell

                if 0 <= r < ROWS and 0 <= c < COLS:
                    if marker == 0:
                        initial_row = r
                        marker = 1
                    if valid_move(gameBoard,initial_row, r, c):
                        make_move(gameBoard,r, c)
                        moved = True
    

    pg.display.update()
