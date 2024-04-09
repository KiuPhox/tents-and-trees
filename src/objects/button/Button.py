import pygame

from objects.Text import Text

from managers.InputManager import InputManager
from managers.SceneManager import SceneManager


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
        self.image = image
        self.position = position
        self.text = Text(string, font, position)

        self.image_rect = (
            self.image.get_rect(
                center=(
                    position[0] + image.get_size()[0] / 2,
                    position[1] + image.get_size()[1] / 2,
                )
            )
            if self.image is not None
            else None
        )
        self.text_rect = self.text.text_rect

        self.left_click_callback = left_click_callback
        self.right_click_callback = right_click_callback

    def update(self, screen: pygame.Surface):
        self.check_input()

        if self.image is not None:
            screen.blit(self.image, self.position)

        self.text.update(screen)

    def check_input(self) -> None:
        mouse_positon = InputManager.get_mouse_position()

        if InputManager.get_mouse_down(0):
            is_clicked = False

            if self.image_rect is not None:
                is_clicked = self.image_rect.collidepoint(mouse_positon)
            else:
                is_clicked = self.text_rect.collidepoint(mouse_positon)

            if is_clicked:
                self.on_left_click()

        if InputManager.get_mouse_down(2):
            is_clicked = False

            if self.image_rect is not None:
                is_clicked = self.image_rect.collidepoint(mouse_positon)
            else:
                is_clicked = self.text_rect.collidepoint(mouse_positon)

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
