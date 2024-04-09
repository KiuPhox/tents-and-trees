import pygame

from constants.GameConfig import ScreenSize


class Sprite:
    def __init__(self, image, position, scale=1, color=(255, 255, 255)):
        self.position = position
        self.image = image
        self.scale = scale
        self.color = color

    def update(self, screen: pygame.Surface):
        width, height = self.image.get_size()
        new_size = (int(width * self.scale), int(height * self.scale))
        scaled_image = pygame.transform.scale(self.image, new_size)

        new_pos = (
            self.position[0] - new_size[0] / 2 + ScreenSize.WIDTH / 2,
            self.position[1] - new_size[1] / 2 + ScreenSize.HEIGHT / 2,
        )

        scaled_image.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
        screen.blit(scaled_image, new_pos)

    def get_rect(self):
        width, height = self.image.get_size()
        new_size = (int(width * self.scale), int(height * self.scale))

        return pygame.Rect(
            self.position[0] - new_size[0] / 2 + ScreenSize.WIDTH / 2,
            self.position[1] - new_size[1] / 2 + ScreenSize.HEIGHT / 2,
            new_size[0],
            new_size[1],
        )
