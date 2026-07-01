import random
import sys
from typing import Optional


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None,
                 perfect: bool = True) -> None:
        self._width: int
        self._height: int
        self._perfect: bool
        self._seed: Optional[int]
        self._maze: list[list[str]]

        self._width = width
        self._height = height
        self._perfect = perfect
        self._maze = []
        if (seed is not None):
            random.seed(seed)

    def generate(self) -> None:
        if (self._width < 3 or self._height < 3):
            raise RuntimeError('Maze dimensions must be at least 3x3.')
        self._maze = self._init_grid(self._width, self._height)

        # El patrón que define nuestro 42
        pattern = [
            "1010111",
            "1010001",
            "1110111",
            "0010100",
            "0010111"
        ]

        if (self._width >= 9 and self._height >= 7):
            start_x = (self._width - 7) // 2
            start_y = (self._height - 5) // 2

            if start_x % 2 == 0:
                start_x += 1
            if start_y % 2 == 0:
                start_y += 1

            y = 0
            while y < len(pattern):
                x = 0
                while x < len(pattern[y]):
                    if pattern[y][x] == '1':
                        self._maze[start_y + y][start_x + x] = '*'
                    x += 1
                y += 1
        else:
            print("Error: The maze size does not allow the '42' pattern.")

        sys.setrecursionlimit(max(sys.getrecursionlimit(),
                                  self._width * self._height))
        self._dfs(self._maze, 1, 1, self._width, self._height)

        if (not self._perfect):
            self._add_cycles(self._maze, self._width, self._height)

        # 2. Dibujamos el 42 definitivo respetando los nuevos límites
        if (self._width >= 9 and self._height >= 7):
            self.draw_pattern_42(self._maze, start_x, start_y)

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
                    if (pattern[y][x] == '1'):
                        maze[start_y + y][start_x + x] = '|'
                    else:
                        maze[start_y + y][start_x + x] = ' '
                x += 1
            y += 1

    def get_maze(self) -> list[list[str]]:
        return (self._maze)

    @staticmethod
    def check_collision(start_x: int, start_y: int, pos: list[int]) -> bool:
        return ((start_x <= pos[0] < start_x + 7)
                and (start_y <= pos[1] < start_y + 5))

    @staticmethod
    def _init_grid(width: int, height: int) -> list[list[str]]:
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
        return (grid)

    @staticmethod
    def _dfs(maze: list[list[str]], x: int, y: int,
             width: int, height: int) -> None:
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
                MazeGenerator._dfs(maze, next_x, next_y, width, height)
            i += 1

    @staticmethod
    def _add_cycles(maze: list[list[str]], width: int, height: int,
                    probability: float = 0.15) -> None:
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
