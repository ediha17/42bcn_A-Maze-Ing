from collections import deque


def maze_to_hex_grid(
        maze: list[list[str]], width: int, height: int) -> list[str]:
    rows: list[str]
    row_str: str
    cell_val: int
    gx: int
    gy: int

    rows = []
    gy = 1
    while (gy < height - 1):
        row_str = ''
        gx = 1
        while (gx < width - 1):
            cell_val = 0
            if (maze[gy - 1][gx] == '|'):
                cell_val |= 1
            if (maze[gy][gx + 1] == '|'):
                cell_val |= 2
            if (maze[gy + 1][gx] == '|'):
                cell_val |= 4
            if (maze[gy][gx - 1] == '|'):
                cell_val |= 8
            row_str += format(cell_val, 'X')
            gx += 2
        rows.append(row_str)
        gy += 2
    return (rows)


def grid_to_cell_coords(
        pos: list[int], width: int, height: int) -> tuple[int, int]:
    if (pos[0] == 0):
        return (0, (pos[1] - 1) // 2)
    if (pos[1] == 0):
        return ((pos[0] - 1) // 2, 0)
    if (pos[0] == width - 1):
        return ((width - 3) // 2, (pos[1] - 1) // 2)
    return ((pos[0] - 1) // 2, (height - 3) // 2)


def _reconstruct_cell_path(
        came_from: dict[tuple[int, int], tuple[tuple[int, int], str]],
        start: tuple[int, int],
        end: tuple[int, int]) -> str:
    path: list[str]
    curr: tuple[int, int]
    prev: tuple[int, int]
    move: str

    path = []
    curr = end
    while (curr != start):
        prev, move = came_from[curr]
        path.append(move)
        curr = prev
    path.reverse()
    return (''.join(path))


def bfs_cell_path(
        hex_grid: list[str],
        start: tuple[int, int],
        end: tuple[int, int]) -> str:
    directions: list[tuple[int, int, str, int]]
    num_rows: int
    num_cols: int
    queue: deque[tuple[int, int]]
    visited: set[tuple[int, int]]
    came_from: dict[tuple[int, int], tuple[tuple[int, int], str]]
    cx: int
    cy: int
    cell_val: int

    directions = [(0, -1, 'N', 1), (1, 0, 'E', 2),
                  (0, 1, 'S', 4), (-1, 0, 'W', 8)]
    num_rows = len(hex_grid)
    num_cols = len(hex_grid[0]) if (num_rows > 0) else 0
    queue = deque([start])
    visited = {start}
    came_from = {}

    while (queue):
        cx, cy = queue.popleft()
        if ((cx, cy) == end):
            return (_reconstruct_cell_path(came_from, start, end))
        cell_val = int(hex_grid[cy][cx], 16)
        for dx, dy, move, bit in directions:
            if (not (cell_val & bit)):
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < num_cols and 0 <= ny < num_rows
                        and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    came_from[(nx, ny)] = ((cx, cy), move)
                    queue.append((nx, ny))
    return ('')


def write_output_file(path: str, hex_rows: list[str],
                      entry: list[int], exit_: list[int],
                      solution: str) -> None:
    i: int

    with open(path, 'w') as f:
        i = 0
        while (i < len(hex_rows)):
            f.write(hex_rows[i] + '\n')
            i += 1
        f.write('\n')
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        f.write(solution + '\n')
    return (None)
