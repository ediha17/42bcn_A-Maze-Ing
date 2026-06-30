# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    mazegen.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/22 17:46:50 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/30 16:05:21 by ehorvat          ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import random
from typing import Optional


class MazeGenerator:
    """Generates a maze using recursive DFS (backtracking algorithm).

    The internal representation is a character grid where '|' is a wall
    and ' ' is an open passage. Cells are at odd grid positions; wall
    slots between adjacent cells are at even positions.

    Example:
        mg = MazeGenerator(width=9, height=9, seed=42)
        mg.generate()
        mg.draw_pattern_42(2, 2)
        maze = mg.get_maze()
    """

    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None,
                 perfect: bool = True) -> None:
        """Initialize the maze generator.

        Args:
            width: Character-grid width (odd values work best).
            height: Character-grid height (odd values work best).
            seed: Random seed for reproducible generation.
            perfect: If True, generate a spanning-tree maze (unique path
                between any two cells). If False, add extra passages.
        """
        self._width: int
        self._height: int
        self._perfect: bool
        self._maze: list[list[str]]

        self._width = width
        self._height = height
        self._perfect = perfect
        self._maze = []
        if (seed is not None):
            random.seed(seed)

    def generate(self) -> None:
        """Generate the maze using recursive DFS backtracking.

        Raises:
            RuntimeError: If width or height is less than 3.
        """
        if (self._width < 3 or self._height < 3):
            raise RuntimeError('Maze dimensions must be at least 3x3.')
        self._maze = _init_grid(self._width, self._height)
        _dfs(self._maze, 1, 1, self._width, self._height)
        if (not self._perfect):
            _add_cycles(self._maze, self._width, self._height)

    @staticmethod
    def draw_pattern_42(maze: list[list[str]],
                        start_x: int, start_y: int) -> None:
        pattern = [
            "1010111",
            "1010001",
            "1110111",
            "0010100",
            "0010111"
        ]
        y = 0
        while y < len(pattern):
            x = 0
            while x < len(pattern[y]):
                if start_y + y < len(maze) and start_x + x < len(maze[0]):
                    if pattern[y][x] == '1':
                        maze[start_y + y][start_x + x] = '|'
                    else:
                        maze[start_y + y][start_x + x] = ' '
                x += 1
            y += 1

    def get_maze(self) -> list[list[str]]:
        """Return the internal character grid.

        Returns:
            2D list where '|' is a wall and ' ' is an open passage.
        """
        return (self._maze)

    @staticmethod
    def check_collision(start_x: int, start_y: int, pos: list[int]) -> bool:
        """Check if a position falls inside the 5x5 '42' pattern area.

        Args:
            start_x: Top-left x of the pattern bounding box.
            start_y: Top-left y of the pattern bounding box.
            pos: [x, y] position to test.

        Returns:
            True if pos is inside the pattern bounding box.
        """
        return ((start_x <= pos[0] < start_x + 7)
                and (start_y <= pos[1] < start_y + 5))


def _init_grid(width: int, height: int) -> list[list[str]]:
    """Allocate a width x height grid filled with '|' (all walls closed)."""
    grid: list[list[str]]
    row: list[str]
    i: int
    j: int

    grid = []
    i = 0
    while (i < height):
        row = []
        j = 0
        while (j < width):
            row.append('|')
            j += 1
        grid.append(row)
        i += 1
    grid[0][0] = ' '
    return (grid)


def _dfs(maze: list[list[str]], x: int, y: int,
         width: int, height: int) -> None:
    """Recursively carve passages via DFS backtracking."""
    coords: list[tuple[int, int]]
    i: int

    coords = [(2, 0), (-2, 0), (0, -2), (0, 2)]
    random.shuffle(coords)
    i = 0
    while (i < len(coords)):
        next_x = x + coords[i][0]
        next_y = y + coords[i][1]
        if (next_x > 0 and next_x < width - 1
                and next_y > 0 and next_y < height - 1
                and maze[next_y][next_x] == '|'):
            maze[y + coords[i][1] // 2][x + coords[i][0] // 2] = ' '
            maze[next_y][next_x] = ' '
            _dfs(maze, next_x, next_y, width, height)
        i += 1


def _add_cycles(maze: list[list[str]], width: int, height: int,
                probability: float = 0.15) -> None:
    """Remove a random subset of interior walls to introduce cycles."""
    gx: int
    gy: int

    gx = 1
    while (gx < width - 1):
        gy = 1
        while (gy < height - 1):
            is_h_wall = (gx % 2 == 1 and gy % 2 == 0)
            is_v_wall = (gx % 2 == 0 and gy % 2 == 1)
            if ((is_h_wall or is_v_wall) and maze[gy][gx] == '|'):
                if (random.random() < probability):
                    maze[gy][gx] = ' '
            gy += 1
        gx += 1


def _draw_pattern_42(maze: list[list[str]],
                     start_x: int, start_y: int) -> None:
    """Stamp the 5x5 '42' bitmask pattern onto the grid."""
    pattern: list[str]
    y: int
    x: int

    pattern = ['11111', '10101', '11101', '10101', '11111']
    y = 0
    while (y < len(pattern)):
        x = 0
        while (x < len(pattern[y])):
            if (pattern[y][x] == '1'):
                maze[start_y + y][start_x + x] = '|'
            x += 1
        y += 1


# ── Backward-compatible module-level shortcuts ──────────────────────────────

def generate_maze(maze: list[list[str]], width: int, height: int) -> None:
    """Generate a maze in the given character grid via DFS backtracking."""
    maze[0][0] = ' '
    _dfs(maze, 1, 1, width, height)


def draw_pattern_42(maze: list[list[str]],
                    start_x: int, start_y: int) -> None:
    """Stamp the '42' pattern onto an existing maze grid."""
    _draw_pattern_42(maze, start_x, start_y)


def check_collision(start_x: int, start_y: int, pos: list[int]) -> bool:
    """Return True if pos is inside the 5x5 area starting at (start_x, start_y)."""
    return ((start_x <= pos[0] < start_x + 5)
            and (start_y <= pos[1] < start_y + 5))
