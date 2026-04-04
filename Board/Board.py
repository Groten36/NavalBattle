
import pygame
from ConstantVariables import *
import random
from Ships.Ship import *


def is_placement_valid(self, start_x, start_y, ship_length, orientation):
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

    def wrapper(self, x, y):
        if self.grid[y][x] == HIT or self.grid[y][x] == MISS:
            print(f"BŁĄD: Strzał na ({x}, {y}) jest powtórzony.")
            return False, "repeated"  # Zwracamy status błędu

        hit, status = func(self, x, y)

        result_text = "Trafiony" if hit else "Pudło"
        print(f"Strzał Gracza na ({x}, {y}) -> {result_text}")
        return hit, status

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

    def generate_possible_placements(self, ship_length):

        orientations = ['horizontal', 'vertical']

        for orientation in orientations:
            if orientation == 'horizontal':
                max_x = BOARD_SIZE - ship_length
                max_y = BOARD_SIZE
            else:  
                max_x = BOARD_SIZE
                max_y = BOARD_SIZE - ship_length

            for start_y in range(max_y):
                for start_x in range(max_x):
                    if self.is_placement_valid(start_x, start_y, ship_length, orientation):
                        yield start_x, start_y, orientation

    def handle_click(self, pos):
        click_x, click_y = pos

        board_end_x = self.x_offset + BOARD_SIZE * TILE_SIZE
        board_end_y = self.y_offset + BOARD_SIZE * TILE_SIZE

        if (self.x_offset <= click_x < board_end_x and
                self.y_offset <= click_y < board_end_y):

            col = (click_x - self.x_offset) // TILE_SIZE
            row = (click_y - self.y_offset) // TILE_SIZE

            if not self.is_player_board:
                print(f"Strzał na: ({col}, {row})")

            return (col, row)
        return None

    def is_placement_valid(self, start_x, start_y, ship_length, orientation):
        for x in range(ship_length):
            if orientation == 'horizontal':

                if (start_x >= BOARD_SIZE or start_x < 0 or start_y >= BOARD_SIZE or start_y < 0 or \
                        self.grid[start_x + x][
                            start_y] != WATER):
                    return False
            else:

                if start_x >= BOARD_SIZE or start_x < 0 or start_y >= BOARD_SIZE or start_y < 0 or self.grid[start_x][
                    start_y + x] != WATER:
                    return False

        return True

    def set_grid(self,ship):
        for c in ship.coordinates:
            self.grid[c[0]][c[1]] = SHIP



    def place_ships_randomly(self):
        ship_length = 3

        for i in range(1, NUMBER_OF_SHIPS):
            possible_placements = list(self.generate_possible_placements(ship_length))

            if not possible_placements:
                print(f"BŁĄD: Nie znaleziono miejsca dla statku o długości {ship_length}.")
                break

            start_x, start_y, orientation = random.choice(possible_placements)

            ship = Ship(i, ship_length, orientation, [start_x, start_y])
            ship.set_position(start_x, start_y, orientation)
            self.set_grid(ship)
            self.fleet.append(ship)

    @log_shot
    def receive_shot(self, x: int, y: int) -> tuple[bool, str]:
        if self.grid[x][y] == SHIP:
            self.grid[x][y] = HIT

            for ship in self.fleet:
                if (x, y) in ship.coordinates:
                    print("nawet w ifa nie wlazi")
                    is_sunk = ship.is_hit(x, y)
                    if is_sunk:
                        return True, "sunk"

            return True, "hit"

        else:
            self.grid[y][x] = MISS
            return False, "miss"

    def update_board(self,x,y,screen):

        screen_x = self.x_offset + x * TILE_SIZE
        screen_y = self.y_offset + y * TILE_SIZE
        tile_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)

        if self.grid[x][y] == MISS:
            pygame.draw.circle(
                screen,
                WHITE,
                tile_rect.center,
                TILE_SIZE // 8
            )

        elif self.grid[x][y] == HIT:

            padding = TILE_SIZE // 4
            start_pos = (screen_x + padding, screen_y + padding)
            end_pos = (screen_x + TILE_SIZE - padding, screen_y + TILE_SIZE - padding)

            pygame.draw.line(
                screen,
                RED,
                start_pos,
                end_pos,
                width=3
            )

            pygame.draw.line(
                screen,
                RED,
                (screen_x + padding, screen_y + TILE_SIZE - padding),
                (screen_x + TILE_SIZE - padding, screen_y + padding),
                width=3
            )
        pygame.display.flip()

    def all_ships_sunk(self) -> bool:
        if not self.fleet:
            return False


        return all(ship.is_sunk for ship in self.fleet)