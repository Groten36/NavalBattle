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
