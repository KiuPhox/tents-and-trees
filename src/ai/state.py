import copy

from objects.Node import NodeState


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

    def __bool__(self):
        return len(self.board) != 0

    def get_tents(self) -> int:
        tents = 0
        for row in self.board:
            for cell in row:
                if cell == NodeState.TENT:
                    tents += 1
        return tents

    def get_row_tents(self, row: int) -> int:
        tents = 0
        for cell in self.board[row]:
            if cell == NodeState.TENT:
                tents += 1
        return tents

    def get_col_tents(self, col: int) -> int:
        tents = 0
        for row in self.board:
            if row[col] == NodeState.TENT:
                tents += 1
        return tents

    def is_goal_state(self) -> bool:
        for i in range(len(self.cols)):
            if self.get_col_tents(i) != self.rows[i]:
                return False

        for i in range(len(self.rows)):
            if self.get_row_tents(i) != self.cols[i]:
                return False

        return True
