import pygame

class Map:
    def __init__(self,surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.color = (0, 255, 255)

    def setup(self):
        image=pygame.transform.scale(pygame.image.load('Map/water.png'), (self.width, self.height))
        self.surface.blit(image, (0, 0))

