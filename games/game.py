#!/usr/local/bin/python3.10
import sys
import csv
import os
import numpy as np
import subprocess
import pygame as pg
from datetime import datetime

#player names taken as command line arguments from main.sh
player1 = sys.argv[1]
player2 = sys.argv[2]
# Defines a class to manage turns and store players names,whose turn it is.
class game:
    def __init__(self, name1, name2):
        self.player1 = name1
        self.player2 = name2
        self.turn = 1
#Starts with player 1's turn and switches turns after each move.
    def board(self,size) :
        self.board = np.zeros((size, size), dtype=int)
        return self.board

    def switch_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

if __name__ == "__main__":

    pg.init()
# Screen dimensions kept varible for flexibility in different screen sizes and to make it easier to scale images
    screenWidth, screenHeight = 800, 600
    screen = pg.display.set_mode((screenWidth, screenHeight))
    pg.display.set_caption("Game Zone")
# Gives the window title "Game Zone" 
    clock = pg.time.Clock()

    background = pg.image.load("Media/images/Cool.png").convert()
    background = pg.transform.scale(background, (screenWidth, screenHeight))
# Load and scale the main background image to fit the screen

    introbackground = pg.image.load("Media/images/Intro.png").convert()
    introbackground = pg.transform.scale(introbackground, (screenWidth, screenHeight))

    winbackground=pg.image.load("Media/images/Outro.png")
    winbackground = pg.transform.scale(winbackground, (screenWidth, screenHeight))

    ticTacToe = pg.image.load("Media/images/Tictactoe.png").convert_alpha()
    ticTacToe = pg.transform.scale(ticTacToe, (125, 125))
    ticTacToe_rect = ticTacToe.get_rect(topleft=(100, 300))

    othello = pg.image.load("Media/images/Othello.png").convert_alpha()
    othello = pg.transform.scale(othello, (125, 125))
    othello_rect = othello.get_rect(topleft=(350, 300))

    connect4 = pg.image.load("Media/images/C$.png").convert_alpha()
    connect4 = pg.transform.scale(connect4, (125, 125))
    connect4_rect = connect4.get_rect(topleft=(600, 300))
# Loads TicTacToe, Othello, and Connect 4 logos, scale them, and get their position rectangles

