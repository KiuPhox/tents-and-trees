from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.components.Sprite import Sprite


class SpriteManager:
    sprites: list["Sprite"] = []

    @staticmethod
    def init():
        SpriteManager.sprites = []

    @staticmethod
    def register_sprite(sprite):
        SpriteManager.sprites.append(sprite)

    @staticmethod
    def unregister_sprite(sprite):
        SpriteManager.sprites.remove(sprite)
