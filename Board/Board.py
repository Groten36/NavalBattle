
import pygame
import os
from ConstantVariables import *

class Board:
    def __init__(self, x_offset, y_offset, is_player_board=False):
        self.grid = [[WATER for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.is_player_board = is_player_board

        # Przykładowe rozmieszczenie statku (powinno być zaimplementowane przez gracza)
        if self.is_player_board:
            self.grid[2][2] = SHIP
            self.grid[2][3] = SHIP
            self.grid[2][4] = SHIP
        else:
            # Symulacja strzałów na planszy przeciwnika
            self.grid[0][0] = MISS
            self.grid[5][5] = HIT

    def draw(self, screen):
        """Rysuje planszę na ekranie Pygame."""
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                state = self.grid[y][x]

                screen_x = self.x_offset + x * TILE_SIZE
                screen_y = self.y_offset + y * TILE_SIZE
                tile_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)


                pygame.draw.rect(screen, BLUE_DARK, tile_rect, 1)


                if self.is_player_board and state == SHIP:
                    pygame.draw.rect(screen, GREY, tile_rect)


                if state == HIT:
                    pygame.draw.circle(screen, RED, tile_rect.center, TILE_SIZE // 4)
                elif state == MISS:
                    pygame.draw.circle(screen, WHITE, tile_rect.center, TILE_SIZE // 8)

    def handle_click(self, pos):
        """Obsługa kliknięcia myszą."""
        click_x, click_y = pos

        # Sprawdzenie, czy kliknięcie było w obrębie planszy
        board_end_x = self.x_offset + BOARD_SIZE * TILE_SIZE
        board_end_y = self.y_offset + BOARD_SIZE * TILE_SIZE

        if (self.x_offset <= click_x < board_end_x and
                self.y_offset <= click_y < board_end_y):

            # Konwersja pikseli na współrzędne siatki
            col = (click_x - self.x_offset) // TILE_SIZE
            row = (click_y - self.y_offset) // TILE_SIZE

            # Przykładowa akcja dla strzału (na planszy przeciwnika)
            if not self.is_player_board:
                print(f"Strzał na: ({col}, {row})")
                # Tutaj byłaby logika sprawdzająca czy trafiony/spudłowany

            return (col, row)
        return None


    def add_ship(self, ship):
        if shi
        self.grid[2][2] = SHIP
        self.grid[2][3] = SHIP
        self.grid[2][4] = SHIP

