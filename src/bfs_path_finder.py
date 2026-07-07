from collections import deque


def reconstruct_path(
        came_from: dict[tuple[int, int], tuple[tuple[int, int], str]],
        start_x: int, start_y: int, exit_x: int, exit_y: int) -> str:

    curr_x, curr_y = exit_x, exit_y
    path: list[str] = []

    while (curr_x, curr_y) != (start_x, start_y):
        prev_pos, move = came_from[(curr_x, curr_y)]
        path.append(move)
        curr_x, curr_y = prev_pos

    path.reverse()
    return "".join(path)


def bfs_shortest_path(maze: list[list[str]], start_x: int, start_y: int,
                      exit_x: int, exit_y: int) -> str:

    directions = [
        (0, -1, 'N'),
        (1, 0, 'E'),
        (0, 1, 'S'),
        (-1, 0, 'W')
    ]

    height: int = len(maze)
    width: int = len(maze[0]) if height > 0 else 0

    queue: deque[tuple[int, int]] = deque([(start_x, start_y)])
    visited: set[tuple[int, int]] = {(start_x, start_y)}
    came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

    while queue:
        curr_x, curr_y = queue.popleft()

        if curr_x == exit_x and curr_y == exit_y:
            return reconstruct_path(
                    came_from, start_x, start_y, exit_x,
                    exit_y)

        for dx, dy, move_dir in directions:
            nx, ny = curr_x + dx, curr_y + dy

            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    if maze[ny][nx] in [' ', 'o']:
                        visited.add((nx, ny))
                        came_from[(nx, ny)] = ((curr_x, curr_y), move_dir)
                        queue.append((nx, ny))

    return ""
