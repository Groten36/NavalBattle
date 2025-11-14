import pygame

class Map:
    def __init__(self,surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.color = (0, 255, 255)

    def setup(self):
        pygame.draw.rect(self.surface, self.color,
                         pygame.Rect(0, 0, self.width, self.height))

        image = pygame.image.load('Map/cartoon_water.png')
        image=pygame.transform.scale(image, (self.width, self.height))
        self.surface.blit(image, (0, 0))

