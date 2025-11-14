import pygame


pygame.init()

window = pygame.display.set_mode((400, 500),pygame.RESIZABLE)
pygame.display.set_caption('Naval Battle')

color = "blue"
running = True

while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(color)
    pygame.display.flip()

    