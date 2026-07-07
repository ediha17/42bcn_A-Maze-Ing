# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    test_conf.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/30 09:00:00 by agarcia2         #+#    #+#              #
#    Updated: 2026/07/01 09:00:00 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from src.conf import set_entry_exit, init_conf


def _blank_maze(width: int, height: int) -> list[list[str]]:
    return ([['|'] * width for _ in range(height)])


# ── init_conf ────────────────────────────────────────────────────────────────

def test_init_conf_converts_dimensions() -> None:
    raw = {
        'WIDTH': 10, 'HEIGHT': 10,
        'ENTRY': '0,0', 'EXIT': '9,9',
        'OUTPUT_FILE': 'test.txt', 'PERFECT': 'True'
    }
    data = init_conf(raw)
    assert (data is not None)
    assert (data.WIDTH == 21)
    assert (data.HEIGHT == 21)


def test_init_conf_returns_none_for_missing_key() -> None:
    assert (init_conf({'WIDTH': 10, 'HEIGHT': 10}) is None)


def test_init_conf_returns_none_for_invalid_perfect() -> None:
    raw = {
        'WIDTH': 10, 'HEIGHT': 10,
        'ENTRY': '0,0', 'EXIT': '9,9',
        'OUTPUT_FILE': 'test.txt', 'PERFECT': 'maybe'
    }
    assert (init_conf(raw) is None)


# ── set_entry_exit ────────────────────────────────────────────────────────────

def test_set_entry_exit_left_border() -> None:
    maze = _blank_maze(9, 9)
    set_entry_exit(maze, [0, 0], [3, 3])
    assert (maze[1][0] == 'x')
    assert (maze[1][1] == ' ')


def test_set_entry_exit_right_border() -> None:
    maze = _blank_maze(9, 9)
    set_entry_exit(maze, [0, 0], [3, 3])
    assert (maze[7][8] == 'o')
    assert (maze[7][7] == ' ')


# ── BREAKING ─────────────────────────────────────────────────────────────────

def test_entry_equals_exit_overwrites_entry() -> None:
    """When ENTRY == EXIT, set_entry_exit writes 'o' last, erasing 'x'."""
    maze = _blank_maze(9, 9)
    set_entry_exit(maze, [0, 0], [0, 0])
    assert (maze[1][0] == 'x')
