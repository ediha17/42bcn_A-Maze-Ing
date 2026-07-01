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


def _count_open_passages(maze: list[list[str]], width: int, height: int) -> int:
    """Count internal wall positions that are open (' ').

    Passage positions are where exactly one of (x, y) is even — the slots
    between cells, not the cells themselves nor the border.
    """
    count: int = 0
    y: int = 1
    while (y < height - 1):
        x: int = 1
        while (x < width - 1):
            if ((x % 2) != (y % 2) and maze[y][x] == ' '):
                count += 1
            x += 1
        y += 1
    return (count)


# ── generate ────────────────────────────────────────────────────────────────

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
    # 15x15 leaves enough free cells outside the 42-pattern for seeds to diverge
    mg1 = MazeGenerator(15, 15, seed=1)
    mg1.generate()
    mg2 = MazeGenerator(15, 15, seed=2)
    mg2.generate()
    assert (mg1.get_maze() != mg2.get_maze())


def test_perfect_maze_all_cells_reachable() -> None:
    # 5x5 has no 42-pattern so all 4 cells must be connected by the DFS
    mg = MazeGenerator(5, 5, seed=42, perfect=True)
    mg.generate()
    assert (_all_cells_reachable(mg.get_maze(), 5, 5))


def test_imperfect_maze_has_more_open_passages() -> None:
    # 21x21 has enough interior walls for _add_cycles to reliably remove at least one
    mg_perfect = MazeGenerator(21, 21, seed=99, perfect=True)
    mg_perfect.generate()
    mg_imperfect = MazeGenerator(21, 21, seed=99, perfect=False)
    mg_imperfect.generate()
    perfect_walls = sum(row.count('|') for row in mg_perfect.get_maze())
    imperfect_walls = sum(row.count('|') for row in mg_imperfect.get_maze())
    assert (imperfect_walls < perfect_walls)


def test_perfect_maze_is_spanning_tree() -> None:
    # 5x5 has 2x2=4 cells → spanning tree needs exactly 3 open passages
    mg = MazeGenerator(5, 5, seed=42, perfect=True)
    mg.generate()
    n_cells = (5 // 2) * (5 // 2)
    assert (_count_open_passages(mg.get_maze(), 5, 5) == n_cells - 1)


def test_imperfect_maze_has_cycles() -> None:
    # 21x21 has enough walls for _add_cycles to open at least one extra passage
    mg = MazeGenerator(21, 21, seed=42, perfect=False)
    mg.generate()
    n_cells = (21 // 2) * (21 // 2)
    assert (_count_open_passages(mg.get_maze(), 21, 21) > n_cells - 1)


def test_generate_raises_on_tiny_maze() -> None:
    import pytest
    mg = MazeGenerator(2, 2)
    with pytest.raises(RuntimeError):
        mg.generate()


# ── check_collision ──────────────────────────────────────────────────────────

def test_check_collision_inside() -> None:
    assert (MazeGenerator.check_collision(2, 2, [3, 3]) is True)
    assert (MazeGenerator.check_collision(2, 2, [2, 2]) is True)
    assert (MazeGenerator.check_collision(2, 2, [6, 6]) is True)


def test_check_collision_outside() -> None:
    assert (MazeGenerator.check_collision(2, 2, [7, 7]) is False)
    assert (MazeGenerator.check_collision(2, 2, [1, 3]) is False)
    assert (MazeGenerator.check_collision(2, 2, [3, 1]) is False)


# ── draw_pattern_42 ──────────────────────────────────────────────────────────

def test_pattern_42_stamps_corners() -> None:
    mg = MazeGenerator(11, 11, seed=42)
    mg.generate()
    maze = mg.get_maze()
    MazeGenerator.draw_pattern_42(maze, 2, 2)
    assert (maze[2][2] == '|')
    assert (maze[2][6] == '|')
    assert (maze[6][2] == ' ')
    assert (maze[6][6] == '|')


def test_huge_maze_no_recursion_error() -> None:
    mg = MazeGenerator(501, 501, seed=1)
    mg.generate()
    assert (len(mg.get_maze()) == 501)
    assert (len(mg.get_maze()[0]) == 501)
