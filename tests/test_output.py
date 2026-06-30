# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    test_output.py                                    :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/30 09:00:00 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/30 09:00:00 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import pytest
from src.output import (maze_to_hex_grid, grid_to_cell_coords,
                        bfs_cell_path, write_output_file)


# ── maze_to_hex_grid ────────────────────────────────────────────────────────

def test_hex_all_walls_closed() -> None:
    """3x3 grid with all walls: single cell encodes as F (0b1111)."""
    maze = [['|', '|', '|'],
            ['|', '|', '|'],
            ['|', '|', '|']]
    assert (maze_to_hex_grid(maze, 3, 3) == ['F'])


def test_hex_all_walls_open() -> None:
    """3x3 grid fully open: single cell encodes as 0."""
    maze = [[' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']]
    assert (maze_to_hex_grid(maze, 3, 3) == ['0'])


def test_hex_north_wall_only() -> None:
    """Only north wall closed → bit 0 → value 1."""
    maze = [['|', '|', '|'],
            [' ', ' ', ' '],
            [' ', ' ', ' ']]
    assert (maze_to_hex_grid(maze, 3, 3) == ['1'])


def test_hex_east_wall_only() -> None:
    """Only east wall closed → bit 1 → value 2."""
    maze = [[' ', ' ', ' '],
            [' ', ' ', '|'],
            [' ', ' ', ' ']]
    assert (maze_to_hex_grid(maze, 3, 3) == ['2'])


def test_hex_south_wall_only() -> None:
    """Only south wall closed → bit 2 → value 4."""
    maze = [[' ', ' ', ' '],
            [' ', ' ', ' '],
            ['|', '|', '|']]
    assert (maze_to_hex_grid(maze, 3, 3) == ['4'])


def test_hex_west_wall_only() -> None:
    """Only west wall closed → bit 3 → value 8."""
    maze = [[' ', ' ', ' '],
            ['|', ' ', ' '],
            [' ', ' ', ' ']]
    assert (maze_to_hex_grid(maze, 3, 3) == ['8'])


def test_hex_correct_row_count() -> None:
    """5x5 grid should produce 2 rows of 2 cells each."""
    maze = [['|'] * 5 for _ in range(5)]
    rows = maze_to_hex_grid(maze, 5, 5)
    assert (len(rows) == 2)
    assert (len(rows[0]) == 2)


# ── grid_to_cell_coords ─────────────────────────────────────────────────────

def test_cell_coords_left_border() -> None:
    assert (grid_to_cell_coords([0, 1], 9, 9) == (0, 0))
    assert (grid_to_cell_coords([0, 3], 9, 9) == (0, 1))


def test_cell_coords_top_border() -> None:
    assert (grid_to_cell_coords([1, 0], 9, 9) == (0, 0))
    assert (grid_to_cell_coords([3, 0], 9, 9) == (1, 0))


def test_cell_coords_right_border() -> None:
    assert (grid_to_cell_coords([8, 1], 9, 9) == (3, 0))
    assert (grid_to_cell_coords([8, 3], 9, 9) == (3, 1))


def test_cell_coords_bottom_border() -> None:
    assert (grid_to_cell_coords([1, 8], 9, 9) == (0, 3))
    assert (grid_to_cell_coords([3, 8], 9, 9) == (1, 3))


# ── bfs_cell_path ───────────────────────────────────────────────────────────

def test_bfs_single_row_east() -> None:
    """3 fully open cells in one row: path must be EE."""
    hex_grid = ['000']
    assert (bfs_cell_path(hex_grid, (0, 0), (2, 0)) == 'EE')


def test_bfs_single_column_south() -> None:
    """3 fully open cells in one column: path must be SS."""
    hex_grid = ['0', '0', '0']
    assert (bfs_cell_path(hex_grid, (0, 0), (0, 2)) == 'SS')


def test_bfs_no_path_all_walls() -> None:
    """All walls closed: no path exists."""
    hex_grid = ['FFF', 'FFF', 'FFF']
    assert (bfs_cell_path(hex_grid, (0, 0), (2, 2)) == '')


def test_bfs_start_equals_end() -> None:
    """Start and end are the same cell: empty path."""
    hex_grid = ['000']
    assert (bfs_cell_path(hex_grid, (0, 0), (0, 0)) == '')


# ── write_output_file ───────────────────────────────────────────────────────

def test_write_output_format(tmp_path: pytest.TempPathFactory) -> None:
    """Output file must match the subject format exactly."""
    out = str(tmp_path / 'maze_test.txt')
    hex_rows = ['ABC', 'DEF']
    write_output_file(out, hex_rows, [0, 1], [9, 7], 'SESE')
    with open(out) as f:
        lines = f.readlines()
    assert (lines[0] == 'ABC\n')
    assert (lines[1] == 'DEF\n')
    assert (lines[2] == '\n')
    assert (lines[3] == '0,1\n')
    assert (lines[4] == '9,7\n')
    assert (lines[5] == 'SESE\n')
