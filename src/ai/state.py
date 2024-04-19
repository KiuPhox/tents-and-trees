import copy

from objects.Tile import TileState
from typing import List, Tuple


class State:
    def __init__(
        self,
        board: List[List[int]],
        rows: List[int],
        cols: List[int],
        previous_state=None,
    ):
        self.board = copy.deepcopy(board)
        self.rows = rows
        self.cols = cols
        self.depth = 0
        self.previous_state = previous_state

        if self.previous_state:
            self.depth = previous_state.depth + 1

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, State):
            return False

        return self.board == value.board

    def get_tents(self) -> int:
        tents = 0
        for row in self.board:
            for cell in row:
                if cell == TileState.TENT:
                    tents += 1
        return tents

    def get_row_tents(self, row: int) -> int:
        tents = 0
        for cell in self.board[row]:
            if cell == TileState.TENT:
                tents += 1
        return tents

    def get_col_tents(self, col: int) -> int:
        tents = 0
        for row in self.board:
            if row[col] == TileState.TENT:
                tents += 1
        return tents

    def width(self):
        return len(self.board)

    def height(self):
        return len(self.board[0])

    def is_goal_state(self) -> bool:
        for i in range(self.height()):
            if self.get_row_tents(i) != self.cols[i]:
                return False

        for i in range(self.width()):
            if self.get_col_tents(i) != self.rows[i]:
                return False

            # Check if each tree has a tent
            for j in range(self.height()):
                if self.board[i][j] != TileState.TREE:
                    continue
                has_tent = False
                hv_coords = self.get_horizontal_and_vertical_coords((i, j))

                for coord in hv_coords:
                    if self.board[coord[0]][coord[1]] == TileState.TENT:
                        has_tent = True
                        break

                if not has_tent:
                    return False

        return True

    def is_coord_valid(self, coord: Tuple[int, int]) -> bool:
        return 0 <= coord[0] < self.width() and 0 <= coord[1] < self.height()

    def is_tent_assignable(self, coord: Tuple[int, int]) -> bool:
        node_state = self.board[coord[0]][coord[1]]

        assignable = False

        if node_state != TileState.EMPTY and node_state != TileState.MARK:
            return False

        for adj_coord in self.get_diagonal_coords(coord):
            if self.board[adj_coord[0]][adj_coord[1]] == TileState.TENT:
                return False

        for hor_vert_coord in self.get_horizontal_and_vertical_coords(coord):
            if self.board[hor_vert_coord[0]][hor_vert_coord[1]] == TileState.TENT:
                return False
            elif self.board[hor_vert_coord[0]][hor_vert_coord[1]] == TileState.TREE:
                assignable = True

        if not assignable:
            return False

        for i in range(self.width()):
            if self.get_col_tents(i) > self.rows[i]:
                return False

        for i in range(self.height()):
            if self.get_row_tents(i) > self.cols[i]:
                return False

        return True

    def get_adjacent_coords(self, coord: Tuple[int, int]) -> List[Tuple[int, int]]:
        res = self.get_horizontal_and_vertical_coords(coord)
        res.extend(self.get_diagonal_coords(coord))

        return res

    def get_diagonal_coords(self, coord: Tuple[int, int]) -> List[Tuple[int, int]]:
        res = []

        top_left_coord = (coord[0] - 1, coord[1] - 1)
        top_right_coord = (coord[0] - 1, coord[1] + 1)
        bottom_left_coord = (coord[0] + 1, coord[1] - 1)
        bottom_right_coord = (coord[0] + 1, coord[1] + 1)

        coords = [
            top_left_coord,
            top_right_coord,
            bottom_left_coord,
            bottom_right_coord,
        ]

        for coord in coords:
            if self.is_coord_valid(coord):
                res.append(coord)

        return res

    def get_horizontal_and_vertical_coords(
        self, coord: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        res = []

        top_coord = (coord[0] - 1, coord[1])
        bottom_coord = (coord[0] + 1, coord[1])
        left_coord = (coord[0], coord[1] - 1)
        right_coord = (coord[0], coord[1] + 1)

        coords = [top_coord, bottom_coord, left_coord, right_coord]

        for coord in coords:
            if self.is_coord_valid(coord):
                res.append(coord)

        return res

    def heuristic(self) -> int:
        return self.get_tents() * 4 - self.depth
