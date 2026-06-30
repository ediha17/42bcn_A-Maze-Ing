# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    bfs_path_finder.py                                :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 15:34:41 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/30 09:00:00 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from collections import deque


def reconstruct_path(
        came_from: dict[tuple[int, int], tuple[tuple[int, int], str]],
        start_x: int, start_y: int, exit_x: int, exit_y: int) -> str:
    """Rebuild the direction string by walking came_from back to start.

    Args:
        came_from: Maps each position to (previous position, direction taken).
        start_x: X coordinate of the starting position.
        start_y: Y coordinate of the starting position.
        exit_x: X coordinate of the goal position.
        exit_y: Y coordinate of the goal position.

    Returns:
        String of directions (N/E/S/W) from start to exit.
    """
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
    """Find the shortest path in the character grid using BFS.

    Traverses ' ' and 'o' cells. Used for terminal display of the solution.

    Args:
        maze: Character grid (' ' = passage, '|' = wall, 'o' = exit).
        start_x: Entry column in the grid.
        start_y: Entry row in the grid.
        exit_x: Exit column in the grid.
        exit_y: Exit row in the grid.

    Returns:
        Direction string (N/E/S/W) or empty string if no path exists.
    """
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
