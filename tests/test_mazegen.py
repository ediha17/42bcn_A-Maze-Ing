# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    test_mazegen.py                                   :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/30 09:00:00 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/30 09:00:00 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from collections import deque
import pytest
from mazegen.mazegen import MazeGenerator


def _all_cells_reachable(maze: list[list[str]], width: int, height: int) -> bool:
    """BFS from (1,1) — return True if all odd-position cells are visited."""
    visited: set[tuple[int, int]] = {(1, 1)}
    queue: deque[tuple[int, int]] = deque([(1, 1)])
    while (queue):
        x, y = queue.popleft()
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height
                    and (nx, ny) not in visited
                    and maze[ny][nx] != '|'):
                visited.add((nx, ny))
                queue.append((nx, ny))
    for cy in range(1, height - 1, 2):
        for cx in range(1, width - 1, 2):
            if ((cx, cy) not in visited):
                return (False)
    return (True)


def test_generate_returns_correct_dimensions() -> None:
    mg = MazeGenerator(9, 9, seed=42)
    mg.generate()
    maze = mg.get_maze()
    assert (len(maze) == 9)
    assert (len(maze[0]) == 9)


def test_seed_makes_generation_reproducible() -> None:
    mg1 = MazeGenerator(9, 9, seed=42)
    mg1.generate()
    mg2 = MazeGenerator(9, 9, seed=42)
    mg2.generate()
    assert (mg1.get_maze() == mg2.get_maze())


def test_different_seeds_produce_different_mazes() -> None:
    mg1 = MazeGenerator(9, 9, seed=1)
    mg1.generate()
    mg2 = MazeGenerator(9, 9, seed=2)
    mg2.generate()
    assert (mg1.get_maze() != mg2.get_maze())


def test_perfect_maze_all_cells_reachable() -> None:
    mg = MazeGenerator(11, 11, seed=42, perfect=True)
    mg.generate()
    assert (_all_cells_reachable(mg.get_maze(), 11, 11))


def test_imperfect_maze_has_more_open_passages() -> None:
    mg_perfect = MazeGenerator(11, 11, seed=99, perfect=True)
    mg_perfect.generate()
    mg_imperfect = MazeGenerator(11, 11, seed=99, perfect=False)
    mg_imperfect.generate()
    perfect_walls = sum(row.count('|') for row in mg_perfect.get_maze())
    imperfect_walls = sum(row.count('|') for row in mg_imperfect.get_maze())
    assert (imperfect_walls < perfect_walls)


def test_check_collision_inside() -> None:
    assert (MazeGenerator.check_collision(2, 2, [3, 3]) is True)
    assert (MazeGenerator.check_collision(2, 2, [2, 2]) is True)
    assert (MazeGenerator.check_collision(2, 2, [6, 6]) is True)


def test_check_collision_outside() -> None:
    assert (MazeGenerator.check_collision(2, 2, [7, 7]) is False)
    assert (MazeGenerator.check_collision(2, 2, [1, 3]) is False)
    assert (MazeGenerator.check_collision(2, 2, [3, 1]) is False)


def test_pattern_42_stamps_corners() -> None:
    mg = MazeGenerator(11, 11, seed=42)
    mg.generate()
    mg.draw_pattern_42(2, 2)
    maze = mg.get_maze()
    assert (maze[2][2] == '|')
    assert (maze[2][6] == '|')
    assert (maze[6][2] == '|')
    assert (maze[6][6] == '|')


def test_generate_raises_on_tiny_maze() -> None:
    mg = MazeGenerator(2, 2)
    with pytest.raises(RuntimeError):
        mg.generate()
