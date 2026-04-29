import sys
import pygame as pg
import numpy as np
import subprocess
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import game

number = 3
target = 3

ticTacToeGame = game(sys.argv[1], sys.argv[2])
gameboard = ticTacToeGame.board(number)

def check_win(m, turn, target):

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

def turn(state):
    return 1 if np.sum(state) % 3 == 0 else 2

def actions(state):
    possible_actions = []
    for i in range(number):
        for j in range(number):
            if state[i][j] == 0:
                possible_actions.append((i,j))
    return possible_actions

def result(state, action):
    new_state = np.copy(state)
    new_state[action[0]][action[1]] = turn(state)
    return new_state

def terminal(state):
    return check_win(state, 1, target) or check_win(state, 2, target) or len(actions(state)) == 0

def utility(state):
    if check_win(state, 1, target):
        return 1
    elif check_win(state, 2, target):
        return -1
    else:
        return 0
    
def minimax(state, maximizing_player):
    if terminal(state):
        return utility(state), None
    
    if maximizing_player:
        max_eval = float('-inf')
        best_action = None
        for action in actions(state):
            eval, _ = minimax(result(state, action), False)
            if eval > max_eval:
                max_eval = eval
                best_action = action
        return max_eval, best_action
    else:
        min_eval = float('inf')
        best_action = None
        for action in actions(state):
            eval, _ = minimax(result(state, action), True)
            if eval < min_eval:
                min_eval = eval
                best_action = action
        return min_eval, best_action
    
def ai_move(state):
    _, action = minimax(state, turn(state) == 1)
    if action is not None:
        state[action[0]][action[1]] = turn(state)


pg.init()

screenWidth, screenHeight = 800, 600
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Tic Tac Toe")

clock = pg.time.Clock()

background = pg.Surface((screenWidth, screenHeight))
background.fill("white")
LINE_WIDTH = 3
for i in range(1, number):
    pg.draw.line(background, "black", (i*screenWidth/number, 0), (i*screenWidth/number, screenHeight), LINE_WIDTH)
    pg.draw.line(background, "black", (0, i*screenHeight/number), (screenWidth, i*screenHeight/number), LINE_WIDTH)

running = True
while running == True:
        clock.tick(60)

        screen.blit(background,(0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    row = y // (screenHeight // number)
                    col = x // (screenWidth // number)
                    if gameboard[row][col] == 0:
                        gameboard[row][col] = ticTacToeGame.turn
                        if check_win(gameboard, ticTacToeGame.turn, target) != True:
                            ticTacToeGame.switch_turn()
            
            if ticTacToeGame.turn == 2:
                ai_move(gameboard)
                if check_win(gameboard, ticTacToeGame.turn, target) != True:
                    ticTacToeGame.switch_turn()             

        cell_width = screenWidth // number
        cell_height = screenHeight // number

        for i in range(number):
            for j in range(number):
                if gameboard[i][j] == 2:
                    pg.draw.circle(screen, "red", (j*cell_width + cell_width//2, i*cell_height + cell_height//2), cell_width//4)
                elif gameboard[i][j] == 1:
                    pg.draw.line(screen, "blue", (j*cell_width + 5, i*cell_height + 5), (j*cell_width + cell_width - 5, i*cell_height + cell_height - 5), 5)
                    pg.draw.line(screen, "blue", (j*cell_width + cell_width - 5, i*cell_height + 5), (j*cell_width + 5, i*cell_height + cell_height - 5), 5)
        
        
        pg.display.update()
        if check_win(gameboard, ticTacToeGame.turn, target) == True:
            #add striking the 5 x/o's code
            pg.time.delay(700)
            sys.exit(ticTacToeGame.turn)
