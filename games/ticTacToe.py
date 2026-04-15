import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame as pg
import subprocess
from game import game 
import numpy as np

ticTacToeGame = game(sys.argv[1], sys.argv[2])

m = ticTacToeGame.board(10)

def check_win(m, turn):
    target = 5

    def horiz(m):
        """Slide a target-wide window across columns recursively."""  
        if m.shape[1] < target:
            return False
        if np.any(np.all(m[:, :target] == turn, axis=1)):
            return True
        return horiz(m[:, 1:])         
      
    def vert(m):
        return horiz(m.T)              

    def diag_at_origin(m):
        """True if main diagonal of top-left target×target block is all 1s."""
        if m.shape[0] < target or m.shape[1] < target:
            return False
        return bool(np.all(np.diag(m[:target, :target]) == turn))

    def slide_row(m):
        """Checks diagonals whose top cell is in row 0 → slide right."""
        if m.shape[1] < target:
            return False
        if diag_at_origin(m):
            return True
        return slide_row(m[:, 1:])      

    def slide_col(m):
        """Checks diagonals whose leftmost cell is in col 0 → slide down."""
        if m.shape[0] < target:
            return False
        if slide_row(m):
            return True
        return slide_col(m[1:, :])      
    def diag(m):
        return slide_col(m[:,1:])


    def anti_diag(m):
        return diag(np.fliplr(m))
    
    return horiz(m) or vert(m) or diag(m) or anti_diag(m)
pg.init()

screenWidth, screenHeight = 800, 600
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Tic Tac Toe")

clock = pg.time.Clock()

background = pg.Surface((screenWidth, screenHeight))
background.fill("white")
LINE_WIDTH = 3
for i in range(1, 10):
    pg.draw.line(background, "black", (i*screenWidth/10, 0), (i*screenWidth/10, screenHeight), LINE_WIDTH)
    pg.draw.line(background, "black", (0, i*screenHeight/10), (screenWidth, i*screenHeight/10), LINE_WIDTH)

running = True
while running == True:
        clock.tick(5)

        screen.blit(background,(0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    row = y // 60
                    col = x // 80
                    if m[row][col] == 0:
                        m[row][col] = ticTacToeGame.turn
                        if check_win(m, ticTacToeGame.turn) != True:
                            ticTacToeGame.switch_turn()

        cell_width = 80
        cell_height = 60
        
        for i in range(10):
            for j in range(10):
                if m[i][j] == 2:
                    pg.draw.circle(screen, "red", (j*cell_width + cell_width//2, i*cell_height + cell_height//2), cell_width//4)
                elif m[i][j] == 1:
                    pg.draw.line(screen, "blue", (j*cell_width + 5, i*cell_height + 5), (j*cell_width + cell_width - 5, i*cell_height + cell_height - 5), 5)
                    pg.draw.line(screen, "blue", (j*cell_width + cell_width - 5, i*cell_height + 5), (j*cell_width + 5, i*cell_height + cell_height - 5), 5)
        
        
        
        pg.display.update()
        if check_win(m, ticTacToeGame.turn) == True:
            #add striking the 5 x/o's code
            pg.time.delay(700)
            sys.exit(ticTacToeGame.turn)
