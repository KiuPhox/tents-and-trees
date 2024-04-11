import copy

from objects.Tile import TileState


class State:
    def __init__(self, board: list[list[int]], rows: list[int], cols: list[int]):
        self.board = copy.deepcopy(board)
        self.rows = rows
        self.cols = cols
        self.previous_state = None

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
        for i in range(self.width()):
            if self.get_col_tents(i) != self.rows[i]:
                return False

        for i in range(self.height()):
            if self.get_row_tents(i) != self.cols[i]:
                return False

        # Check if all trees have a tent next to them
        for i in range(self.width()):
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

    def get_horizontal_and_vertical_coords(
        self, position: tuple[int, int]
    ) -> list[tuple[int, int]]:
        res = []

        for i in range(-1, 2):
            if i == 0:
                continue

            new_x = position[0] + i
            new_y = position[1]

            if (
                new_x < 0
                or new_x >= self.width()
                or new_y < 0
                or new_y >= self.height()
            ):
                continue

            res.append((new_x, new_y))

        for j in range(-1, 2):
            if j == 0:
                continue

            new_x = position[0]
            new_y = position[1] + j

            if (
                new_x < 0
                or new_x >= self.width()
                or new_y < 0
                or new_y >= self.height()
            ):
                continue

            res.append((new_x, new_y))

        return res
