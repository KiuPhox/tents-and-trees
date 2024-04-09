import pygame

from constants.GameConfig import ScreenSize
from objects.sprite.Sprite import Sprite
from utils.Time import Time


class AnimationSprite(Sprite):
    def __init__(self, image_path, pos, scale=1, frame_count=1, frame_duration=0.1):
        # get all the frames from the image folder path
        self.frame_count = frame_count
        self.frame_duration = frame_duration
        self.frames = [
            pygame.image.load(f"{image_path}/{i}.png") for i in range(frame_count)
        ]

        super().__init__(self.frames[0], pos, scale)

        self.current_frame = 0
        self.frame_time = 0
        self.playing = False

    def update(self, screen: pygame.Surface):
        if self.playing:
            self.frame_time += Time.deltaTime

            if self.frame_time >= self.frame_duration:
                self.current_frame += 1
                self.frame_time = 0

                if self.current_frame >= self.frame_count:
                    self.current_frame = self.frame_count - 1
                    self.stop()

        self.image = self.frames[self.current_frame]

        super().update(screen)

    def play(self, immediately=False):
        if immediately:
            self.current_frame = self.frame_count - 1
            return

        self.current_frame = 0
        self.frame_time = 0
        self.image = self.frames[self.current_frame]

        self.playing = True

    def stop(self):
        self.playing = False
