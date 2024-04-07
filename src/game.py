import pygame
from sys import exit

from utils.Time import Time

from constants.GameConfig import ScreenSize
from constants.AssetPath import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tents and Trees")

        self.screen = pygame.display.set_mode((ScreenSize.WIDTH, ScreenSize.HEIGHT))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FontPath.TT_FORS, 32)

        self.bg = pygame.image.load(ImagePath.BACKGROUND)
        self.bg.fill(
            (245, 224, 205),
            special_flags=pygame.BLEND_RGB_MULT,
        )

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.bg, (0, 0))

        pygame.display.update()

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.draw()

            Time.deltaTime = self.clock.tick(60) / 1000
            Time.time = pygame.time.get_ticks() / 1000


game = Game()
game.update()
