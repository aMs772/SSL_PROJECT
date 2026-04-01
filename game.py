import sys
import pygame as pg

player1 = sys.argv[1]
player2 = sys.argv[2]

class game:
    def __init__(self, name1, name2):
        self.player1 = name1
        self.player2 = name2
        self.turn = 1

    def switch_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1


pg.init()

screenWidth, screenHeight = 800, 600
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Game Zone")

clock = pg.time.Clock()

background = pg.image.load("images/pic2.jpg").convert()
background = pg.transform.scale(background, (screenWidth, screenHeight))

ticTacToe = pg.image.load("images/gameLogos/ticTacToe.png").convert_alpha()
ticTacToe = pg.transform.scale(ticTacToe, (125, 125))
ticTacToe_rect = ticTacToe.get_rect(topleft=(100, 300))

othello = pg.image.load("images/gameLogos/othello.png").convert_alpha()
othello = pg.transform.scale(othello, (125, 125))
othello_rect = othello.get_rect(topleft=(350, 300))

connect4 = pg.image.load("images/gameLogos/connect4.png").convert_alpha()
connect4 = pg.transform.scale(connect4, (125, 125))
connect4_rect = connect4.get_rect(topleft=(600, 300))

heading_font= pg.font.Font(None, 150)
heading = heading_font.render("Game Zone", False, "yellow")
heading_rect = heading.get_rect(center=(screenWidth//2, 75))

command_font = pg.font.Font(None, 50)
command = command_font.render("Click on game to start", False, "black")
command_rect = command.get_rect(center=(screenWidth//2, 200))

pg.mixer.pre_init(44100, -16, 2, 512)
backgroundMusic = pg.mixer.Sound("sound/beats.mp3")
#backgroundMusic.set_volume(0.5)


def intro_screen(player1, player2):
    big = pg.font.Font(None, 100)
    med = pg.font.Font(None, 60)
    small = pg.font.Font(None, 30)

    ko = big.render("KO", True, (255, 0, 0))
    vs = small.render("VS", True, (255, 255, 255))
    p1_text = med.render(player1, True, (255, 255, 0))
    p2_text = med.render(player2, True, (0, 200, 255))
    press = small.render("Press any key", True, (255, 255, 255))

    # Symmetric positions
    center_x = screenWidth // 2
    p1_target_x = center_x - 150
    p2_target_x = center_x + 50
    x1 = -p1_text.get_width()  # start offscreen left
    x2 = screenWidth           # start offscreen right

    running = True
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                running = False  

        screen.fill((50, 50, 100))  

        if x1 < p1_target_x:
            x1 += 5
        if x2 > p2_target_x:
            x2 -= 5

        screen.blit(ko, (center_x - 50, 50))
        screen.blit(p1_text, (x1, 200))
        screen.blit(vs, (center_x - 20, 260))
        screen.blit(p2_text, (x2, 320))
        screen.blit(press, (center_x - 100, 450))

        pg.display.update()
def menu():
    playedGame = False
    while playedGame == False:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        backgroundMusic.play()

        screen.blit(background, (0, 0))
        screen.blit(heading, heading_rect)
        screen.blit(command, command_rect)
        screen.blit(ticTacToe, ticTacToe_rect)
        screen.blit(othello, othello_rect)
        screen.blit(connect4, connect4_rect)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ticTacToe_rect.collidepoint(event.pos):
                    # call tic tac toe 
                    playedGame = True
                    pass
                elif othello_rect.collidepoint(event.pos):
                    # call othello
                    playedGame = True
                    pass
                elif connect4_rect.collidepoint(event.pos):
                    # call connect4
                    playedGame = True
                    pass
    
        if playedGame:
            # append history.csv
            # call leaderboard.sh
            # visualise results using matplotlib
            # prompt to play again
            pass

        pg.display.update()

intro_screen(player1,player2)
menu()
