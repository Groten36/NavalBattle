import pygame
import os
from Board.Board import Board
from ConstantVariables import *


def setup_board():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Naval Battle")

    try:
        water_bg = pygame.image.load('Board/water.png').convert()
        water_bg = pygame.transform.scale(water_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        water_bg = None

    player_board = Board(
        x_offset=BOARD_OFFSET,
        y_offset=BOARD_OFFSET,
        is_player_board=True
    )

    enemy_board = Board(
        x_offset=SCREEN_WIDTH - BOARD_OFFSET - BOARD_SIZE * TILE_SIZE,
        y_offset=BOARD_OFFSET,
        is_player_board=False
    )

    if water_bg:
        screen.blit(water_bg, (0, 0))
    else:
        screen.fill(BLUE_DARK)

    player_board.draw(screen)
    enemy_board.draw(screen)

    return player_board, enemy_board


def main():
    pygame.init()

    player_board,enemy_board=setup_board()

    player_ships=[]
    enemy_ships=[]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if SETUP:
                for i in range(NUMBER_OF_SHIPS):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pass
            else:
                pass
                '''
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
    
                    clicked_coords = enemy_board.handle_click(pos)
                    if clicked_coords:
                        pass
                '''

    pygame.display.flip()

if __name__ == '__main__':
    main()
