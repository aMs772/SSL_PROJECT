#!/usr/local/bin/python3.10
import sys
import csv
import os
import numpy as np
import subprocess
import pygame as pg
from datetime import datetime
import matplotlib.pyplot as plt

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

    sortbackground=pg.image.load("Media/images/B.png")
    sortbackground = pg.transform.scale(sortbackground, (screenWidth, screenHeight))

    ticTacToe = pg.image.load("Media/images/Tictactoe.png").convert_alpha()
    ticTacToe = pg.transform.scale(ticTacToe, (125, 125))
    ticTacToe_rect = ticTacToe.get_rect(topleft=(100, 300))

    othello = pg.image.load("Media/images/Othello.png").convert_alpha()
    othello = pg.transform.scale(othello, (125, 125))
    othello_rect = othello.get_rect(topleft=(350, 300))

    connect4 = pg.image.load("Media/images/C$.png").convert_alpha()
    connect4 = pg.transform.scale(connect4, (125, 125))
    connect4_rect = connect4.get_rect(topleft=(600, 300))

    popit = pg.image.load("Media/images/Popit.png").convert_alpha()
    popit = pg.transform.scale(popit, (125, 125))
    popit_rect = popit.get_rect(topleft=(350, 450))
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

    def sort_screen():
        #button dimensions of each W,l,w/l
        #dimesions of box
        #add sort leader board by 
        title_font = pg.font.SysFont("Georgia", 52, bold=True)
        title_text = title_font.render("Sort Leaderboard By", True, (180, 255, 255))

        title_rect = title_text.get_rect(center=(screenWidth // 2, 250))
        btn_wid,btn_ht=230,90
        btn_y=369

        W_x = screenWidth // 2 - 1.5*btn_wid - 20
        L_x = screenWidth // 2 - 0.5*btn_wid
        W_L_x=screenWidth // 2 + 0.5*btn_wid +20

        W_rect = pg.Rect(W_x, btn_y, btn_wid, btn_ht)
        L_rect=  pg.Rect(L_x, btn_y, btn_wid, btn_ht)
        W_L_rect=  pg.Rect(W_L_x, btn_y, btn_wid, btn_ht)

        running=True
        while running:
            clock.tick(60)
            mouse_pos=pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        if W_rect.collidepoint(event.pos):
                            running = False
                            sort_option="W"

                        if L_rect.collidepoint(event.pos):
                            running=False
                            sort_option="L"

                        if W_L_rect.collidepoint(event.pos):
                            running=False
                            sort_option="W/L"
            screen.blit(sortbackground,(0,0))

            W_color = (30 ,90, 160) if W_rect.collidepoint(mouse_pos) else (20 ,60, 120)
            pg.draw.rect(screen, W_color, W_rect, border_radius=30)
            pg.draw.rect(screen, (100, 200, 255), W_rect, width=3, border_radius=30)

            small_font1 = pg.font.SysFont("Arial", 40, bold=True)
            W_text = small_font1.render("Wins", True, (255, 245, 230))
            screen.blit(W_text, W_text.get_rect(center=W_rect.center))

            L_color = (30 ,90, 160) if L_rect.collidepoint(mouse_pos) else (20 ,60, 120)
            pg.draw.rect(screen, L_color, L_rect, border_radius=30)
            pg.draw.rect(screen, (100, 200, 255), L_rect, width=3, border_radius=30)

            small_font1 = pg.font.SysFont("Arial", 40, bold=True)
            L_text = small_font1.render("Loses", True, (255, 245, 230))
            screen.blit(L_text, L_text.get_rect(center=L_rect.center))

            W_L_color = (30 ,90, 160) if W_L_rect.collidepoint(mouse_pos) else (20 ,60, 120)
            pg.draw.rect(screen, W_L_color, W_L_rect, border_radius=30)
            pg.draw.rect(screen, (100, 200, 255), W_L_rect, width=3, border_radius=30)

            small_font1 = pg.font.SysFont("Arial", 40, bold=True)
            W_L_text = small_font1.render("Wins/Loses", True, (255, 245, 230))
            screen.blit(W_L_text, W_L_text.get_rect(center=W_L_rect.center))

            shadow_text = title_font.render("Sort Leaderboard By", True, (0, 80, 120))
            shadow_rect = shadow_text.get_rect(center=(screenWidth // 2 + 3, 253))
            screen.blit(shadow_text, shadow_rect)

            screen.blit(title_text,title_rect)

            pg.display.update()

        return sort_option
    
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
                        elif popit_rect.collidepoint(event.pos):
                            # call popit
                            resultp=subprocess.run(["python3.10", "games/pop_it.py", player1, player2])
                            if resultp.returncode != 0 :
                                winner = player1 if resultp.returncode == 1 else player2
                                loser=player2 if resultp.returncode == 1 else player1
                                playedGame = True
                                gamePlayed="PopIt"

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
                sort_option=sort_screen()
                subprocess.run(["bash", "leaderboard.sh",sort_option])
                # visualise results using matplotlib
                wins = {}
                losses = {}
                ratios = {}
                game_freq = {}

                with open("data.txt") as f:
                    for line in f:
                        game, user, w, l, r = line.strip().split(",")

                        w=int(w)
                        l=int(l)
                        r=float(r)
                        wins[user] = wins.get(user, 0) + w
                        losses[user] = losses.get(user, 0) + l
                        game_freq[game] = game_freq.get(game, 0) + 1
                        
                ratios = {u: wins[u] / losses[u] if losses[u] != 0 else wins[u] for u in wins}
                top = sorted(wins, key=wins.get, reverse=True)[:5]
                top_wins = [wins[x] for x in top]
                top_r = sorted(ratios ,key=ratios.get, reverse=True)[:5]
                top_ratio=[ratios[x] for x in top_r]

                plt.figure(figsize=(5,4))
                plt.bar(top, top_wins)
                plt.title("Top Wins")
                plt.tight_layout()
                plt.savefig("bar.png")
                plt.close()

                plt.figure(figsize=(5,4))
                plt.bar(top_r, top_ratio)
                plt.title("Win/Loss Ratio")
                plt.tight_layout()
                plt.savefig("wl.png")
                plt.close()

                plt.figure(figsize=(5,4))
                plt.pie(game_freq.values(), labels=game_freq.keys(), autopct="%1.1f%%")
                plt.title("Game Frequency")
                plt.tight_layout()
                plt.savefig("pie.png")
                plt.close()
                bar = pg.image.load("bar.png")
                wl  = pg.image.load("wl.png")
                pie = pg.image.load("pie.png")

                bar = pg.transform.smoothscale(bar, (380, 260))
                wl  = pg.transform.smoothscale(wl,  (380, 260))
                pie = pg.transform.smoothscale(pie, (380, 260))
                show = True

                while show:
                    for e in pg.event.get():
                        if e.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if e.type == pg.KEYDOWN:
                            show = False

                    screen.fill((20, 20, 20))
                    screen.blit(bar, (20, 20))
                    screen.blit(wl,  (400, 20))
                    screen.blit(pie, (210, 310))

                    pg.display.update()
                    
                backgroundMusic.stop()
                win_screen(winner)
                # prompt to play again
                music=False
                playedGame = False

            pg.display.update()
#Display gets updated every frame to show the latest changes on the screen.

    intro_screen(player1,player2)
    menu() 
