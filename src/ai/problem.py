from ai.state import State
from objects.Tile import TileState


def get_adjacent_positions(
    position: tuple[int, int], size: tuple[int, int]
) -> list[tuple[int, int]]:
    res = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            new_x = position[0] + i
            new_y = position[1] + j

            if new_x < 0 or new_x >= size[0] or new_y < 0 or new_y >= size[1]:
                continue

            res.append((new_x, new_y))

    return res


def get_horizontal_and_vertical_positions(
    position: tuple[int, int], size: tuple[int, int]
) -> list[tuple[int, int]]:
    res = []

    for i in range(-1, 2):
        if i == 0:
            continue

        new_x = position[0] + i
        new_y = position[1]

        if new_x < 0 or new_x >= size[0] or new_y < 0 or new_y >= size[1]:
            continue

        res.append((new_x, new_y))

    for j in range(-1, 2):
        if j == 0:
            continue

        new_x = position[0]
        new_y = position[1] + j

        if new_x < 0 or new_x >= size[0] or new_y < 0 or new_y >= size[1]:
            continue

        res.append((new_x, new_y))

    return res


def tent_assignable(state: State, position: tuple[int, int]) -> bool:
    node_state = state.board[position[0]][position[1]]

    assignable = False

    if node_state != TileState.EMPTY and node_state != TileState.MARK:
        return False

    for adj_pos in get_adjacent_positions(
        position, (len(state.board), len(state.board[0]))
    ):
        if state.board[adj_pos[0]][adj_pos[1]] == TileState.TENT:
            return False

    for hor_vert_pos in get_horizontal_and_vertical_positions(
        position, (len(state.board), len(state.board[0]))
    ):
        if state.board[hor_vert_pos[0]][hor_vert_pos[1]] == TileState.TREE:
            assignable = True
            break

    if not assignable:
        return False

    for i in range(len(state.rows)):
        if state.get_col_tents(i) > state.rows[i]:
            return False

    for i in range(len(state.cols)):
        if state.get_row_tents(i) > state.cols[i]:
            return False

    return True


def get_possible_states(state: State) -> list[State]:
    res = []

    for i in range(len(state.board)):
        for j in range(len(state.board[i])):
            if tent_assignable(state, (i, j)):
                new_state = State(state.board, state.rows, state.cols)
                new_state.board[i][j] = TileState.TENT

                new_state.previous_state = state

                res.append(new_state)

    return res
