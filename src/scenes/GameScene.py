import pygame
import copy

from constants.GameConfig import ScreenSize
from constants.AssetPath import FontPath, ImagePath

from engine.Button import Button
from engine.GameObject import GameObject
from engine.components.Sprite import Sprite
from engine.components.Text import Text, TextAlign

from managers.SceneManager import SceneManager
from managers.GameManager import GameManager

from objects.Grid import Grid

from ai.searching import Searching
from scenes.Scene import Scene


class GameScene(Scene):
    def __init__(self, screen):
        super().__init__("GameScene", screen)

    def start(self):
        self.create_background()

        self.create_level_title()
        self.create_time_text()
        self.create_node_text()

        self.create_bfs_button()
        self.create_dfs_button()
        self.create_next_button()
        self.create_previous_button()
        self.create_exit_button()

        self.create_grid()

        self.create_searching()

    def create_background(self):
        self.bg = GameObject(self)
        self.bg.name = "Background"

        bg_sprite = Sprite(self.bg)
        bg_sprite.color = (245, 224, 205)
        bg_sprite.set_sprite(ImagePath.BACKGROUND)
        self.bg.add_component(bg_sprite)

    def create_level_title(self):
        self.level_title = GameObject(self)
        self.level_title.position = (0, -ScreenSize.HEIGHT / 2 + 50)

        level_text = Text(self.level_title)
        level_text.text = f"Level {GameManager.current_level}"
        level_text.font = pygame.font.Font(FontPath.TT_FORS, 40)
        level_text.color = (127, 79, 65)

        self.level_title.add_component(level_text)

    def create_time_text(self):
        self.time = GameObject(self)
        self.time.position = (-ScreenSize.WIDTH / 2 + 50, -ScreenSize.HEIGHT / 2 + 100)

        self.time_text = Text(self.time)
        self.time_text.align = TextAlign.LEFT
        self.time_text.text = f"Time: 0"
        self.time_text.font = pygame.font.Font(FontPath.TT_FORS, 40)
        self.time_text.color = (127, 79, 65)

        self.time.add_component(self.time_text)

    def create_node_text(self):
        self.node = GameObject(self)
        self.node.position = (-ScreenSize.WIDTH / 2 + 50, -ScreenSize.HEIGHT / 2 + 50)

        self.node_text = Text(self.node)
        self.node_text.align = TextAlign.LEFT
        self.node_text.text = f"Node: 0"
        self.node_text.font = pygame.font.Font(FontPath.TT_FORS, 40)
        self.node_text.color = (127, 79, 65)

        self.node.add_component(self.node_text)

    def create_bfs_button(self):
        self.bfs_button = Button(
            self,
            None,
            "BFS",
            left_click_callback=(self.on_bfs_button_click, [], {}),
        )
        self.bfs_button.touch_zone_size = (70, 30)
        self.bfs_button.label.font = pygame.font.Font(FontPath.TT_FORS, 40)
        self.bfs_button.position = (
            ScreenSize.WIDTH / 2 - 100,
            -ScreenSize.HEIGHT / 2 + 50,
        )
        self.bfs_button.label.color = (127, 79, 65)

    def create_dfs_button(self):
        self.dfs_button = Button(
            self,
            None,
            "DFS",
            left_click_callback=(self.on_dfs_button_click, [], {}),
        )
        self.dfs_button.touch_zone_size = (70, 30)
        self.dfs_button.label.font = pygame.font.Font(FontPath.TT_FORS, 40)
        self.dfs_button.position = (
            ScreenSize.WIDTH / 2 - 100,
            -ScreenSize.HEIGHT / 2 + 100,
        )
        self.dfs_button.label.color = (127, 79, 65)

    def create_next_button(self):
        self.next_button = Button(
            self,
            ImagePath.NEXT_BTN,
            "",
            left_click_callback=(self.on_next_button_click, [], {}),
        )
        self.next_button.scale = (0.5, 0.5)
        self.next_button.label.font = pygame.font.Font(FontPath.TT_FORS, 40)
        self.next_button.position = (
            50,
            ScreenSize.HEIGHT / 2 - 50,
        )
        self.next_button.sprite.color = (127, 79, 65)

    def create_previous_button(self):
        self.previous_button = Button(
            self,
            ImagePath.PREV_BTN,
            "",
            left_click_callback=(self.on_previous_button_click, [], {}),
        )
        self.previous_button.scale = (0.5, 0.5)
        self.previous_button.label.font = pygame.font.Font(FontPath.TT_FORS, 40)
        self.previous_button.position = (
            -50,
            ScreenSize.HEIGHT / 2 - 50,
        )
        self.previous_button.sprite.color = (127, 79, 65)

    def create_exit_button(self):
        self.exit_button = Button(
            self,
            None,
            "Exit",
            left_click_callback=(SceneManager.change_scene, ["MenuScene"], {}),
        )
        self.exit_button.touch_zone_size = (80, 50)
        self.exit_button.label.font = pygame.font.Font(FontPath.TT_FORS, 40)
        self.exit_button.position = (
            ScreenSize.WIDTH / 2 - 100,
            ScreenSize.HEIGHT / 2 - 50,
        )
        self.exit_button.label.color = (127, 79, 65)

    def create_grid(self):
        self.grid = Grid(self)
        self.grid.start()
        self.grid.create()

    def create_searching(self):
        self.solution_index = 0

        self.searching = Searching(
            self.grid.initial_matrix,
            self.grid.initial_rows_index,
            self.grid.initial_cols_index,
        )

    def reset_searching(self):
        self.searching.reset()
        self.grid.reset(True)
        self.solution_index = 0

    def on_bfs_button_click(self):
        self.reset_searching()

        self.searching.bfs()
        self.time_text.text = f"Time: {round(self.searching.time, 7)}s"
        self.node_text.text = f"Node: {self.searching.total_nodes}"

    def on_dfs_button_click(self):
        self.reset_searching()

        self.searching.dfs()
        self.time_text.text = f"Time: {round(self.searching.time, 7)}s"
        self.node_text.text = f"Node: {self.searching.total_nodes}"

    def on_previous_button_click(self):
        solution = self.searching.solution
        if self.solution_index > 0:
            self.solution_index -= 1

            self.grid.current_matrix = copy.deepcopy(
                solution[self.solution_index].board
            )
            self.grid.update_ui()
            self.grid.update_grid(True)

    def on_next_button_click(self):
        solution = self.searching.solution
        if self.solution_index < len(solution) - 1:
            self.solution_index += 1

            self.grid.current_matrix = copy.deepcopy(
                solution[self.solution_index].board
            )
            self.grid.update_ui()
            self.grid.update_grid(True)

    def update(self):
        super().update()
        # self.screen.fill((0, 0, 0))
        # self.screen.blit(self.bg, (0, 0))

        # self.time_text.update(self.screen)
        # self.level_title.update(self.screen)
        # self.bfs_button.update(self.screen)
        # self.dfs_button.update(self.screen)
        # self.previous_button.update(self.screen)
        # self.next_button.update(self.screen)
        # self.exit_button.update(self.screen)

        # self.grid.update(self.screen)
