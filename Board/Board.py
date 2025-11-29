
import pygame
import os
from ConstantVariables import *
import random
from Ships.Ship import *


def is_placement_valid(self, start_x, start_y, ship_length, orientation):
    # jak skńczysz wątki te sprzątnij maszkarony w ifach
    for x in range(ship_length):
        if orientation == 'horizontal':

            if (start_x >= BOARD_SIZE or start_x < 0 or start_y >= BOARD_SIZE or start_y < 0 or \
                self.grid[start_x + x][
                    start_y] != WATER) or (start_x+1>=BOARD_SIZE or self.grid[start_x + 1][
                start_y] == SHIP) or (start_y+1>=BOARD_SIZE or self.grid[start_x][start_y + 1] == SHIP) or (start_x-1<0 or self.grid[start_x - 1][
                start_y] == SHIP) or (start_y-1<=0 or self.grid[start_x][start_y - 1] == SHIP):
                return False
        else:

            if start_x >= BOARD_SIZE or start_x < 0 or start_y >= BOARD_SIZE or start_y < 0 or self.grid[start_x][
                start_y + x] != WATER  or (start_x+1>=BOARD_SIZE or self.grid[start_x + 1][
                start_y] == SHIP) or (start_y+1>=BOARD_SIZE or self.grid[start_x][start_y + 1] == SHIP) or (start_x-1<0 or self.grid[start_x - 1][
                start_y] == SHIP) or (start_y-1<=0 or self.grid[start_x][start_y - 1] == SHIP):
                return False

    return True


def log_shot(func):
    """Dekorator logujący współrzędne strzału."""

    def wrapper(self, x, y):
        # Sprawdzenie czy strzał jest legalny (np. czy pole nie było już ostrzelane)
        if self.grid[y][x] == HIT or self.grid[y][x] == MISS:
            print(f"BŁĄD: Strzał na ({x}, {y}) jest powtórzony.")
            return False, "repeated"  # Zwracamy status błędu

        hit, status = func(self, x, y)

        # Logowanie po wykonaniu oryginalnej funkcji
        result_text = "Trafiony" if hit else "Pudło"
        print(f"Strzał Gracza na ({x}, {y}) -> {result_text}")
        return hit, status  # Zwracamy wynik strzału i status (np. 'hit', 'miss', 'sunk')

    return wrapper



class Board:
    def __init__(self, x_offset, y_offset, is_player_board=False):
        self.grid = [[WATER for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.is_player_board = is_player_board
        self.fleet=[]


    def draw(self, screen):

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

    def is_placement_valid(self, start_x, start_y, ship_length, orientation):
        #jak skńczysz wątki te maszkarony w ifach
        for x in range(ship_length):
            if orientation == 'horizontal':

                if (start_x >= BOARD_SIZE or start_x < 0 or start_y >= BOARD_SIZE or start_y < 0 or \
                        self.grid[start_x + x][
                            start_y] != WATER) or self.grid[start_x + 1][start_y] == SHIP or self.grid[start_x][start_y+1] == SHIP or self.grid[start_x - 1][start_y] == SHIP or self.grid[start_x][start_y-1] == SHIP:
                    return False
            else:

                if start_x >= BOARD_SIZE or start_x < 0 or start_y >= BOARD_SIZE or start_y < 0 or self.grid[start_x][
                    start_y + x] != WATER or self.grid[start_x][start_y]==SHIP or self.grid[start_x + 1][start_y] == SHIP or self.grid[start_x][start_y+1] == SHIP or self.grid[start_x - 1][start_y] == SHIP or self.grid[start_x][start_y-1] == SHIP:
                    return False

        return True

    def set_grid(self,ship):
        for c in ship.coordinates:
            self.grid[c[0]][c[1]] = SHIP



    def place_ships_randomly(self):
        ship_length=3
        for i in range(1,NUMBER_OF_SHIPS):
            placed = False
            while not placed:

                # A. Losowy Wybór Orientacji
                orientation = random.choice(['horizontal', 'vertical'])


                if orientation == 'horizontal':
                    max_x = BOARD_SIZE - ship_length
                    max_y = BOARD_SIZE - 1
                else:  # 'vertical'
                    max_x = BOARD_SIZE - 1
                    max_y = BOARD_SIZE - ship_length

                start_x = random.randint(0, max_x)
                start_y = random.randint(0, max_y)

                if is_placement_valid(self,start_x, start_y, ship_length, orientation):
                    ship=Ship(i,ship_length,orientation,[start_x,start_y])
                    ship.set_position(start_x, start_y,orientation)
                    self.set_grid(ship)
                    self.fleet.append(ship)

                    placed = True

    @log_shot
    def receive_shot(self, x: int, y: int) -> tuple[bool, str]:
        """
        Przetwarza strzał na planszy.
        :return: (czy trafiono, status strzału)
        """
        # Sprawdzenie, czy jest statek w tym miejscu
        if self.grid[x][y] == SHIP:
            self.grid[x][y] = HIT  # Zmiana stanu na TRAFIONY

            # Wyszukanie, który statek został trafiony
            for ship in self.fleet:
                if (x, y) in ship.coordinates:
                    print("nawet w ifa nie wlazi")
                    is_sunk = ship.is_hit(x, y)
                    if is_sunk:
                        return True, "sunk"  # Zwracamy True i status "zatopiony"

            return True, "hit"  # Trafiony, ale nie zatopiony

        else:
            self.grid[y][x] = MISS  # Zmiana stanu na PUDŁO
            return False, "miss"

    def update_board(self,x,y,screen):

        screen_x = self.x_offset + x * TILE_SIZE
        screen_y = self.y_offset + y * TILE_SIZE
        tile_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)

        if self.grid[x][y] == MISS:
            # Rysowanie białego kółka (PUDŁO)
            # Używamy tile_rect.center do precyzyjnego umieszczenia
            pygame.draw.circle(
                screen,
                WHITE,
                tile_rect.center,
                TILE_SIZE // 8  # Mały promień
            )

        elif self.grid[x][y] == HIT:
            # Rysowanie czerwonego krzyżyka (TRAFIENIE)

            # Wymiary krzyżyka
            padding = TILE_SIZE // 4
            start_pos = (screen_x + padding, screen_y + padding)
            end_pos = (screen_x + TILE_SIZE - padding, screen_y + TILE_SIZE - padding)

            # Rysowanie pierwszej linii (przekątna)
            pygame.draw.line(
                screen,
                RED,
                start_pos,
                end_pos,
                width=3
            )

            # Rysowanie drugiej linii (przeciwprzekątna)
            pygame.draw.line(
                screen,
                RED,
                (screen_x + padding, screen_y + TILE_SIZE - padding),
                (screen_x + TILE_SIZE - padding, screen_y + padding),
                width=3
            )
        pygame.display.flip()

