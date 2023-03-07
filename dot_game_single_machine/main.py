import pygame
from cell import Cell
from random import *
import time


pygame.init()
display_width = 600
display_height = 600
count_score_height = 100
cell = 50


gameDisplay = pygame.display.set_mode((display_width,display_height+count_score_height))
pygame.display.set_caption('Game Maybe...')

clock = pygame.time.Clock()

def message_display(text,x,y):
    largetext = pygame.font.Font('freesansbold.ttf',25)
    TextSurf = largetext.render(text, True, (255,255,255))
    TextRect = TextSurf.get_rect()
    TextRect = (x,y)
    gameDisplay.blit(TextSurf,TextRect)



cells = []

for i in range (cell//2, display_height-cell//2, cell):
    cells.append([]) 
    for j in range(cell//2, display_width-cell//2, cell):
        isBorder = False
        if(j == cell//2 or i == cell//2):
            isBorder = True
        new_cell = Cell(j, i, cell, isBorder)
        cells[-1].append(new_cell)



def drawGrid(gameDisplay, color):
    for i in range (cell//2, display_height, cell):
        for j in range(cell//2, display_width, cell):
            pygame.draw.circle(gameDisplay, (255, 255, 255), (j, i), 5)

def countScore():
    score = [0, 0]

    for cell_row in cells:
        for cell in cell_row:
            if cell.player is not None:
                score[cell.player] +=1 
    return score


def gameLoop():
    curr_player = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = pygame.mouse.get_pos()
                already_changed = 0
                curr_curr_player = curr_player
                for cell_row in cells:
                    for cell in cell_row:
                        curr_player, already_changed = cell.update(mouse, curr_player, already_changed, curr_curr_player)
                        # curr_curr_player = curr_player

            

        gameDisplay.fill((0,0,0))
        drawGrid(gameDisplay, (255, 255, 255))
        for cell_row in cells:
            for cell in cell_row:
                cell.draw(gameDisplay)
        
        message_display(f"Score: {countScore()}", 50, display_height+50)
        message_display(f"{curr_player}", 300, display_height+50)
        pygame.display.update()
        clock.tick(30)

gameLoop()
pygame.quit()
