import pygame


class Text:
    def __init__(self, text: str, font: pygame.font.Font, position: tuple):
        self.surface = font.render(text, False, (0, 0, 0))
        self.font = font
        self.text = text
        self.position = (
            position[0] - self.surface.get_size()[0] / 2,
            position[1] - self.surface.get_size()[1] / 2,
        )

    def update(self, screen: pygame.Surface):
        self.surface = self.font.render(self.text, False, (0, 0, 0))
        screen.blit(self.surface, self.position)
