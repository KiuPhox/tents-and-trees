import pygame

from constants.AssetPath import FontPath, ImagePath

from engine.GameObject import GameObject
from engine.components.Sprite import Sprite
from engine.Button import Button

from managers.SceneManager import SceneManager
from managers.GameManager import GameManager
from managers.TweenManager import Tween

from scenes.Scene import Scene
from utils.Color import Color

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
            self.create_level_button(i, level_count)

    def create_level_button(self, i: int, level_count: int) -> Button:
        button = Button(self, ImagePath.LEVEL_BTN, f"{i + 1}")
        button.position = (
            (i % LEVEL_COLUMNS - LEVEL_COLUMNS / 2 + 0.5) * 100,
            (i // LEVEL_COLUMNS - level_count / LEVEL_COLUMNS / 2 + 0.5) * 100,
        )
        button.scale = (0.4, 0.4)
        button.sprite.color = Color.hsl_to_rgb(
            (67, 0.52, 0.7 - i * (0.5 / level_count))
        )
        button.label.color = (255, 255, 255)
        button.label.font = pygame.font.Font(FontPath.TT_FORS, 60)
        button.name = f"Level {i + 1}"

        button.left_click_callback = (self.on_level_button_click, (i,), {})
        button.on_enter_callback = (self.on_level_button_enter, (button,), {})
        button.on_exit_callback = (self.on_level_button_exit, (button,), {})

        return button

    def on_level_button_click(self, i: int):
        GameManager.current_level = i + 1
        SceneManager.change_scene("GameScene")

    def on_level_button_enter(self, button: GameObject):
        button.scale = (0.4, 0.4)
        Tween(
            button,
            duration=0.1,
            scale=(0.45, 0.45),
        )

    def on_level_button_exit(self, button: GameObject):
        button.scale = (0.45, 0.45)
        Tween(
            button,
            duration=0.1,
            scale=(0.4, 0.4),
        )
