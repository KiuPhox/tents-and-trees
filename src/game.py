import pygame
from sys import exit

from utils.Time import Time

from constants.GameConfig import ScreenSize
from constants.AssetPath import *

from scenes.GameScene import GameScene
from scenes.MenuScene import MenuScene

from managers.SceneManager import SceneManager
from managers.InputManager import InputManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tents and Trees")

        self.screen = pygame.display.set_mode((ScreenSize.WIDTH, ScreenSize.HEIGHT))
        self.clock = pygame.time.Clock()

        self.init_scene_manager()

    def init_scene_manager(self):
        SceneManager.scenes["GameScene"] = GameScene(self.screen)
        SceneManager.scenes["MenuScene"] = MenuScene(self.screen)

        SceneManager.change_scene("MenuScene")

    def render(self):
        SceneManager.update()
        pygame.display.update()

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            InputManager.update()

            self.render()

            Time.deltaTime = self.clock.tick(60) / 1000
            Time.time = pygame.time.get_ticks() / 1000


game = Game()
game.update()
