import queue
import sys

import pygame
import os
from Board.Board import Board
from ConstantVariables import *
import random
from Ships.Ship import Ship
from Oponent.Oponent import AIBoard


def setup_board(screen):
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

    player_fleet = []
    enemy_fleet = []

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

def is_win(fleet:list[Ship]):
    for ship in fleet:
        if ship.is_sunk == False:
            return False
    print("Wszystkie statki zatiopoine Wygrałeś")
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_board,enemy_board=setup_board(screen)

    player_ships=[]
    enemy_ships=[]

    running = True

    ai_thread = AIBoard(target_board=player_board)

    # Rozpocznij wątek (wywołuje metodę run() w tle)
    ai_thread.start()
    GAME_STATE = "PLAYER_TURN"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if GAME_STATE == "PLAYER_TURN" and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # handle_click zwraca (x, y) siatki, jeśli kliknięcie było na planszy
                grid_coords = enemy_board.handle_click(pos)

                if grid_coords:
                    x, y = grid_coords

                    # Przetwarzanie strzału! (Używamy metody dekorowanej)
                    hit, status = enemy_board.receive_shot(x, y)
                    enemy_board.update_board(x,y,screen)
                    # Zmiana tury NASTĘPUJE ZAWSZE po strzale w tej wersji Gry w Statki
                    # Niezależnie od tego, czy trafił, czy spudłował.
                    if status != "repeated":
                        pygame.display.update()
                        GAME_STATE = "AI_TURN"
                        # Wysłanie sygnału do wątku AI, aby zaczął myśleć
                        ai_thread.is_active = True  # Ustawienie flagi, by AI rozpoczęło proces_turn()
                        print("Tura AI, AI rozpoczyna myślenie...")

            if GAME_STATE == "AI_TURN":
                try:
                    # Odbiór ruchu od AI bez blokowania
                    x, y = ai_thread.move_queue.get(block=False)

                    # Przetwarzanie strzału AI (player_board.receive_shot)
                    # ...

                    # Zmiana tury i sprawdzenie warunków zwycięstwa
                    if not player_board.all_ships_sunk():
                        GAME_STATE = "PLAYER_TURN"
                    else:
                        GAME_STATE = "GAME_OVER"

                except queue.Empty:
                    pass  # AI wciąż myśli, kontynuujemy pętlę.

        pygame.display.flip()

    ai_thread.stop()
    ai_thread.join(timeout=2)  # Czekanie na zakończenie wątku AI

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
