import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame as pg
import subprocess
from game import game 
import numpy as np

pg.init()
clock = pg.time.Clock()
screenWidth, screenHeight = 800, 600
screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE)
pg.display.set_caption("GRID")


btn_wid,btn_ht=120,60
btn_y=230
grid_x = screenWidth // 2 - btn_wid // 2
grid_rect1 = pg.Rect(grid_x, btn_y-100, btn_wid, btn_ht)
grid_rect2 = pg.Rect(grid_x, btn_y, btn_wid, btn_ht)
grid_rect3 = pg.Rect(grid_x, btn_y+100, btn_wid, btn_ht)

grid_color = (30 ,90, 160)
    
small_font1 = pg.font.SysFont("Arial", 40, bold=True)
grid_text1 = small_font1.render("6", True, (255, 245, 230))
grid_text2 = small_font1.render("8", True, (255, 245, 230))
grid_text3 = small_font1.render("10", True, (255, 245, 230))




running = True

while running:
    clock.tick(60)
    mouse_pos = pg.mouse.get_pos()
    screen.fill((15, 10, 40))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if grid_rect1.collidepoint(event.pos):
                    running=False
                    sys.exit(6)
                elif grid_rect2.collidepoint(event.pos):
                    sys.exit(8)
                    
    pg.draw.rect(screen, grid_color, grid_rect1, border_radius=30)
    pg.draw.rect(screen, (100, 200, 255), grid_rect1, width=3, border_radius=30)
    screen.blit(grid_text1, grid_text1.get_rect(center=grid_rect1.center))

    pg.draw.rect(screen, grid_color, grid_rect2, border_radius=30)
    pg.draw.rect(screen, (100, 200, 255), grid_rect2, width=3, border_radius=30)
    screen.blit(grid_text2, grid_text2.get_rect(center=grid_rect2.center))

    pg.draw.rect(screen, grid_color, grid_rect3, border_radius=30)
    pg.draw.rect(screen, (100, 200, 255), grid_rect3, width=3, border_radius=30)
    screen.blit(grid_text3, grid_text3.get_rect(center=grid_rect3.center))


    pg.display.update()


    
