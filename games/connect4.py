import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame as pg
import pygame.gfxdraw
import subprocess
from game import game 
import numpy as np

C4 = game(sys.argv[1], sys.argv[2])

m = C4.board(7)

def check_win(m, turn):
    target = 4

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
       return slide_col(m)


    def anti_diag(m):
        return diag(np.fliplr(m))
    
    return horiz(m) or vert(m) or diag(m) or anti_diag(m)
pg.init()

screenWidth, screenHeight = 800, 600
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Connect 4")

clock = pg.time.Clock()

background = pg.Surface((screenWidth, screenHeight))
background.fill("orange")
LINE_WIDTH = 3
for i in range(1, 7):
    pg.draw.line(background, "red", (i*screenWidth/7, 0), (i*screenWidth/7, screenHeight), LINE_WIDTH)
    pg.draw.line(background, "red", (0, i*screenHeight/7), (screenWidth, i*screenHeight/7), LINE_WIDTH)

running = True
while running == True:
        clock.tick(4)
        cell_width = screenWidth // 7
        cell_height = screenHeight // 7

        screen.blit(background,(0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    row = y // cell_height
                    col = x // cell_width
                    row_tofill = 6
                    while row_tofill >= 0 and m[row_tofill][col] != 0:
                        row_tofill -= 1

                    if row_tofill >= 0:
                        m[row_tofill][col] = C4.turn
                        if check_win(m, C4.turn) != True:
                            C4.switch_turn()

        
        for i in range(7):
            for j in range(7):
                if m[i][j] == 2:
                    pg.draw.circle(screen, "yellow", (j*cell_width + cell_width//2, i*cell_height + cell_height//2), cell_width//4)
                elif m[i][j] == 1:
                    pg.draw.circle(screen, "blue", (j*cell_width + cell_width//2, i*cell_height + cell_height//2), cell_width//4)
        pg.display.update()
        
        if check_win(m, C4.turn) == True:
            pg.time.delay(700)
            sys.exit(C4.turn)
        

