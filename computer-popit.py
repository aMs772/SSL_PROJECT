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

screenWidth, screenHeight, gameWidth = 800, 600, 600
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Pop It")

clock = pg.time.Clock()
background = pg.Surface((screenWidth, screenHeight))
background.fill("white")

row3 = pg.Surface((gameWidth, screenHeight/number))
row3.fill("yellow")

row2 = pg.Surface((gameWidth, screenHeight/number))
row2.fill("orange")

row1 = pg.Surface((gameWidth, screenHeight/number))
row1.fill("red")

row4 = pg.Surface((gameWidth, screenHeight/number))
row4.fill("blue")

row5 = pg.Surface((gameWidth, screenHeight/number))
row5.fill("green") 

row6 = pg.Surface((gameWidth, screenHeight/number))
row6.fill("purple")

rows = [row1, row2, row3, row4, row5, row6]

popped_square = pg.Surface((gameWidth/number, screenHeight/number))
popped_square.fill("black")

LINE_WIDTH = 3
lines_background = pg.Surface((gameWidth, screenHeight))

marker = 0
running = True

while running == True:
        clock.tick(5)

        screen.blit(background, (0, 0))
        
        for i in range(number):
            screen.blit(rows[i], (100, i*screenHeight/number))
                
        for i in range(number):
            for j in range(number):
                if gameBoard[i][j] == 1:
                    screen.blit(popped_square, (100 + j*gameWidth/number, i*screenHeight/number))
        
        if check_win(gameBoard) == True:
            #add striking the 5 x/o's code
            pg.time.delay(6000)
            sys.exit(PopIt.turn)
        
        for i in range(1, number + 1):
            pg.draw.line(background, "black", (100 + i*gameWidth/number, 0), (100 + i*gameWidth/number, screenHeight), LINE_WIDTH)
            pg.draw.line(background, "black", (100, i*screenHeight/number), (100 + gameWidth, i*screenHeight/number), LINE_WIDTH)

        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    row = y // (screenHeight // number)
                    col = (x - 100) // (gameWidth // number)
                    if marker == 0:
                        initial_row = row
                        marker = 1
                    if col < 0 or col > number - 1:
                        continue
                    if PopIt.turn == 1:
                        if valid_move(gameBoard, initial_row, row, col):
                            make_move(gameBoard, row, col)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    marker = 0
                    PopIt.switch_turn()

            if PopIt.turn == 2:
                ai_move(gameBoard, initial_row)
                PopIt.switch_turn()

            if check_win(gameBoard) == True:
                sys.exit(PopIt.turn)        

        pg.display.update()
    


