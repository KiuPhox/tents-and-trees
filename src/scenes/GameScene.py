import pygame

from constants.GameConfig import ScreenSize
from constants.AssetPath import FontPath, ImagePath

from managers.SceneManager import SceneManager
from managers.GameManager import GameManager

from objects.Grid import Grid
from objects.Text import Text
from objects.button.Button import Button

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.image.load(ImagePath.BACKGROUND)
        self.bg.fill(
            (245, 224, 205),
            special_flags=pygame.BLEND_RGB_MULT,
        )

        self.level_title = Text(
            f"Level {GameManager.current_level}",
            pygame.font.Font(FontPath.TT_FORS, 40),
            (ScreenSize.WIDTH / 2, 50),
        )

        self.level_title.color = (127, 79, 65)

        self.grid = Grid()

    def enter(self):
        self.level_title.text = f"Level {GameManager.current_level}"

        self.grid.create()

    def update(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))

        self.level_title.update(self.screen)

        self.grid.update(self.screen)