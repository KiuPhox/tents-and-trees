import pygame

from objects.button.Button import Button
from constants.AssetPath import ImagePath

class Node:
    def __init__(self, coord: tuple[int, int], position: tuple[float, float], state: int) -> None:
        self.coord = coord
        self.position = position
        self.tile = Button(pygame.image.load(ImagePath.BLACK_SQUARE), position, left_click_callback=(self.on_left_click, [], {}), right_click_callback=(self.on_right_click, [], {}))

        self.tree = pygame.image.load(ImagePath.TREE)
        self.tent = pygame.image.load(ImagePath.TENT)

        self.set_state(state)

    def update(self, screen: pygame.Surface):
        self.tile.update(screen)

        if self._state == NodeState.TREE:
            screen.blit(self.tree, (self.position[0], self.position[1] - 10))
        elif self._state == NodeState.TENT:
            screen.blit(self.tent, (self.position[0], self.position[1]))

    def get_state(self) -> int:
        return self._state

    def set_state(self, state: int):
        self._state = state

        if (self._state == NodeState.EMPTY):
            self.tile.image = pygame.image.load(ImagePath.BLACK_SQUARE)
        elif (self._state == NodeState.TREE):
            self.tile.image = pygame.image.load(ImagePath.GREEN_SQUARE)
        elif (self._state == NodeState.MARK):
            self.tile.image = pygame.image.load(ImagePath.GREEN_SQUARE)
        elif (self._state == NodeState.TENT):
            self.tile.image = pygame.image.load(ImagePath.GREEN_SQUARE)
            

    def on_left_click(self):
        if self._state == NodeState.TENT:
            self.set_state(NodeState.EMPTY)
        elif self._state != NodeState.TREE:
            self.set_state(NodeState.TENT)
        
    def on_right_click(self):
        if self._state == NodeState.MARK:
            self.set_state(NodeState.EMPTY)
        elif self._state != NodeState.TREE:
            self.set_state(NodeState.MARK)

class NodeState:
    EMPTY = 0
    TREE = 1
    MARK = 2
    TENT = 3