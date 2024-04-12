import random
import pygame

from constants.AssetPath import ImagePath

from engine.Button import Button
from engine.GameObject import GameObject
from engine.components.Sprite import Sprite
from engine.components.AnimationSprite import AnimationSprite

from managers.EaseManager import Ease
from managers.TweenManager import Tween

from scenes.Scene import Scene
from utils.Color import Color


class Tile:
    def __init__(
        self,
        coord: tuple[int, int],
        position: tuple[float, float],
        state: int,
        scene: Scene,
    ) -> None:
        self.coord = coord
        self.position = position
        self.scene = scene

        self.create_button()
        self.create_neutral()
        self.create_grass()
        self.create_tent()
        self.create_tree()

        self._prev_state = state
        self._state = state

        self.set_state(state)

    def create_button(self):
        self.button = Button(self.scene, ImagePath.NEUTRAL)
        self.button.left_click_callback = (self.on_left_click, [], {})
        self.button.right_click_callback = (self.on_right_click, [], {})
        self.button.scale = (0.35, 0.35)
        self.button.position = self.position
        self.button.active = False

    def create_neutral(self):
        self.neutral = GameObject(self.scene)
        self.neutral.position = self.position
        self.neutral.scale = (0.35, 0.35)

        neutral_sprite = Sprite(self.neutral)
        neutral_sprite.set_sprite(ImagePath.NEUTRAL)

    def create_grass(self):
        self.grass = GameObject(self.scene)
        self.grass.position = self.position
        self.grass.scale = (0.35, 0.35)

        grass_sprite = Sprite(self.grass)
        grass_sprite.set_sprite(ImagePath.GRASS)
        grass_sprite.color = Color.hsl_to_rgb(
            (67, 0.52, 0.7 - random.randint(0, 3) * 0.05)
        )

    def create_tent(self):
        self.tent_start = GameObject(self.scene)
        self.tent_start.position = (self.position[0], self.position[1])
        self.tent_start.scale = (0.35, 0.35)

        self.tent_start_animation = AnimationSprite(
            self.tent_start, ImagePath.TENT_START_ANIMATION, 29, 0.02
        )
        self.tent_start.add_component(self.tent_start_animation)

        self.tent_hide = GameObject(self.scene)
        self.tent_hide.position = (self.position[0], self.position[1])
        self.tent_hide.scale = (0.35, 0.35)

        self.tent_hide_animation = AnimationSprite(
            self.tent_hide, ImagePath.TENT_HIDE_ANIMATION, 16, 0.02
        )
        self.tent_hide.add_component(self.tent_hide_animation)

    def create_tree(self):
        self.tree = GameObject(self.scene)
        self.tree.position = (self.position[0], self.position[1] - 8)
        self.tree.scale = (0.35, 0.35)

        self.tree_start_animation = AnimationSprite(
            self.tree, ImagePath.TREE_START_ANIMATION, 51, 0.02
        )
        self.tree.add_component(self.tree_start_animation)

    def set_state(self, state: int, immediately=False):
        self._prev_state = self._state
        self._state = state

        self.grass.active = False
        self.neutral.active = False
        self.tent_start.active = False
        self.tent_hide.active = False

        if self._state == TileState.EMPTY:
            self.tree.active = False

            self.show(self.neutral, immediately)

            if self._prev_state == TileState.TENT:
                self.tent_hide.active = True
                self.tent_hide_animation.play(immediately)

        elif self._state == TileState.MARK:
            self.grass.active = True

            if self._prev_state == TileState.TENT:
                self.tent_hide.active = True
                self.tent_hide_animation.play(immediately)
            else:
                self.show(self.grass, immediately)

            if self._prev_state == TileState.EMPTY:
                self.hide(self.neutral, immediately)
        elif self._state == TileState.TENT:
            self.grass.active = True
            self.tent_start.active = True
            self.tent_start_animation.play(immediately)

            if self._prev_state == TileState.EMPTY:
                self.show(self.grass, immediately)
                self.hide(self.neutral, immediately)

        elif self._state == TileState.TREE:
            self.tree.active = True
            self.tree_start_animation.play(immediately)

    def show(self, game_object: GameObject, immediately=False):
        if immediately:
            game_object.active = True
            game_object.scale = (0.35, 0.35)
            return

        game_object.active = True
        game_object.scale = (0.0, 0.0)
        Tween(game_object, (0.35, 0.35), 0.25).set_ease(Ease.OUT_QUAD)

    def hide(self, game_object: GameObject, immediately=False):
        if immediately:
            game_object.active = True
            game_object.scale = (0, 0)
            return

        game_object.active = True
        game_object.scale = (0.35, 0.35)
        Tween(game_object, (0.0, 0.0), 0.25).set_ease(Ease.OUT_QUAD)

    def on_left_click(self):
        if self._state == TileState.TENT:
            self.set_state(TileState.EMPTY)
        elif self._state != TileState.TREE:
            self.set_state(TileState.TENT)

        self.on_tile_state_changed(self.coord, self._state)

    def on_right_click(self):
        if self._state == TileState.MARK:
            self.set_state(TileState.EMPTY)
        elif self._state != TileState.TREE:
            self.set_state(TileState.MARK)

        self.on_tile_state_changed(self.coord, self._state)


class TileState:
    EMPTY = 0
    TREE = 1
    MARK = 2
    TENT = 3
