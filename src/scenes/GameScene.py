import pygame
import copy

from constants.GameConfig import ScreenSize
from constants.AssetPath import FontPath, ImagePath

from managers.SceneManager import SceneManager
from managers.GameManager import GameManager

from objects.Grid import Grid
from objects.Text import Text
from objects.button.Button import Button

from ai.searching import Searching


class GameScene:
    def __init__(self, screen):
        self.screen = screen

        self.bg = pygame.image.load(ImagePath.BACKGROUND)
        self.bg.fill(
            (245, 224, 205),
            special_flags=pygame.BLEND_RGB_MULT,
        )

        self.level_title = Text(
            f"Level {GameManager.current_level}",
            pygame.font.Font(FontPath.TT_FORS, 40),
            (100, 50),
        )

        self.bfs_button = Button(
            None,
            (ScreenSize.WIDTH - 100, 50),
            "BFS",
            pygame.font.Font(FontPath.TT_FORS, 40),
            left_click_callback=(self.on_bfs_button_click, [], {}),
        )

        self.dfs_button = Button(
            None,
            (ScreenSize.WIDTH - 100, 100),
            "DFS",
            pygame.font.Font(FontPath.TT_FORS, 40),
            left_click_callback=(self.on_dfs_button_click, [], {}),
        )

        self.previous_button = Button(
            None,
            (ScreenSize.WIDTH / 2 - 100, ScreenSize.HEIGHT - 50),
            "Previous",
            pygame.font.Font(FontPath.TT_FORS, 40),
            left_click_callback=(self.on_previous_button_click, [], {}),
        )

        self.next_button = Button(
            None,
            (ScreenSize.WIDTH / 2 + 100, ScreenSize.HEIGHT - 50),
            "Next",
            pygame.font.Font(FontPath.TT_FORS, 40),
            left_click_callback=(self.on_next_button_click, [], {}),
        )

        self.exit_button = Button(
            None,
            (ScreenSize.WIDTH - 100, ScreenSize.HEIGHT - 50),
            "Exit",
            pygame.font.Font(FontPath.TT_FORS, 40),
            left_click_callback=(SceneManager.change_scene, ["MenuScene"], {}),
        )

        self.time_text = Text(
            "Time: 0",
            pygame.font.Font(FontPath.TT_FORS, 40),
            (100, ScreenSize.HEIGHT - 50),
        )

        self.time_text.color = (127, 79, 65)
        self.level_title.color = (127, 79, 65)
        self.bfs_button.text.color = (127, 79, 65)
        self.dfs_button.text.color = (127, 79, 65)
        self.previous_button.text.color = (127, 79, 65)
        self.next_button.text.color = (127, 79, 65)
        self.exit_button.text.color = (127, 79, 65)

    def start(self):
        self.level_title.text = f"Level {GameManager.current_level}"
        self.time_text.text = "Time: 0"

        self.grid = Grid()
        self.grid.start()
        self.grid.create()

        self.solution_index = 0

        self.searching = Searching(
            self.grid.initial_matrix,
            self.grid.initial_rows_index,
            self.grid.initial_cols_index,
        )

    def reset_searching(self):
        self.searching.reset()
        self.grid.reset()
        self.grid.update_grid(True)
        self.solution_index = 0

    def on_bfs_button_click(self):
        self.reset_searching()

        self.searching.bfs()
        self.time_text.text = f"Time: {round(self.searching.time, 7)}s"

    def on_dfs_button_click(self):
        self.reset_searching()

        self.searching.dfs()
        self.time_text.text = f"Time: {round(self.searching.time, 7)}s"

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
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))

        self.time_text.update(self.screen)
        self.level_title.update(self.screen)
        self.bfs_button.update(self.screen)
        self.dfs_button.update(self.screen)
        self.previous_button.update(self.screen)
        self.next_button.update(self.screen)
        self.exit_button.update(self.screen)

        self.grid.update(self.screen)
