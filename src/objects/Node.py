import pygame

from managers.EaseManager import Ease
from managers.TweenManager import Tween
from objects.button.Button import Button

from constants.AssetPath import ImagePath
from objects.sprite.AnimationSprite import AnimationSprite
from objects.sprite.Sprite import Sprite


class Node:
    def __init__(
        self, coord: tuple[int, int], position: tuple[float, float], state: int
    ) -> None:
        self.coord = coord
        self.position = position

        self.tile = Button(
            pygame.image.load(ImagePath.NEUTRAL),
            position,
            left_click_callback=(self.on_left_click, [], {}),
            right_click_callback=(self.on_right_click, [], {}),
        )

        self.tile.sprite.scale = 0.35

        self.tile.active = False

        self.tree_start_animation = AnimationSprite(
            ImagePath.TREE_START_ANIMATION, (0, 0), 0.35, 51, 0.02
        )

        self.tent_start_animation = AnimationSprite(
            ImagePath.TENT_START_ANIMATION, (0, 0), 0.35, 29, 0.02
        )

        self.tent_hide_animation = AnimationSprite(
            ImagePath.TENT_HIDE_ANIMATION, (0, 0), 0.35, 16, 0.02
        )

        self.neutral = Sprite(pygame.image.load(ImagePath.NEUTRAL), position, 0.35)

        self.grass = Sprite(
            pygame.image.load(ImagePath.GRASS), position, 0.35, (204, 214, 125)
        )

        self._prev_state = state
        self._state = state
        self.set_state(state)

    def update(self, screen: pygame.Surface):
        self.tile.update(screen)

        if self._state == NodeState.TREE:
            self.tree_start_animation.position = (
                self.position[0],
                self.position[1] - 8,
            )
            self.tree_start_animation.update(screen)
        elif self._state == NodeState.TENT:
            self.grass.position = self.position
            self.grass.update(screen)

            self.tent_start_animation.position = (
                self.position[0],
                self.position[1] - 9,
            )

            self.tent_start_animation.update(screen)
        elif self._state == NodeState.MARK:
            self.neutral.position = self.position
            self.neutral.update(screen)

            self.grass.position = self.position
            self.grass.update(screen)

            if self._prev_state == NodeState.TENT:
                self.tent_hide_animation.position = (
                    self.position[0],
                    self.position[1] - 9,
                )

                self.tent_hide_animation.update(screen)
        elif self._state == NodeState.EMPTY:
            self.neutral.position = self.position
            self.neutral.update(screen)

            self.grass.position = self.position
            self.grass.update(screen)

            if self._prev_state == NodeState.TENT:
                self.tent_hide_animation.position = (
                    self.position[0],
                    self.position[1] - 9,
                )

                self.tent_hide_animation.update(screen)

    def get_state(self) -> int:
        return self._state

    def set_state(self, state: int, immediately=False):
        self._prev_state = self._state
        self._state = state

        if self._state == NodeState.EMPTY:
            if immediately:
                self.neutral.scale = 0.35
                self.grass.scale = 0
            else:
                self.neutral.scale = 0
                Tween(self.neutral, 0.35, 0.25, Ease.OUT_QUAD)
                Tween(self.grass, 0, 0.25, Ease.OUT_QUAD)

            if self._prev_state == NodeState.TENT:
                self.tent_hide_animation.play(immediately)
        elif self._state == NodeState.TREE:
            self.tree_start_animation.play(immediately)
        elif self._state == NodeState.MARK:
            if self._prev_state == NodeState.TENT:
                self.tent_hide_animation.play(immediately)
            else:
                if immediately:
                    self.grass.scale = 0.35
                else:
                    self.grass.scale = 0
                    Tween(self.grass, 0.35, 0.25, Ease.OUT_QUAD)

            if immediately or self._prev_state == NodeState.TENT:
                self.neutral.scale = 0
            else:
                Tween(self.neutral, 0, 0.25, Ease.OUT_QUAD)
        elif self._state == NodeState.TENT:
            if immediately:
                self.grass.scale = 0.35
            else:
                self.grass.scale = 0
                Tween(self.grass, 0.35, 0.25, Ease.OUT_QUAD)
            self.tent_start_animation.play(immediately)

    def on_left_click(self):
        if self._state == NodeState.TENT:
            self.set_state(NodeState.EMPTY)
        elif self._state != NodeState.TREE:
            self.set_state(NodeState.TENT)

        self.on_tile_state_changed(self.coord, self._state)

    def on_right_click(self):
        if self._state == NodeState.MARK:
            self.set_state(NodeState.EMPTY)
        elif self._state != NodeState.TREE:
            self.set_state(NodeState.MARK)

        self.on_tile_state_changed(self.coord, self._state)


class NodeState:
    EMPTY = 0
    TREE = 1
    MARK = 2
    TENT = 3
