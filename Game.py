import pygame

from Map.Map import Map
from Ships.Ship import Ship

pygame.init()

def setup():
    surface=pygame.display.set_mode((1800, 900))
    pygame.display.set_caption('Naval Battle')
    surface.fill((211, 169, 108) )
    map=Map(surface,1500,900)
    map.setup()
    player_ship=Ship(10,20,[1,2,4],50,100,850)
    pygame.draw.rect(surface,'grey',[player_ship.x_coordinate,player_ship.y_coordinate,100,player_ship.length])
    oponent_ship = Ship(10, 20, [1, 2, 4], 50, 1350, 50)
    pygame.draw.rect(surface, 'black', [oponent_ship.x_coordinate, oponent_ship.y_coordinate, 100, oponent_ship.length])

setup()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.flip()

    