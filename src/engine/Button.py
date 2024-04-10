import pygame

from engine.GameObject import GameObject
from engine.components.Text import Text
from engine.components.Sprite import Sprite

from managers.UIManager import UIManager


class Button(GameObject):
    def __init__(
        self,
        scene,
        image: str = None,
        string: str = "",
        left_click_callback=None,
        right_click_callback=None,
    ) -> None:
        super().__init__(scene)

        self.sprite = None

        if image is not None:
            self.sprite = Sprite(self)
            self.sprite.set_sprite(image)
            self.add_component(self.sprite)

        self.label = Text(self)
        self.label.text = string
        self.add_component(self.label)

        self.left_click_callback = left_click_callback
        self.right_click_callback = right_click_callback

        self.touch_zone_size = (0, 0)

        UIManager.register_button(self)

    def update(self):
        super().update()
        self.label.position = self.position

    def on_left_click(self) -> None:
        if self.left_click_callback is not None:
            function, args, kwargs = self.left_click_callback
            function(*args, **kwargs)

    def on_right_click(self) -> None:
        if self.right_click_callback is not None:
            function, args, kwargs = self.right_click_callback
            function(*args, **kwargs)

    def destroy(self):
        UIManager.unregister_button(self)
        super().destroy()

    def touch_zone(self) -> tuple[float, float]:
        if self.sprite is None:
            return (
                self.position[0] - self.touch_zone_size[0] / 2,
                self.position[1] - self.touch_zone_size[1] / 2,
                self.position[0] + self.touch_zone_size[0] / 2,
                self.position[1] + self.touch_zone_size[1] / 2,
            )

        return (
            self.position[0] - self.sprite.width() / 2,
            self.position[1] - self.sprite.height() / 2,
            self.position[0] + self.sprite.width() / 2,
            self.position[1] + self.sprite.height() / 2,
        )