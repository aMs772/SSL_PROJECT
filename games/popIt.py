import sys
import numpy as np
import pygame as pg
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import game
import subprocess

PopIt = game(sys.argv[1], sys.argv[2])

gameBoard = PopIt.board(6)

def check_win(gameBoard):
    return np.all(gameBoard == 1)

def valid_move(gameBoard, r_initial, r, c):
    if r == r_initial:
        if gameBoard[r][c] == 0:
            return True
    
    return False

def make_move(gameBoard, r, c):
    gameBoard[r][c] = 1

pg.init()

screenWidth, screenHeight, gameWidth = 800, 600, 600
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Pop It")

clock = pg.time.Clock()
background = pg.Surface((screenWidth, screenHeight))
background.fill("white")

row3 = pg.Surface((gameWidth, screenHeight/6))
row3.fill("yellow")

row2 = pg.Surface((gameWidth, screenHeight/6))
row2.fill("orange")

row1 = pg.Surface((gameWidth, screenHeight/6))
row1.fill("red")

row4 = pg.Surface((gameWidth, screenHeight/6))
row4.fill("blue")

row5 = pg.Surface((gameWidth, screenHeight/6))
row5.fill("green") 

row6 = pg.Surface((gameWidth, screenHeight/6))
row6.fill("purple")

rows = [row1, row2, row3, row4, row5, row6]

popped_square = pg.Surface((gameWidth/6, screenHeight/6))
popped_square.fill("black")

LINE_WIDTH = 3
lines_background = pg.Surface((gameWidth, screenHeight))

marker = 0
running = True

while running == True:
        clock.tick(5)

        screen.blit(background, (0, 0))
        
        for i in range(6):
            screen.blit(rows[i], (100, i*screenHeight/6))
                
        for i in range(6):
            for j in range(6):
                if gameBoard[i][j] == 1:
                    screen.blit(popped_square, (100 + j*gameWidth/6, i*screenHeight/6))
        
        if check_win(gameBoard) == True:
            #add striking the 5 x/o's code
            pg.time.delay(6000)
            sys.exit(PopIt.turn)
        
        for i in range(1, 6):
            pg.draw.line(background, "black", (100 + i*gameWidth/6, 0), (100 + i*gameWidth/6, screenHeight), LINE_WIDTH)
            pg.draw.line(background, "black", (100, i*screenHeight/6), (100 + gameWidth, i*screenHeight/6), LINE_WIDTH)

        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    row = y // (screenHeight // 6)
                    col = (x - 100) // (gameWidth // 6)
                    if marker == 0:
                        initial_row = row
                        marker = 1
                    if col < 0 or col > 5:
                        continue
                    elif valid_move(gameBoard, initial_row, row, col):
                        make_move(gameBoard, row, col)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    marker = 0
