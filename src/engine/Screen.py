import pygame

from managers.InputManager import InputManager
from managers.SpriteManager import SpriteManager
from managers.UIManager import UIManager


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

    def render(self):
        self.handle_input()
        self.render_sprites()
        self.render_texts()

    def handle_input(self):
        mouse_position = InputManager.get_mouse_position()

        mouse_position = (
            mouse_position[0] - self.width / 2,
            mouse_position[1] - self.height / 2,
        )

        if InputManager.get_mouse_down(0):
            for button in UIManager.buttons:
                if button.sprite is None:
                    return

                if (
                    mouse_position[0] >= button.position[0] - button.sprite.width() / 2
                    and mouse_position[0]
                    <= button.position[0] + button.sprite.width() / 2
                    and mouse_position[1]
                    >= button.position[1] - button.sprite.height() / 2
                    and mouse_position[1]
                    <= button.position[1] + button.sprite.height() / 2
                ):
                    button.on_left_click()

        if InputManager.get_mouse_down(2):
            for button in UIManager.buttons:
                if button.sprite is None:
                    return

                if (
                    mouse_position[0] >= button.position[0] - button.sprite.width() / 2
                    and mouse_position[0]
                    <= button.position[0] + button.sprite.width() / 2
                    and mouse_position[1]
                    >= button.position[1] - button.sprite.height() / 2
                    and mouse_position[1]
                    <= button.position[1] + button.sprite.height() / 2
                ):
                    button.on_right_click()

        pass

    def render_sprites(self):
        for sprite in SpriteManager.sprites:
            game_object = sprite.game_object

            if not game_object.active:
                continue

            size = (sprite.width(), sprite.height())

            scaled_image = pygame.transform.scale(sprite.image, size)
            scaled_image.fill(sprite.color, special_flags=pygame.BLEND_RGB_MULT)

            position = (
                game_object.position[0] - sprite.width() / 2 + self.width / 2,
                game_object.position[1] - sprite.height() / 2 + self.height / 2,
            )

            self.screen.blit(scaled_image, position)

    def render_texts(self):
        for text in UIManager.texts:
            game_object = text.game_object

            if not game_object.active:
                continue

            text.surface = text.font.render(text.text, True, text.color)
            size = text.surface.get_size()

            scaled_text = pygame.transform.scale(text.surface, size)

            position = (
                game_object.position[0] - size[0] / 2 + self.width / 2,
                game_object.position[1] - size[1] / 2 + self.height / 2,
            )

            self.screen.blit(scaled_text, position)
