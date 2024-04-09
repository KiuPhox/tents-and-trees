import pygame
import copy

from constants.GameConfig import ScreenSize
from constants.AssetPath import ImagePath
from constants.AssetPath import FontPath

from managers.GameManager import GameManager

from objects.Node import Node, NodeState
from objects.Text import Text

TEXT_DEFAULT_COLOR = (127, 79, 65)
TEXT_CORRECT_COLOR = (201, 167, 153)
TEXT_WRONG_COLOR = (255, 0, 0)

NODE_SIZE = 57


class Grid:
    def start(self):
        self.initial_matrix = []
        self.current_matrix = []

        self.initial_rows_index = []
        self.initial_cols_index = []
        self.current_rows_index = []
        self.current_cols_index = []

        self.rows_text = []
        self.cols_text = []

        self.grid: list[list[Node]] = []

        self.font = pygame.font.Font(FontPath.TT_FORS, 36)

    def create(self):
        level_data = GameManager.get_current_level_data()

        self.initial_matrix = level_data["map"]
        self.current_matrix = copy.deepcopy(self.initial_matrix)
        self.current_rows_index = self.initial_rows_index = level_data["rows"]
        self.initial_cols_index = self.current_cols_index = level_data["cols"]

        rows = len(self.initial_matrix)
        cols = len(self.initial_matrix[0])

        for y in range(rows):
            row = []
            for x in range(cols):
                pos = (
                    (x + 0.5 - cols / 2) * NODE_SIZE,
                    (y + 0.5 - rows / 2) * NODE_SIZE,
                )
                coord = (x, y)

                node = Node(coord, pos, self.initial_matrix[y][x])
                node.on_tile_state_changed = self.on_tile_state_changed

                row.append(node)
            self.grid.append(row)

        for i in range(rows):
            text = Text(
                str(self.initial_rows_index[i]),
                self.font,
                (
                    (i - cols / 2) * NODE_SIZE + 32 + ScreenSize.WIDTH / 2,
                    ScreenSize.HEIGHT / 2 - (cols / 2 + 0.5) * NODE_SIZE,
                ),
            )
            text.color = TEXT_DEFAULT_COLOR
            self.rows_text.append(text)
        for i in range(cols):
            text = Text(
                str(self.initial_cols_index[i]),
                self.font,
                (
                    ScreenSize.WIDTH / 2 - (rows / 2 + 0.5) * NODE_SIZE,
                    (i - rows / 2) * NODE_SIZE + 32 + ScreenSize.HEIGHT / 2,
                ),
            )
            text.color = TEXT_DEFAULT_COLOR
            self.cols_text.append(text)

        self.update_ui()

    def reset(self):
        self.current_matrix = copy.deepcopy(self.initial_matrix)
        self.current_rows_index = self.initial_rows_index
        self.current_cols_index = self.initial_cols_index

        self.update_ui()
        self.update_grid()

    def update(self, screen: pygame.Surface):
        for row in self.grid:
            for node in row:
                node.update(screen)

        for text in self.rows_text:
            text.update(screen)

        for text in self.cols_text:
            text.update(screen)

    def on_tile_state_changed(self, coord: tuple[int, int], state: int):
        self.current_matrix[coord[1]][coord[0]] = state
        self.update_ui()

    def update_ui(self):
        for i in range(len(self.current_rows_index)):
            if self.get_col_tents(i) == self.current_rows_index[i]:
                self.rows_text[i].color = TEXT_CORRECT_COLOR
            elif self.get_col_tents(i) > self.current_rows_index[i]:
                self.rows_text[i].color = TEXT_WRONG_COLOR
            else:
                self.rows_text[i].color = TEXT_DEFAULT_COLOR

        for i in range(len(self.current_cols_index)):
            if self.get_row_tents(i) == self.current_cols_index[i]:
                self.cols_text[i].color = TEXT_CORRECT_COLOR
            elif self.get_row_tents(i) > self.current_cols_index[i]:
                self.cols_text[i].color = TEXT_WRONG_COLOR
            else:
                self.cols_text[i].color = TEXT_DEFAULT_COLOR

    def update_grid(self, immediately=False):
        for row in self.grid:
            for node in row:
                node.set_state(
                    self.current_matrix[node.coord[1]][node.coord[0]], immediately
                )

    def get_col_tents(self, col: int):
        tents = 0
        for row in self.current_matrix:
            if row[col] == NodeState.TENT:
                tents += 1
        return tents

    def get_row_tents(self, row: int):
        tents = 0
        for cell in self.current_matrix[row]:
            if cell == NodeState.TENT:
                tents += 1
        return tents
