import math

from engine.GameObject import GameObject
from managers.EaseManager import Ease, EaseManager

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
        self,
        game_object: GameObject,
        scale: tuple[float, float],
        duration: float,
        ease=Ease.LINEAR,
    ) -> None:
        self.game_object = game_object
        self.ease = ease
        self.duration = duration

        self.start_scale = self.game_object.scale
        self.end_scale = scale

        self.start_time = Time.time

        TweenManager.tweens.append(self)

    def update(self):
        elapsed = Time.time - self.start_time
        t = min(elapsed / self.duration, 1)

        xScale = self.start_scale[0] + EaseManager.ease_func(self.ease, t) * (
            self.end_scale[0] - self.start_scale[0]
        )

        yScale = self.start_scale[1] + EaseManager.ease_func(self.ease, t) * (
            self.end_scale[1] - self.start_scale[1]
        )

        self.game_object.scale = (xScale, yScale)

        if t == 1:
            self.destroy()

    def destroy(self):
        TweenManager.tweens.remove(self)
