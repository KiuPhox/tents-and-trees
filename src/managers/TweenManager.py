import math

from managers.EaseManager import Ease, EaseManager
from objects.sprite.Sprite import Sprite

from utils.Time import Time


class TweenManager:
    tweens = []

    @staticmethod
    def init():
        TweenManager.tweens = []

    @staticmethod
    def update():
        for tween in TweenManager.tweens:
            tween.update()


class Tween:
    def __init__(
        self, sprite: Sprite, scale: float, duration: float, ease=Ease.LINEAR
    ) -> None:
        self.sprite = sprite
        self.ease = ease
        self.duration = duration

        self.start_scale = sprite.scale
        self.end_scale = scale

        self.start_time = Time.time

        TweenManager.tweens.append(self)

    def update(self):
        elapsed = Time.time - self.start_time
        t = min(elapsed / self.duration, 1)

        self.sprite.scale = self.start_scale + EaseManager.ease_func(self.ease, t) * (
            self.end_scale - self.start_scale
        )

        if t == 1:
            self.destroy()

    def destroy(self):
        TweenManager.tweens.remove(self)
