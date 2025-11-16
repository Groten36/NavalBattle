import pygame

from Map.Map import Map

pygame.init()

surface=pygame.display.set_mode((1800, 900))
pygame.display.set_caption('Naval Battle')
surface.fill((211, 169, 108) )
map=Map(surface,1500,900)
map.setup()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.flip()

    