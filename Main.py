import queue
import sys

import pygame
import os
from Board.Board import Board
from ConstantVariables import *
import random
from Ships.Ship import Ship
from Oponent.Oponent import Oponent


def setup_board(screen):
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

    player_board.place_ships_randomly()
    enemy_board.place_ships_randomly()
    player_board.draw(screen)
    enemy_board.draw(screen)
    pygame.display.update()
    return player_board, enemy_board


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_board,enemy_board=setup_board(screen)


    running = True

    GAME_STATE = "PLAYER_TURN"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if GAME_STATE == "PLAYER_TURN" and event.type == pygame.MOUSEBUTTONDOWN:
                print("TURA GRACZA")
                pos = pygame.mouse.get_pos()


                grid_coords = enemy_board.handle_click(pos)

                if grid_coords:
                    x, y = grid_coords


                    hit, status = enemy_board.receive_shot(x, y)
                    enemy_board.update_board(x,y,screen)

                    if status != "repeated":
                        pygame.display.update()
                        GAME_STATE = "AI_TURN"

                        print("TURA AI")

                    if not enemy_board.all_ships_sunk():
                        GAME_STATE = "AI_TURN"
                    else:
                        GAME_STATE = "GAME_OVER"


            if GAME_STATE == "AI_TURN":
                try:


                    hit, status = player_board.receive_shot(x, y)
                    player_board.update_board(x,y,screen)


                    if not player_board.all_ships_sunk():
                        GAME_STATE = "PLAYER_TURN"
                    else:
                        GAME_STATE = "GAME_OVER"

                except queue.Empty:
                    pass

        if GAME_STATE == "GAME_OVER":
            print("GAME OVER")

        pygame.display.flip()



    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
