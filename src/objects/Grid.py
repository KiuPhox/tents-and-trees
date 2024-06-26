import pygame
import copy

from constants.AssetPath import FontPath

from engine.GameObject import GameObject
from engine.components.Text import Text
from managers.GameManager import GameManager

from objects.Tile import Tile, TileState

from scenes.Scene import Scene

from typing import Tuple

TEXT_DEFAULT_COLOR = (127, 79, 65)
TEXT_CORRECT_COLOR = (201, 167, 153)
TEXT_WRONG_COLOR = (255, 0, 0)

TILE_SIZE = 56


class Grid:
    def __init__(self, scene: Scene) -> None:
        self.scene = scene

    def start(self):
        self.initial_matrix = []
        self.current_matrix = []

        self.initial_rows_index = []
        self.initial_cols_index = []
        self.current_rows_index = []
        self.current_cols_index = []

        self.rows_text = []
        self.cols_text = []

        self.grid: list[list[Tile]] = []

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
                    (x + 0.5 - cols / 2) * TILE_SIZE,
                    (y + 0.5 - rows / 2) * TILE_SIZE,
                )
                coord = (x, y)

                tile = Tile(coord, pos, self.initial_matrix[y][x], self.scene, rows - 5)
                tile.on_tile_state_changed = self.on_tile_state_changed

                row.append(tile)
            self.grid.append(row)

        for i in range(rows):
            game_object = GameObject(self.scene)
            game_object.position = (
                (i - cols / 2 + 0.5) * TILE_SIZE,
                -(cols / 2 + 0.5) * TILE_SIZE,
            )

            text = Text(game_object)
            text.text = str(self.initial_rows_index[i])
            text.font = self.font
            text.color = TEXT_DEFAULT_COLOR

            self.rows_text.append(text)

        for i in range(cols):
            game_object = GameObject(self.scene)
            game_object.position = (
                -(rows / 2 + 0.5) * TILE_SIZE,
                (i - rows / 2 + 0.5) * TILE_SIZE,
            )

            text = Text(game_object)

            text.text = str(self.initial_cols_index[i])
            text.font = self.font
            text.color = TEXT_DEFAULT_COLOR

            self.cols_text.append(text)

        self.update_ui()

    def reset(self, immediately=False):
        self.current_matrix = copy.deepcopy(self.initial_matrix)
        self.current_rows_index = self.initial_rows_index
        self.current_cols_index = self.initial_cols_index

        self.update_ui()
        self.update_grid(immediately)

    def on_tile_state_changed(self, coord: Tuple[int, int], state: int):
        self.current_matrix[coord[1]][coord[0]] = state
        self.update_ui()

    def update_ui(self):
        for i in range(len(self.current_rows_index)):
            tents = self.get_col_tile_states(i, TileState.TENT)
            empty = self.get_col_tile_states(i, TileState.EMPTY)

            if tents == self.current_rows_index[i]:
                self.rows_text[i].color = TEXT_CORRECT_COLOR
            elif tents > self.current_rows_index[i] or empty == 0:
                self.rows_text[i].color = TEXT_WRONG_COLOR
            else:
                self.rows_text[i].color = TEXT_DEFAULT_COLOR

        for i in range(len(self.current_cols_index)):
            tents = self.get_row_tile_states(i, TileState.TENT)
            empty = self.get_row_tile_states(i, TileState.EMPTY)

            if tents == self.current_cols_index[i]:
                self.cols_text[i].color = TEXT_CORRECT_COLOR
            elif tents > self.current_cols_index[i] or empty == 0:
                self.cols_text[i].color = TEXT_WRONG_COLOR
            else:
                self.cols_text[i].color = TEXT_DEFAULT_COLOR

    def update_grid(self, immediately=False):
        for row in self.grid:
            for tile in row:
                tile.set_state(
                    self.current_matrix[tile.coord[1]][tile.coord[0]], immediately
                )

    def get_col_tile_states(self, col: int, state: int):
        res = 0
        for row in self.current_matrix:
            if row[col] == state:
                res += 1
        return res

    def get_row_tile_states(self, row: int, state: int):
        res = 0
        for cell in self.current_matrix[row]:
            if cell == state:
                res += 1
        return res
