import sys
import pygame as pg
import numpy as np
import subprocess
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import game

number = 3
target = 3

if len(sys.argv) > 2:
    player1 = sys.argv[1]
    player2 = sys.argv[2]
elif len(sys.argv) == 2:
    player1 = sys.argv[1]
    player2 = input("Enter name of player 2: ")
else:
    player1 = input("Enter name of player 1: ")
    player2 = input("Enter name of player 2: ")

ticTacToeGame = game(player1, player2)
gameBoard = ticTacToeGame.board(number)

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
screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE)
pg.display.set_caption("Tic Tac Toe")
clock = pg.time.Clock()

# gameBoard info
boardSize = int(screenHeight * 0.85)
boardX, boardY = (screenWidth - boardSize) // 2, (screenHeight - boardSize) // 2
cell_width = cell_height = boardSize // number
anim_cells = {} 
name_font = pg.font.SysFont("Georgia", 28, bold=True)

won = False
running = True

while running:
    clock.tick(60) 
    
    # Drawing Background & Circles 
    screen.fill((15, 10, 40))
    pg.draw.rect(screen, (30, 0, 60),  pg.Rect(0, 0, screenWidth, screenHeight // 2))
    pg.draw.rect(screen, (10, 0, 30),  pg.Rect(0, screenHeight // 2, screenWidth, screenHeight // 2))
    pg.draw.circle(screen, (80, 0, 120),  (screenWidth // 4, screenHeight // 3), 180)
    pg.draw.circle(screen, (0, 60, 140),  (3 * screenWidth // 4, 2 * screenHeight // 3), 200)

    # Drawing Grid 
    pg.draw.rect(screen, (20, 20, 45), (boardX, boardY, boardSize, boardSize))
    for i in range(number + 1):
        pg.draw.line(screen, (100, 100, 150), (boardX + i*cell_width, boardY), (boardX + i*cell_width, boardY + boardSize), 2)
        pg.draw.line(screen, (100, 100, 150), (boardX, boardY + i*cell_height), (boardX + boardSize, boardY + i*cell_height), 2)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit(); sys.exit(0)
        
        if ticTacToeGame.turn == 2 and not won:
            ai_move(gameBoard)
            if check_win(gameBoard, ticTacToeGame.turn, target):
                won = True
                draw = False
            elif np.count_nonzero(gameBoard) == number*number:
                won = True
                draw = True
            else:
                ticTacToeGame.switch_turn()
        
        if event.type == pg.MOUSEBUTTONDOWN and not won:
            if event.button == 1:
                x, y = event.pos
                col = (x - boardX) // cell_width
                row = (y - boardY) // cell_height
                if 0 <= row < number and 0 <= col < number and gameBoard[row][col] == 0:
                    gameBoard[row][col] = ticTacToeGame.turn
                    anim_cells[(row, col)] = 4
                    if check_win(gameBoard, ticTacToeGame.turn, target):
                        won = True
                        draw= False
                    elif np.count_nonzero(gameBoard) == number*number:
                        won = True  
                        draw = True
                    else:
                        ticTacToeGame.switch_turn()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
                else:
                    screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE)
                screenWidth, screenHeight = screen.get_size()
                boardSize = int(screenHeight * 0.85)
                boardX    = (screenWidth - boardSize) // 2
                boardY    = (screenHeight - boardSize) // 2
                cell_width = cell_height = boardSize // 10

        if event.type == pg.VIDEORESIZE:
            screenWidth, screenHeight = event.w, event.h
            screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE)
            boardSize = int(screenHeight * 0.85)
            boardX    = (screenWidth - boardSize) // 2
            boardY    = (screenHeight - boardSize) // 2
            cell_width = cell_height = boardSize // 10

    # Doing animation
    anim_done = True
    for i in range(number):
        for j in range(number):
            if gameBoard[i][j] != 0:
                target_s = cell_width * 0.7
                if anim_cells.get((i, j), target_s) < target_s:
                    anim_cells[(i, j)] += 5
                    anim_done = False
                
                s = anim_cells.get((i, j), target_s)
                cell_x, cell_y = boardX + j * cell_width + cell_width // 2, boardY + i * cell_height + cell_height // 2

                if gameBoard[i][j] == 1: 
                    pg.draw.line(screen, (220, 60, 60), (cell_x-(s/2), cell_y-(s/2)), (cell_x+(s/2), cell_y+(s/2)), 4)
                    pg.draw.line(screen, (220, 60, 60), (cell_x+(s/2), cell_y-(s/2)), (cell_x-(s/2), cell_y+(s/2)), 4)
                elif gameBoard[i][j] == 2: 
                    pg.draw.circle(screen, (60, 180, 220), (cell_x, cell_y), int(s/2), 4)

    # displaying players
    p1x, p1y = boardX // 2, screenHeight // 2
    # Player 1 Symbol & Name
    pg.draw.line(screen, (220, 60, 60), (p1x-20, p1y-60), (p1x+20, p1y-20), 5)
    pg.draw.line(screen, (220, 60, 60), (p1x+20, p1y-60), (p1x-20, p1y-20), 5)
    p1name = name_font.render(ticTacToeGame.player1, True, "white")
    screen.blit(p1name, p1name.get_rect(center=(p1x, p1y + 20)))
    if ticTacToeGame.turn == 1:
        pg.draw.rect(screen, (255, 215, 0), (p1x-60, p1y-80, 120, 130), 3, border_radius=10)
        
    p2x = boardX + boardSize + (screenWidth - boardX - boardSize) // 2
    p2y = screenHeight // 2
    # Player 2 Symbol & Name
    pg.draw.circle(screen, (60, 180, 220), (p2x, p2y-40), 20, 5)
    p2name = name_font.render(ticTacToeGame.player2, True, "white")
    screen.blit(p2name, p2name.get_rect(center=(p2x, p2y + 20)))
    if ticTacToeGame.turn == 2:
        pg.draw.rect(screen, (255, 215, 0), (p2x-60, p2y-80, 120, 130), 3, border_radius=10)

    pg.display.update()

    if won and anim_done:
        
        winner_name = ticTacToeGame.player1 if ticTacToeGame.turn == 1 else ticTacToeGame.player2
        font_big = pg.font.Font(None, 100)
        font_small = pg.font.Font(None, 40)
        if draw == False:
            name=f"{winner_name} won!!"
        else :
            name=f"It's a Tie"

        text = font_big.render(name, True, (255, 140, 200))
        subtext = font_small.render("Returning...", True, (255, 255, 255))

        text_rect = text.get_rect(center=(screenWidth // 2, screenHeight // 2 - 30))
        sub_rect = subtext.get_rect(center=(screenWidth // 2, screenHeight // 2 + 50))

        start_time = pg.time.get_ticks()

        while True:
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            screen.fill((25, 10, 50)) 

            rect_w, rect_h = 500, 250
            rect_x = screenWidth // 2 - rect_w // 2
            rect_y = screenHeight // 2 - rect_h // 2

            pg.draw.rect(screen, (60, 20, 100), (rect_x, rect_y, rect_w, rect_h), border_radius=25)
            pg.draw.rect(screen, (200, 150, 255), (rect_x, rect_y, rect_w, rect_h), 3, border_radius=25)

            screen.blit(text, text_rect)
            screen.blit(subtext, sub_rect)

            pg.display.update()

            if pg.time.get_ticks() - start_time > 2000:
                break
        pg.time.delay(1500)
        x = ticTacToeGame.turn if draw == False else 3
        sys.exit(x) 
