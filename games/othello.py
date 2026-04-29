import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame as pg
import numpy as np
from game import game 

Othello = game(sys.argv[1], sys.argv[2])

gameBoard = Othello.board(8)

# initial setup
gameBoard[3][3] = 1
gameBoard[3][4] = 2
gameBoard[4][3] = 2
gameBoard[4][4] = 1


# GAME LOGIC 

def check_win(gameBoard, turn):
    if np.count_nonzero(gameBoard == 1) + np.count_nonzero(gameBoard == 2) == 64:
        if np.count_nonzero(gameBoard == 1) > np.count_nonzero(gameBoard == 2):
            return 1
        elif np.count_nonzero(gameBoard == 1) < np.count_nonzero(gameBoard == 2):
            return 2
        else:
            return 0
    elif turn == 1 and not valid_moves(gameBoard, turn):
        return 2
    elif turn == 2 and not valid_moves(gameBoard, turn):
        return 1
    else:
        return -1


def valid_moves(gameBoard, turn):
    moves = []
    for i in range(8):
        for j in range(8):
            if valid_move(gameBoard, i, j, turn):
                moves.append((i, j))
    return moves


def flip_direction(gameBoard, r, c, turn, dr, dc, make_move):
    opponent = 3 - turn

    max_steps = min(
        (7 - r) if dr > 0 else (r if dr < 0 else 7),
        (7 - c) if dc > 0 else (c if dc < 0 else 7)
    )

    if max_steps == 0:
        return False

    rows = r + dr * np.arange(1, max_steps + 1)
    cols = c + dc * np.arange(1, max_steps + 1)

    line = gameBoard[rows, cols]

    if line[0] != opponent:
        return False

    turn_positions = np.where(line == turn)[0]

    if len(turn_positions) == 0:
        return False

    nearest = turn_positions[0]

    if np.all(line[:nearest] == opponent):
        if make_move:
            gameBoard[rows[:nearest], cols[:nearest]] = turn
        return True

    return False


def valid_move(gameBoard, r, c, turn):
    if gameBoard[r][c] != 0:
        return False

    return (
        flip_direction(gameBoard, r, c, turn, 0, 1, False) or
        flip_direction(gameBoard, r, c, turn, 0, -1, False) or
        flip_direction(gameBoard, r, c, turn, 1, 0, False) or
        flip_direction(gameBoard, r, c, turn, -1, 0, False) or
        flip_direction(gameBoard, r, c, turn, 1, 1, False) or
        flip_direction(gameBoard, r, c, turn, -1, -1, False) or
        flip_direction(gameBoard, r, c, turn, 1, -1, False) or
        flip_direction(gameBoard, r, c, turn, -1, 1, False)
    )


def make_move(gameBoard, r, c, turn):
    gameBoard[r][c] = turn

    flip_direction(gameBoard, r, c, turn, 0, 1, True)
    flip_direction(gameBoard, r, c, turn, 0, -1, True)
    flip_direction(gameBoard, r, c, turn, 1, 0, True)
    flip_direction(gameBoard, r, c, turn, -1, 0, True)
    flip_direction(gameBoard, r, c, turn, 1, 1, True)
    flip_direction(gameBoard, r, c, turn, -1, -1, True)
    flip_direction(gameBoard, r, c, turn, 1, -1, True)
    flip_direction(gameBoard, r, c, turn, -1, 1, True)



pg.init()

screenWidth, screenHeight = 1000, 700
screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE)
pg.display.set_caption("Othello")

clock = pg.time.Clock()
name_font = pg.font.SysFont("Georgia", 28, bold=True)

# centered board
boardSize = int(screenHeight * 0.85)
boardX = (screenWidth - boardSize) // 2
boardY = (screenHeight - boardSize) // 2
cell_width = boardSize // 8
cell_height = boardSize // 8

