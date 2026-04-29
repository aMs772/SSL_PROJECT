import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame as pg
from game import game 
import numpy as np

if len(sys.argv) > 2:
    player1 = sys.argv[1]
    player2 = sys.argv[2]
elif len(sys.argv) == 2:
    player1 = sys.argv[1]
    player2 = input("Enter name of player 2: ")
else:
    player1 = input("Enter name of player 1: ")
    player2 = input("Enter name of player 2: ")


connect4 = game(sys.argv[1], sys.argv[2])
gameBoard = connect4.board(7)

# background colour change
bg_p1 = (255, 120, 120)   # red
bg_p2 = (120, 170, 255)   # blue
bg_t = 0

def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

def check_win(m, turn):
    target = 4

    def horiz(m):
        if m.shape[1] < target:
            return False
        if np.any(np.all(m[:, :target] == turn, axis=1)):
            return True
        return horiz(m[:, 1:])

    def vert(m):
        return horiz(m.T)

    def diag_at_origin(m):
        if m.shape[0] < target or m.shape[1] < target:
            return False
        return bool(np.all(np.diag(m[:target, :target]) == turn))

    def slide_row(m):
        if m.shape[1] < target:
            return False
        if diag_at_origin(m):
            return True
        return slide_row(m[:, 1:])

    def slide_col(m):
        if m.shape[0] < target:
            return False
        if slide_row(m):
            return True
        return slide_col(m[1:, :])

    def diag(m):
        return slide_col(m)

    def anti_diag(m):
        return diag(np.fliplr(m))

    return horiz(m) or vert(m) or diag(m) or anti_diag(m)

