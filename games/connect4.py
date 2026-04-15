import sys
import pygame as pg
from game import Game 
import numpy as np

connect4Game = Game(sys.argv[1], sys.argv[2])

n = 7

m = connect4Game.board(n)

def check_win(m, turn):
    target = 5

    def horiz(m):
        """Slide a target-wide window across columns recursively."""  
        if m.shape[1] < target:
            return False
        if np.any(np.all(m[:, :target] == turn, axis=1)):
            return True
        return horiz(m[:, 1:])         
    
    return horiz(m.T) or horiz(m)
pg.init()
screenWidth, screenHeight = 800, 600
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Tic Tac Toe")

clock = pg.time.Clock()

LINE_WIDTH = 5
screen.fill("white")
running = True
while running == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    running = False
            
        pg.display.update()

        cell_width = screenWidth/n
        cell_height = screenHeight/n
        
        for i in range(n):
            for j in range(n):
                if m[i][j] == 2:
                    pg.draw.circle(screen, "red", (j*cell_width + cell_width//2, i*cell_height + cell_height//2), cell_width//4)
                elif m[i][j] == 1:
                    pg.draw.line(screen, "blue", (j*cell_width + 5, i*cell_height + 5), (j*cell_width + cell_width - 5, i*cell_height + cell_height - 5), 5)
                    pg.draw.line(screen, "blue", (j*cell_width + cell_width - 5, i*cell_height + 5), (j*cell_width + 5, i*cell_height + cell_height - 5), 5)
        
        for i in range(1,n):
            for j in range(1,n):
                pg.draw.line(screen, "black", (i*screenWidth/n, 0), (i*screenWidth/n, screenHeight), LINE_WIDTH)
                
                pg.draw.line(screen, "black", (0, j*screenHeight/n), (screenWidth, j*screenHeight/n), LINE_WIDTH)
        if check_win(m, connect4Game.turn) == True:
            print("Player " + str(connect4Game.turn) + " wins!")
            running = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    col = int(x // cell_width)
                    column = m[:, col]
                    empty_rows = np.where(column == 0)[0]

                    if len(empty_rows) > 0:
                            row = empty_rows[-1]  

                            if m[row][col] == 0:
                                m[row][col] = connect4Game.turn
                                connect4Game.switch_turn()
