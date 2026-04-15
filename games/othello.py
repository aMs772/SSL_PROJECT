import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame as pg
import subprocess
from game import game 
import numpy as np

Othello = game(sys.argv[1], sys.argv[2])

gameBoard = Othello.board(8)

gameBoard[3][3] = 1
gameBoard[3][4] = 2
gameBoard[4][3] = 2
gameBoard[4][4] = 1

def check_win(gameBoard, turn):
    return False

def valid_move(gameBoard, r, c, turn):
    if gameBoard[r][c] != 0:
        return False    
    
    def horizRight(gameBoard):
        if c == 7 or gameBoard[r][c+1] != 3-turn:
            return False
        indices = np.where(gameBoard[r][c+1:8] == turn)[0]
        nearest_pos = indices[0] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos > 0 and np.all(gameBoard[r][c+1:c+nearest_pos] == 3-turn):
            return True
    def horizLeft(gameBoard):
        if c == 0 or gameBoard[r][c-1] != 3-turn:
            return False
        indices = np.where(gameBoard[r][:c] == turn)[0]
        nearest_pos = indices[len(indices)-1] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos < c-1 and np.all(gameBoard[r][nearest_pos+1:c] == 3-turn):
            return True
    def vertDown(gameBoard):
        if r == 7 or gameBoard[r+1][c] != 3-turn:
            return False
        indices = np.where(gameBoard[r+1:8, c] == turn)[0]
        nearest_pos = indices[0] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos > 0 and np.all(gameBoard[r+1:r+nearest_pos, c] == 3-turn):
            return True
    def vertUp(gameBoard):  
        if r == 0 or gameBoard[r-1][c] != 3-turn:
            return False
        indices = np.where(gameBoard[:r, c] == turn)[0]
        nearest_pos = indices[len(indices)-1] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos < r-1 and np.all(gameBoard[nearest_pos+1:r, c] == 3-turn):
            return True 
    def diagDownRight(gameBoard):
        if r == 7 or c == 7 or gameBoard[r+1][c+1] != 3-turn:
            return False
        indices = np.where(np.diag(gameBoard[r+1:8, c+1:8]) == turn)[0]
        nearest_pos = indices[0] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos > 0 and np.all(np.diag(gameBoard[r+1:r+nearest_pos, c+1:c+nearest_pos]) == 3-turn):
            return True
    def diagUpLeft(gameBoard):
        if r == 0 or c == 0 or gameBoard[r-1][c-1] != 3-turn:
            return False
        indices = np.where(np.diag(gameBoard[:r, :c]) == turn)[0]
        nearest_pos = indices[len(indices)-1] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos < min(r, c)-1 and np.all(np.diag(gameBoard[nearest_pos+1:r, nearest_pos+1:c]) == 3-turn):
            return True
    def diagDownLeft(gameBoard):
        if r == 7 or c == 0 or gameBoard[r+1][c-1] != 3-turn:
            return False
        indices = np.where(np.diag(np.fliplr(gameBoard[r+1:8, :c])) == turn)[0]
        nearest_pos = indices[0] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos > 0 and np.all(np.diag(np.fliplr(gameBoard[r+1:r+nearest_pos, :nearest_pos])) == 3-turn):
            return True
    def diagUpRight(gameBoard):
        if r == 0 or c == 7 or gameBoard[r-1][c+1] != 3-turn:
            return False
        indices = np.where(np.diag(np.fliplr(gameBoard[:r, c+1:8])) == turn)[0]
        nearest_pos = indices[len(indices)-1] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos < min(r, 7-c)-1 and np.all(np.diag(np.fliplr(gameBoard[nearest_pos+1:r, c+1:c+nearest_pos])) == 3-turn):
            return True
        
    return horizRight(gameBoard) or horizLeft(gameBoard) or vertDown(gameBoard) or vertUp(gameBoard) or diagDownRight(gameBoard) or diagUpLeft(gameBoard) or diagDownLeft(gameBoard) or diagUpRight(gameBoard)

