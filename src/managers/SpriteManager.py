class SpriteManager:
    sprites = []

    @staticmethod
    def init():
        SpriteManager.sprites = []

    @staticmethod
    def register_sprite(sprite):
        SpriteManager.sprites.append(sprite)

    @staticmethod
    def unregister_sprite(sprite):
        SpriteManager.sprites.remove(sprite)