# Images,sounds and fonts are loaded and transformed to fit the screen and look good.
    heading_font= pg.font.Font(None, 150)
    heading = heading_font.render("Game Zone", False, "yellow")
    heading_rect = heading.get_rect(center=(screenWidth//2, 75))

    command_font = pg.font.Font(None, 50)
    command = command_font.render("Click on game to start", False, "white")
    command_rect = command.get_rect(center=(screenWidth//2, 200))
# Load fonts and render the heading text and command text.

    pg.mixer.pre_init(44100, -16, 2, 512)
    backgroundMusic = pg.mixer.Sound("Media/sounds/Metamorphosis_Bgm.mp3")
    Winmusic = pg.mixer.Sound("Media/sounds/applause.wav")
    intromusic=pg.mixer.Sound("Media/sounds/intro.mp3")
 
    def win_screen(winner):
        big_font1 = pg.font.Font(None, 120)
        med_font1 = pg.font.Font(None, 70)
        small_font1 = pg.font.Font(None, 40)
        Winmusic.play()
        # Button dimensions
        btn_w, btn_h = 220, 60

        back_x = screenWidth // 2 - btn_w - 20
        quit_x = screenWidth // 2 + 20
        btn_y = 420

        import random
        stars = [(random.randint(0, screenWidth),
                  random.randint(0, screenHeight),
                  random.randint(1, 3)) for _ in range(80)]

        running = True
        while running:
            clock.tick(60)
            mouse_pos = pg.mouse.get_pos()

            back_rect = pg.Rect(back_x, btn_y, btn_w, btn_h)
            quit_rect = pg.Rect(quit_x, btn_y, btn_w, btn_h)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        if back_rect.collidepoint(event.pos):
                            running = False
                            Winmusic.stop()

                        if quit_rect.collidepoint(event.pos):
                            pg.quit()
                            sys.exit()

            screen.blit(winbackground, (0, 0))

            for (sx, sy, sr) in stars:
                flicker = random.randint(-1, 1) 
                safe_radius = max(1, sr + flicker) 
                pg.draw.circle(screen, (255, 255, 200), (sx, sy), safe_radius)

            panel = pg.Surface((500, 300), pg.SRCALPHA)
            panel.fill((0, 0, 0, 160))
            screen.blit(panel, (screenWidth // 2 - 250, 100))

            name_surf = big_font1.render(winner, True, (255, 215, 0))
            name_rect = name_surf.get_rect(center=(screenWidth // 2, 200))
            screen.blit(name_surf, name_rect)

            won_surf = med_font1.render("WON!", True, (255, 80, 80))
            won_rect = won_surf.get_rect(center=(screenWidth // 2, 310))
            screen.blit(won_surf, won_rect)

            # Back button
            back_color = (200, 50, 50) if back_rect.collidepoint(mouse_pos) else (140, 20, 20)
            pg.draw.rect(screen, back_color, back_rect, border_radius=30)
            pg.draw.rect(screen, (255, 100, 100), back_rect, width=3, border_radius=30)

            back_text = small_font1.render("Back to Menu", True, (255, 255, 255))
            screen.blit(back_text, back_text.get_rect(center=back_rect.center))

            # Quit button
            quit_color = (200, 50, 50) if quit_rect.collidepoint(mouse_pos) else (140, 20, 20)
            pg.draw.rect(screen, quit_color, quit_rect, border_radius=30)
            pg.draw.rect(screen, (255, 100, 100), quit_rect, width=3, border_radius=30)

            quit_text = small_font1.render("Quit", True, (255, 255, 255))
            screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

            pg.display.update()

    def intro_screen(player1, player2):
        big = pg.font.Font(None, 100)
        med = pg.font.Font(None, 60)
        small = pg.font.Font(None, 30)
        intromusic.play()

        ko = big.render("KO", True, (255, 0, 0))
        vs = small.render("VS", True, (255, 255, 255))
        p1_text = med.render(player1, True, (255, 255, 0))
        p2_text = med.render(player2, True, (0, 200, 255))
        press = small.render("Press any key", True, (255, 255, 255))

    # Symmetric positions
        center_x = screenWidth // 2
        p1_target_x = center_x - 110
        p2_target_x = center_x + 70
        x1 = -p1_text.get_width()  # start offscreen left
        x2 = screenWidth           # start offscreen right

        running = True
        while running:
            clock.tick(60)
# clock.tick(60) limits the loop to run at 60 frames per second, ensuring that the game runs smoothly and doesn't consume excessive CPU resources.
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
# The event loop checks if the user clicks the close button, the game will quit and exit the program.
                
                if event.type == pg.KEYDOWN:
                    running = False  
                    intromusic.stop()

            #screen.fill((50, 50, 100))  

            if x1 < p1_target_x:
                x1 += 0.8
            if x2 > p2_target_x:
                x2 -= 0.8
# Draw all images and text onto the screen at their positions
            screen.blit(introbackground,(0,0))
            screen.blit(ko, (center_x - 50, 50))
            screen.blit(p1_text, (x1, 200))
            screen.blit(vs, (center_x - 20, 260))
            screen.blit(p2_text, (x2, 320))
            screen.blit(press, (center_x - 100, 450))

            pg.display.update()


    def menu():
        playedGame = False
        backgroundMusic.play(-1)
        music=False
        while playedGame == False:
            if music == False:
                backgroundMusic.play(-1)
                music=True
            clock.tick(60)
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
# When user clicks the mouse button, it checks if click was on game logos. If so, it sets playedGame to True, which starts the game.
                     if event.button == 1:
                        if ticTacToe_rect.collidepoint(event.pos):
                            # call tic tac toe 
                            resultT = subprocess.run(["python3.10", "games/tictactoe.py", player1, player2])
                            if resultT.returncode != 0:
                                winner = player1 if resultT.returncode == 1 else player2
                                loser=player2 if resultT.returncode == 1 else player2
                                playedGame = True
                                gamePlayed="TicTacToe"
                        elif othello_rect.collidepoint(event.pos):
                            # call othello
                            resultO = subprocess.run(["python3.10", "games/othello.py", player1, player2])
                            if resultO.returncode != 0:
                                winner = player1 if resultO.returncode == 1 else player2
                                loser=player2 if resultO.returncode == 1 else player2
                                playedGame = True
                                gamePlayed="Othello"
                        elif connect4_rect.collidepoint(event.pos):
                            # call connect4
                            resultC=subprocess.run(["python3.10", "games/connect4.py", player1, player2])
                            if resultC.returncode != 0 :
                                winner = player1 if resultC.returncode == 1 else player2
                                loser=player2 if resultC.returncode == 1 else player2
                                playedGame = True
                                gamePlayed="Connect4"

# Draw all images and text onto the screen at their positions
            screen.blit(background, (0, 0))
            screen.blit(heading, heading_rect)
            screen.blit(command, command_rect)
            
            # HOVER EFFECTS
            if ticTacToe_rect.collidepoint(mouse_pos):
                temp = pg.transform.scale(ticTacToe, (140, 140))
                screen.blit(temp, (ticTacToe_rect.x - 7, ticTacToe_rect.y - 7))
            else:
                screen.blit(ticTacToe, ticTacToe_rect)

            if othello_rect.collidepoint(mouse_pos):
                temp = pg.transform.scale(othello, (140, 140))
                screen.blit(temp, (othello_rect.x - 7, othello_rect.y - 7))
            else:
                screen.blit(othello, othello_rect)

            if connect4_rect.collidepoint(mouse_pos):
                temp = pg.transform.scale(connect4, (140, 140))
                screen.blit(temp, (connect4_rect.x - 7, connect4_rect.y - 7))
            else:
                screen.blit(connect4, connect4_rect)

            if playedGame:
                now = datetime.now()
                file = open("history.csv", "a")  # open file in append mode
           
                writer = csv.writer(file)        # create writer
                writer.writerow([winner,loser,now,gamePlayed])   # append details of the game
           
                file.close()  # close file 
                # appended history.csv
                # call leaderboard.sh 
                subprocess.run(["bash", "leaderboard.sh"])
                # visualise results using matplotlib
                backgroundMusic.stop()
                win_screen(winner)
                # prompt to play again
                music=False
                playedGame = False

            pg.display.update()
#Display gets updated every frame to show the latest changes on the screen.

    intro_screen(player1,player2)
    menu() 