def make_move(gameBoard, r, c, turn):
    gameBoard[r][c] = turn
    
    def horizRight(gameBoard):
        if c == 7 or gameBoard[r][c+1] != 3-turn:
            return False
        indices = np.where(gameBoard[r][c+1:8] == turn)[0]
        nearest_pos = indices[0] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos > 0 and np.all(gameBoard[r][c+1:c+nearest_pos] == 3-turn):
            gameBoard[r][c+1:c+nearest_pos+1] = turn
    def horizLeft(gameBoard):
        if c == 0 or gameBoard[r][c-1] != 3-turn:
            return False
        indices = np.where(gameBoard[r][:c] == turn)[0]
        nearest_pos = indices[len(indices)-1] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos < c-1 and np.all(gameBoard[r][nearest_pos+1:c] == 3-turn):
            gameBoard[r][nearest_pos+1:c] = turn
    def vertDown(gameBoard):
        if r == 7 or gameBoard[r+1][c] != 3-turn:
            return False
        indices = np.where(gameBoard[r+1:8, c] == turn)[0]
        nearest_pos = indices[0] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos > 0 and np.all(gameBoard[r+1:r+1+nearest_pos, c] == 3-turn):
            gameBoard[r+1:r+nearest_pos, c] = turn
    def vertUp(gameBoard):  
        if r == 0 or gameBoard[r-1][c] != 3-turn:
            return False
        indices = np.where(gameBoard[:r, c] == turn)[0]
        nearest_pos = indices[len(indices)-1] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos < r-1 and np.all(gameBoard[nearest_pos+1:r, c] == 3-turn):
            gameBoard[nearest_pos+1:r, c] = turn 
    def diagDownRight(gameBoard):
        if r == 7 or c == 7 or gameBoard[r+1][c+1] != 3-turn:
            return False
        indices = np.where(np.diag(gameBoard[r+1:8, c+1:8]) == turn)[0]
        nearest_pos = indices[0] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos > 0 and np.all(np.diag (gameBoard[r+1:r+nearest_pos, c+1:c+nearest_pos]) == 3-turn):
            gameBoard[r+1:r+nearest_pos, c+1:c+nearest_pos] = turn
    def diagUpLeft(gameBoard):  
        if r == 0 or c == 0 or gameBoard[r-1][c-1] != 3-turn:
            return False
        indices = np.where(np.diag(gameBoard[:r, :c]) == turn)[0]
        nearest_pos = indices[len(indices)-1] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos < min(r, c)-1 and np.all(np.diag(gameBoard[nearest_pos+1:r, nearest_pos+1:c]) == 3-turn):
            gameBoard[nearest_pos+1:r, nearest_pos+1:c] = turn
    def diagDownLeft(gameBoard):
        if r == 7 or c == 0 or gameBoard[r+1][c-1] != 3-turn:
            return False
        indices = np.where(np.diag(np.fliplr(gameBoard[r+1:8, :c])) == turn)[0]
        nearest_pos = indices[0] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos > 0 and np.all(np.diag(np.fliplr(gameBoard[r+1:r+nearest_pos, :nearest_pos])) == 3-turn):
            gameBoard[r+1:r+nearest_pos, :nearest_pos] = turn
    def diagUpRight(gameBoard):
        if r == 0 or c == 7 or gameBoard[r-1][c+1] != 3-turn:
            return False
        indices = np.where(np.diag(np.fliplr(gameBoard[:r, c+1:8])) == turn)[0]
        nearest_pos = indices[len(indices)-1] if len(indices) > 0 else -1
        if nearest_pos != -1 and nearest_pos < min(r, 7-c)-1 and np.all(np.diag(np.fliplr(gameBoard[nearest_pos+1:r, c+1:c+nearest_pos])) == 3-turn):
            gameBoard[nearest_pos+1:r, c+1:c+nearest_pos] = turn    
    horizRight(gameBoard)
    horizLeft(gameBoard)
    vertDown(gameBoard)
    vertUp(gameBoard)
    diagDownRight(gameBoard)
    diagUpLeft(gameBoard)
    diagDownLeft(gameBoard)
    diagUpRight(gameBoard)

pg.init()

screenWidth, screenHeight = 800, 600
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Othello")

clock = pg.time.Clock()

background = pg.Surface((screenWidth, screenHeight))
background.fill("green")

LINE_WIDTH = 2

for i in range(1, 8):
        pg.draw.line(background, "black", (i*screenWidth/8, 0), (i*screenWidth/8, screenHeight), LINE_WIDTH)
        pg.draw.line(background, "black", (0, i*screenHeight/8), (screenWidth, i*screenHeight/8), LINE_WIDTH)

running = True
while running == True:
    clock.tick(5)

    screen.blit(background,(0,0))
    cell_width = screenWidth // 8
    cell_height = screenHeight // 8
        
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
            
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                row = y // cell_height
                col = x // cell_width
                if valid_move(gameBoard, row, col, Othello.turn):
                    make_move(gameBoard, row, col, Othello.turn)
                    if check_win(gameBoard, Othello.turn) != True:
                        Othello.switch_turn()
                    
        for i in range(8):
            for j in range(8):
                if gameBoard[i][j] == 1:
                    pg.draw.circle(screen, "black", (j*cell_width + cell_width//2, i*cell_height + cell_height//2), cell_width//4)
                elif gameBoard[i][j] == 2:
                    pg.draw.circle(screen, "white", (j*cell_width + cell_width//2, i*cell_height + cell_height//2), cell_width//4)
        pg.display.update()
    if check_win(gameBoard,Othello.turn) == True:
        sys.exit(Othello.turn)