#drawing the board and bg colour changing effects
def draw_board(screen, board, hover_col, turn):
    global bg_t
    speed = 0.05
    if turn == 1:
        bg_t = max(0, bg_t - speed)
    else:
        bg_t = min(1, bg_t + speed)

    bg_color = lerp_color(bg_p1, bg_p2, bg_t)
    screen.fill(bg_color)

    # drawing the entire board
    pg.draw.rect(screen, (50, 100, 160), (boardx, boardy, boardw, boardh), border_radius=20)

    # drawing the cells
    for r in range(7):
        for c in range(7):
            cx = int(boardx + c * cell_width + cell_width // 2)
            cy = int(boardy + r * cell_height + cell_height // 2)

            if board[r][c] == 0:
                pg.draw.circle(screen, bg_color, (cx, cy), int(cell_width // 2.5))
            else:
                color = (255, 60, 60) if board[r][c] == 1 else (255, 220, 0)
                pg.draw.circle(screen, color, (cx, cy), int(cell_width // 2.5))

    # for hover highlight
    if hover_col is not None:
        hover_col = max(0, min(6, hover_col))
        col_x = boardx + hover_col * cell_width

        hover_rect = pg.Surface((cell_width, boardh), pg.SRCALPHA)
        pg.draw.rect(hover_rect, (255, 255, 255, 22), (0, 0, cell_width, boardh), border_radius=8)
        screen.blit(hover_rect, (col_x, boardy))

        color = (255, 80, 80) if turn == 1 else (255, 215, 0)
        hx = col_x + cell_width // 2
        hy = int(boardy - cell_height * 0.6)
        pg.draw.circle(screen, color, (hx, hy), int(cell_width // 2.5))

    # Player 1 info and panels
    p1x, p1y = boardx // 2, screenheight // 2
    p1name = name_font.render(connect4.player1, True, "blue")
    screen.blit(p1name, p1name.get_rect(center=(p1x, p1y + 20)))
    pg.draw.circle(screen, (255, 60, 60), (p1x, p1y - 40), int(cell_width // 2.5))
#highlights 
    if connect4.turn == 1:
        pg.draw.rect(screen, (255, 215, 0), (p1x - 60, p1y - 80, 120, 130), 3, border_radius=10)

    # Player 2 panels and info
    p2x = boardx + boardw + (screenwidth - boardx - boardw) // 2
    p2y = screenheight // 2
    pg.draw.circle(screen, (255, 220, 0), (p2x, p2y - 40), int(cell_width // 2.5))

    p2name = name_font.render(connect4.player2, True, "red")
    screen.blit(p2name, p2name.get_rect(center=(p2x, p2y + 20)))
#highlights
    if connect4.turn == 2:
        pg.draw.rect(screen, (255, 215, 0), (p2x - 60, p2y - 80, 120, 130), 3, border_radius=10)


def animate_fall(screen, board, col, target_row, turn):
    current_y = boardy - (cell_height // 2)
    target_y = boardy + (target_row * cell_height) + (cell_height // 2)
    target_x = boardx + (col * cell_width) + (cell_width // 2)

    color = (255, 0, 0) if turn == 1 else (255, 255, 0)

    speed = 0
    gravity = 2
#animates the falling of the circle
    while current_y < target_y:
        draw_board(screen, board, None, turn)

        speed += gravity
        current_y += speed

        if current_y > target_y:
            current_y = target_y

        pg.draw.circle(screen, color, (int(target_x), int(current_y)), int(cell_width // 2.5))

        pg.display.update()
        clock.tick(60)

    draw_board(screen, board, None, turn)
    pg.draw.circle(screen, color, (int(target_x), int(target_y)), int(cell_width // 2.5))
    pg.display.update()


pg.init()

screenwidth, screenheight = 800, 600
screen = pg.display.set_mode((screenwidth, screenheight))
pg.display.set_caption("Connect 4")

boardh = boardw = int(screenheight * 0.78)
boardx = (screenwidth - boardw) // 2
boardy = (screenheight - boardh) // 2

cell_width = boardw // 7
cell_height = boardh // 7

name_font = pg.font.SysFont("Georgia", 28, bold=True)
clock = pg.time.Clock()
fullscreen = False


running = True
won=False
draw=False
while running:
    clock.tick(60)

    for event in pg.event.get():
        #if closed
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
#if the mouse is in btweent he board then hover effect occurs
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pg.mouse.get_pos()
            if boardx < x < boardx + boardw and boardy < y < boardy + boardh:
                col = int((x - boardx) // cell_width)
                col = max(0, min(6, col))
                row_tofill = 6

                while row_tofill >= 0 and gameBoard[row_tofill][col] != 0:
                    row_tofill -= 1
#checks which row is empty to be filled
                if row_tofill >= 0:
                    animate_fall(screen,gameBoard, col, row_tofill, connect4.turn)
                    gameBoard[row_tofill][col] = connect4.turn
#handles the logic for win draw and turn changing
                    if check_win(gameBoard, connect4.turn):
                        won = True
                        draw = False
                    elif np.count_nonzero(gameBoard) == 49:
                        won = True
                        draw = True
                    else:
                        connect4.switch_turn()
#for using the game in fullscreen
        if event.type == pg.KEYDOWN and event.key == pg.K_F11:
            fullscreen = not fullscreen

            if fullscreen:
                screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            else:
                screen = pg.display.set_mode((800, 600), pg.RESIZABLE)

            screenwidth, screenheight = screen.get_size()

            boardh = boardw = int(screenheight * 0.78)
            boardx = (screenwidth - boardw) // 2
            boardy = (screenheight - boardh) // 2
            cell_width = boardw // 7
            cell_height = boardh // 7
#for using the game in fullscreen

        if event.type == pg.VIDEORESIZE and not fullscreen:
            screenwidth, screenheight = event.w, event.h
            screen = pg.display.set_mode((screenwidth, screenheight), pg.RESIZABLE)

            boardh = boardw = int(screenheight * 0.78)
            boardx = (screenwidth - boardw) // 2
            boardy = (screenheight - boardh) // 2
            cell_width = boardw // 7
            cell_height = boardh // 7

    x, y = pg.mouse.get_pos()
    if boardx < x < boardx + boardw and boardy < y < boardy + boardh:
        hover_col = int((x - boardx) // cell_width)
        hover_col = max(0, min(6, hover_col))
    else:
        hover_col = None

    draw_board(screen, connect4.board, hover_col, connect4.turn)
    pg.display.update()
#runs this part only if the game is over
    if won == True:
        winner_name = connect4.player1 if connect4.turn == 1 else connect4.player2

        font_big = pg.font.Font(None, 100)
        font_small = pg.font.Font(None, 40)
#prints the player won and waits for some time
        if draw == False:
            name = f"{winner_name} won!!"
        else:
            name = "It's a Tie"

        text = font_big.render(name, True, (255, 140, 200))
        subtext = font_small.render("Returning...", True, (255, 255, 255))

        text_rect = text.get_rect(center=(screenwidth // 2, screenheight // 2 - 30))
        sub_rect = subtext.get_rect(center=(screenwidth // 2, screenheight // 2 + 50))

        start_time = pg.time.get_ticks()

        while True:
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            screen.fill((25, 10, 50)) 

            rect_w, rect_h = 500, 250
            rect_x = screenwidth // 2 - rect_w // 2
            rect_y = screenheight // 2 - rect_h // 2

            pg.draw.rect(screen, (60, 20, 100), (rect_x, rect_y, rect_w, rect_h), border_radius=25)
            pg.draw.rect(screen, (200, 150, 255), (rect_x, rect_y, rect_w, rect_h), 3, border_radius=25)

            screen.blit(text, text_rect)
            screen.blit(subtext, sub_rect)

            pg.display.update()
#for waiting of 1sec
            if pg.time.get_ticks() - start_time > 1000:
                break
#returns to game.py accordingly 
        x = connect4.turn if draw == False else 3
        sys.exit(x)
