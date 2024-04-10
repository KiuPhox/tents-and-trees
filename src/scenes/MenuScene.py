import pygame

from constants.AssetPath import FontPath, ImagePath
from constants.GameConfig import ScreenSize

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite
from engine.components.AnimationSprite import AnimationSprite

from managers.SceneManager import SceneManager
from managers.GameManager import GameManager

from engine.Button import Button

from scenes.Scene import Scene

LEVEL_COLUMNS = 10


class MenuScene(Scene):
    def __init__(self, screen):
        super().__init__("MenuScene", screen)

    def start(self):
        level_count = GameManager.get_level_count()

        self.bg = GameObject(self)
        self.bg.name = "Background"

        bg_sprite = Sprite(self.bg)
        bg_sprite.color = (245, 224, 205)
        bg_sprite.set_sprite(ImagePath.BACKGROUND)

        self.bg.add_component(bg_sprite)

        for i in range(level_count):
            button = Button(
                self,
                ImagePath.NEUTRAL,
                f"{i + 1}",
                (self.on_level_button_click, (i,), {}),
            )
            button.position = (
                (i % LEVEL_COLUMNS - LEVEL_COLUMNS / 2 + 0.5) * 80,
                (i // LEVEL_COLUMNS - level_count / LEVEL_COLUMNS / 2) * 80,
            )
            button.scale = (0.45, 0.45)
            button.label.color = (255, 255, 255)
            button.label.font = pygame.font.Font(FontPath.TT_FORS, 40)
            button.name = f"Level {i + 1}"

    def on_level_button_click(self, i: int):
        GameManager.current_level = i + 1
        SceneManager.change_scene("GameScene")
