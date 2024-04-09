import pygame

from objects.Text import Text

from managers.InputManager import InputManager
from managers.SceneManager import SceneManager
from objects.sprite.Sprite import Sprite


class Button:
    def __init__(
        self,
        image: pygame.Surface,
        position: tuple[float, float],
        string: str = "",
        font: pygame.font.Font = None,
        left_click_callback=None,
        right_click_callback=None,
    ) -> None:
        self.position = position
        self.text = Text(string, font, position)

        self.sprite = Sprite(image, position) if image is not None else None

        self.text_rect = self.text.text_rect

        self.left_click_callback = left_click_callback
        self.right_click_callback = right_click_callback

        self.active = True

    def update(self, screen: pygame.Surface):
        self.check_input()

        if self.sprite is not None and self.active:
            self.sprite.update(screen)
            pygame.draw.rect(screen, (255, 0, 0), self.sprite.get_rect(), 1)

        self.text.update(screen)

    def check_input(self) -> None:
        mouse_position = InputManager.get_mouse_position()

        if InputManager.get_mouse_down(0):
            is_clicked = False

            if self.sprite is not None:
                is_clicked = self.sprite.get_rect().collidepoint(mouse_position)
            else:
                is_clicked = self.text_rect.collidepoint(mouse_position)

            if is_clicked:
                self.on_left_click()

        if InputManager.get_mouse_down(2):
            is_clicked = False

            if self.sprite is not None:
                is_clicked = self.sprite.get_rect().collidepoint(mouse_position)
            else:
                is_clicked = self.text_rect.collidepoint(mouse_position)

            if is_clicked:
                self.on_right_click()

    def on_left_click(self) -> None:
        if self.left_click_callback is not None:
            function, args, kwargs = self.left_click_callback
            function(*args, **kwargs)

    def on_right_click(self) -> None:
        if self.right_click_callback is not None:
            function, args, kwargs = self.right_click_callback
            function(*args, **kwargs)
