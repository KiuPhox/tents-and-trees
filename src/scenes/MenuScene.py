import pygame

from constants.AssetPath import FontPath, ImagePath
from constants.GameConfig import ScreenSize

from managers.SceneManager import SceneManager
from managers.GameManager import GameManager

from objects.button.Button import Button

LEVEL_COLUMNS = 10


class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.image.load(ImagePath.BACKGROUND)
        self.bg.fill(
            (245, 224, 205),
            special_flags=pygame.BLEND_RGB_MULT,
        )

        self.level_buttons = []

        level_count = GameManager.get_level_count()

        for i in range(level_count):
            button = Button(
                None,
                (
                    ScreenSize.WIDTH / 2 + (i % LEVEL_COLUMNS - LEVEL_COLUMNS / 2) * 60,
                    ScreenSize.HEIGHT / 2
                    + (i // LEVEL_COLUMNS - level_count / LEVEL_COLUMNS / 2) * 60,
                ),
                f"{i + 1}",
                pygame.font.Font(FontPath.TT_FORS, 40),
                (self.on_level_button_click, (i,), {}),
            )

            button.text.color = (127, 79, 65)

            self.level_buttons.append(button)

    def enter(self):
        pass

    def update(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))

        for button in self.level_buttons:
            button.update(self.screen)

    def on_level_button_click(self, i: int):
        GameManager.current_level = i + 1
        SceneManager.change_scene("GameScene")
