import time

from ai.state import State
from objects.Tile import TileState


class Searching:
    def __init__(self, board: list[list[int]], rows: list[int], cols: list[int]):
        self.state = State(board, rows, cols)
        self.solution = []
        self.time = 0
        self.total_nodes = 0

    def bfs(self):
        start_time = time.time()

        queue = [self.state]
        visited = []

        while queue:
            current_state = queue.pop(0)
            visited.append(current_state)

            if current_state.is_goal_state():
                while current_state:
                    self.solution.insert(0, current_state)

                    current_state = current_state.previous_state

                self.time = time.time() - start_time
                self.total_nodes = len(visited) + len(queue)
                return self.solution

            possible_states = self.get_possible_states(current_state)

            for state in possible_states:
                if state not in visited and state not in queue:
                    queue.append(state)

        return self.solution

    def dfs(self) -> None:
        start_time = time.time()

        stack = [self.state]
        visited = []

        while stack:
            current_state = stack.pop()
            visited.append(current_state)

            if current_state.is_goal_state():
                while current_state:
                    self.solution.insert(0, current_state)

                    current_state = current_state.previous_state

                self.time = time.time() - start_time
                self.total_nodes = len(visited) + len(stack)
                return self.solution

            possible_states = self.get_possible_states(current_state)

            for state in possible_states:
                if state not in visited and state not in stack:
                    stack.append(state)

        return self.solution

    def get_possible_states(self, state: State) -> list[State]:
        res = []

        for i in range(len(state.board)):
            for j in range(len(state.board[i])):
                if state.is_tent_assignable((i, j)):
                    new_state = State(state.board, state.rows, state.cols)
                    new_state.board[i][j] = TileState.TENT

                    new_state.previous_state = state

                    res.append(new_state)

        return res

    def reset(self) -> None:
        self.state = State(self.state.board, self.state.rows, self.state.cols)
        self.solution = []
