# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    test_parser.py                                    :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/30 09:00:00 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/30 09:00:00 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from src.parser import (ft_parser, ft_parser_map,
                        ft_parser_coords, check_patern42)


# ── ft_parser ───────────────────────────────────────────────────────────────

def test_parser_int_value() -> None:
    data = b'WIDTH=20\nHEIGHT=15\n'
    result = ft_parser(data)
    assert (result['WIDTH'] == 20)
    assert (result['HEIGHT'] == 15)


def test_parser_string_value() -> None:
    result = ft_parser(b'OUTPUT_FILE=maze.txt\n')
    assert (result['OUTPUT_FILE'] == 'maze.txt')


def test_parser_ignores_comments() -> None:
    result = ft_parser(b'# comment\nWIDTH=10\n')
    assert ('WIDTH' in result)
    assert ('#' not in result)


def test_parser_ignores_empty_lines() -> None:
    result = ft_parser(b'\n\nWIDTH=5\n\n')
    assert (result['WIDTH'] == 5)
    assert (len(result) == 1)


def test_parser_strips_whitespace() -> None:
    result = ft_parser(b'  WIDTH  =  20  \n')
    assert (result['WIDTH'] == 20)


def test_parser_coord_stays_string() -> None:
    result = ft_parser(b'ENTRY=0,1\n')
    assert (result['ENTRY'] == '0,1')


# ── ft_parser_map ───────────────────────────────────────────────────────────

def test_parser_map_all_keys_present() -> None:
    data = {
        'WIDTH': 20, 'HEIGHT': 15,
        'ENTRY': '0,1', 'EXIT': '19,13',
        'OUTPUT_FILE': 'maze.txt', 'PERFECT': 'True'
    }
    assert (ft_parser_map(data) is True)


def test_parser_map_missing_key() -> None:
    assert (ft_parser_map({'WIDTH': 20, 'HEIGHT': 15}) is False)


def test_parser_map_empty_dict() -> None:
    assert (ft_parser_map({}) is False)


def _base_map(perfect: object) -> dict:
    return {
        'WIDTH': 20, 'HEIGHT': 15,
        'ENTRY': '0,1', 'EXIT': '19,13',
        'OUTPUT_FILE': 'maze.txt', 'PERFECT': perfect
    }


def test_parser_map_perfect_false_valid() -> None:
    assert (ft_parser_map(_base_map('False')) is True)


def test_parser_map_perfect_invalid_uppercase() -> None:
    assert (ft_parser_map(_base_map('TRUE')) is False)
    assert (ft_parser_map(_base_map('FALSE')) is False)


def test_parser_map_perfect_invalid_string() -> None:
    assert (ft_parser_map(_base_map('maybe')) is False)
    assert (ft_parser_map(_base_map('NONE')) is False)


def test_parser_map_perfect_invalid_int() -> None:
    assert (ft_parser_map(_base_map(1)) is False)
    assert (ft_parser_map(_base_map(0)) is False)


def test_parser_map_seed_valid() -> None:
    m = _base_map('True')
    m['SEED'] = 42
    assert (ft_parser_map(m) is True)


def test_parser_map_seed_negative_valid() -> None:
    m = _base_map('True')
    m['SEED'] = -1
    assert (ft_parser_map(m) is True)


def test_parser_map_seed_absent_valid() -> None:
    assert (ft_parser_map(_base_map('True')) is True)


def test_parser_map_seed_string_invalid() -> None:
    m = _base_map('True')
    m['SEED'] = 'abc'
    assert (ft_parser_map(m) is False)


# ── ft_parser_coords ────────────────────────────────────────────────────────

def test_coords_basic() -> None:
    assert (ft_parser_coords('0,1') == [0, 1])
    assert (ft_parser_coords('19,13') == [19, 13])


def test_coords_with_spaces() -> None:
    assert (ft_parser_coords(' 0 , 1 ') == [0, 1])


def test_coords_single_value() -> None:
    assert (ft_parser_coords('0') == [-1, -1])


def test_coords_three_values() -> None:
    assert (ft_parser_coords('0,1,2') == [-1, -1])


# ── check_patern42 ──────────────────────────────────────────────────────────

def test_pattern42_large_enough() -> None:
    assert (check_patern42(10, 10) is True)
    assert (check_patern42(7, 7) is True)


def test_pattern42_too_small() -> None:
    assert (check_patern42(6, 10) is False)
    assert (check_patern42(10, 6) is False)
    assert (check_patern42(3, 3) is False)


# ── BREAKING ─────────────────────────────────────────────────────────────────

def test_parser_invalid_utf8() -> None:
    """ft_parser crashes with UnicodeDecodeError on non-UTF8 bytes."""
    ft_parser(b'\xff\xfeWIDTH=20\n')