running = True
while running:
    clock.tick(60)

    # BACKGROUND 
    screen.fill((200, 230, 220))
    pg.draw.rect(screen, (185, 220, 210), (0, 0, screenWidth, screenHeight // 2))
    pg.draw.rect(screen, (170, 205, 195), (0, screenHeight // 2, screenWidth, screenHeight // 2))

    # BOARD 
    pg.draw.rect(screen, (140, 220, 140), (boardX, boardY, boardSize, boardSize))

    grid_color = (50, 100, 50)

    # GRID 
    for i in range(1, 8):
        pg.draw.line(screen, grid_color,
                     (boardX + i * cell_width, boardY),
                     (boardX + i * cell_width, boardY + boardSize), 2)

        pg.draw.line(screen, grid_color,
                     (boardX, boardY + i * cell_height),
                     (boardX + boardSize, boardY + i * cell_height), 2)

    # EVENTS 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                col = (x - boardX) // cell_width
                row = (y - boardY) // cell_height

                if 0 <= row < 8 and 0 <= col < 8:
                    if valid_move(gameBoard, row, col, Othello.turn):
                        make_move(gameBoard, row, col, Othello.turn)
                        if check_win(gameBoard, Othello.turn) == -1:
                            Othello.switch_turn()

        if event.type == pg.VIDEORESIZE:
            screenWidth, screenHeight = event.w, event.h
            screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE)

            boardSize = int(screenHeight * 0.85)
            boardX = (screenWidth - boardSize) // 2
            boardY = (screenHeight - boardSize) // 2
            cell_width = boardSize // 8
            cell_height = boardSize // 8

    # DRAW DISCS 
    for i in range(8):
        for j in range(8):
            cx = boardX + j * cell_width + cell_width // 2
            cy = boardY + i * cell_height + cell_height // 2

            if gameBoard[i][j] == 1:
                pg.draw.circle(screen, (0, 0, 0), (cx, cy), cell_width // 2 - 5)
            elif gameBoard[i][j] == 2:
                pg.draw.circle(screen, (255, 255, 255), (cx, cy), cell_width // 2 - 5)

    # DISC COUNT 
    black_count = np.count_nonzero(gameBoard == 1)
    white_count = np.count_nonzero(gameBoard == 2)

    # LEFT PANEL
    p1x, p1y = boardX // 2, screenHeight // 2

    if Othello.turn == 1:
        pg.draw.rect(screen, (255, 215, 0), (p1x - 80, p1y - 110, 160, 180), 3, border_radius=12)

    pg.draw.circle(screen, (0, 0, 0), (p1x, p1y - 60), 25)

    p1text = name_font.render(Othello.player1, True, "black")
    screen.blit(p1text, p1text.get_rect(center=(p1x, p1y - 10)))

    p1score = name_font.render(f"Discs: {black_count}", True, "black")
    screen.blit(p1score, p1score.get_rect(center=(p1x, p1y + 30)))

    # RIGHT PANEL 
    p2x = boardX + boardSize + (screenWidth - boardX - boardSize) // 2
    p2y = screenHeight // 2

    if Othello.turn == 2:
        pg.draw.rect(screen, (255, 215, 0), (p2x - 80, p2y - 110, 160, 180), 3, border_radius=12)

    pg.draw.circle(screen, (255, 255, 255), (p2x, p2y - 60), 25)

    p2text = name_font.render(Othello.player2, True, "black")
    screen.blit(p2text, p2text.get_rect(center=(p2x, p2y - 10)))

    p2score = name_font.render(f"Discs: {white_count}", True, "black")
    screen.blit(p2score, p2score.get_rect(center=(p2x, p2y + 30)))

    if check_win(gameBoard, Othello.turn) == 1:
        #add winning animation here
        pg.time.delay(1500)
        sys.exit(1)
    elif check_win(gameBoard, Othello.turn) == 2:
        #add winning animation here
        pg.time.delay(1500)
        sys.exit(2)
    elif check_win(gameBoard, Othello.turn) == 0:
        #add draw animation here
        pg.time.delay(1500)
        sys.exit(3)
        
    pg.display.update()
