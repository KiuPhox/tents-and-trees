import pygame


class Text:
    def __init__(self, text: str, font: pygame.font.Font, position: tuple[float, float]):
        self.color = (0, 0, 0)
        
        self.font = font if font is not None else pygame.font.Font(None, 32)
        self.surface = self.font.render(text, True, self.color)

        self.text = text
        self.position = (
            position[0] - self.surface.get_size()[0] / 2,
            position[1] - self.surface.get_size()[1] / 2,
        )
        self.text_rect = self.surface.get_rect(center=position)


    def update(self, screen: pygame.Surface):
        self.surface = self.font.render(self.text, True, self.color)
        
        screen.blit(self.surface, self.position)
