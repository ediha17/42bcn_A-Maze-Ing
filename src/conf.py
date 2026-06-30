# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    conf.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 15:42:49 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/30 16:14:15 by ehorvat          ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from typing import Optional, Tuple
from pydantic import BaseModel, Field, field_validator
from src import parser


class MazeConfig(BaseModel):
    """Validated configuration for a maze generation run."""

    WIDTH: int = Field(gt=0)
    HEIGHT: int = Field(gt=0)
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool

    @field_validator('ENTRY', 'EXIT', mode='before')
    @classmethod
    def validate_coords(cls: object, v: str) -> Optional[tuple]:
        """Parse and validate a coordinate value from the config dict.

        Args:
            v: Raw string 'x,y' or already-parsed tuple.

        Returns:
            Tuple (x, y) on success.

        Raises:
            ValueError: If the coordinate string is malformed.
        """
        if isinstance(v, str):
            res = parser.ft_parser_coords(v)
            if (res[0] == -1):
                raise ValueError("Coordenadas inválidas")
            return tuple(res)
        return (v)


def init_conf(map: dict) -> Optional[MazeConfig]:
    """Validate a parsed config dict and return a MazeConfig instance.

    Args:
        map: Dict produced by ft_parser().

    Returns:
        A MazeConfig on success, or None if validation fails.
    """
    if (not parser.ft_parser_map(map)):
        return (None)
    if (not parser.check_patern42(map["WIDTH"], map["HEIGHT"])):
        return (None)

    if map["WIDTH"] % 2 == 0:
        map["WIDTH"] += 1
    if map["HEIGHT"] % 2 == 0:
        map["HEIGHT"] += 1
    try:
        map['PERFECT'] = (map['PERFECT'] == "True")
        return (MazeConfig(**map))
    except Exception as e:
        print(f"Error de validación Pydantic: {e}")
        return (None)


def init_maze(width: int, height: int) -> list[list[str]]:
    """Allocate a WIDTH x HEIGHT grid filled with '|' (all walls closed).

    Args:
        width: Number of columns.
        height: Number of rows.

    Returns:
        2D list of '|' characters.
    """
    map: list[list[str]]
    row: list[str]
    i: int
    j: int

    map = []
    i = 0
    while (i < height):
        row = []
        j = 0
        while (j < width):
            row.append('|')
            j += 1
        i += 1
        map.append(row)
    return (map)


def set_entry_exit(maze: list[list[str]], ent: list[int],
                   ext: list[int]) -> None:
    """Mark entry ('x') and exit ('o') and open the adjacent passages.

    Args:
        maze: Character grid to modify in-place.
        ent: [x, y] grid position of the entry.
        ext: [x, y] grid position of the exit.
    """
    maze[ent[1]][ent[0]] = 'x'
    maze[ext[1]][ext[0]] = 'o'
    if (ent[0] == 0):
        maze[ent[1]][1] = ' '
    elif (ent[1] == 0):
        maze[1][ent[0]] = ' '
    if (ext[0] == len(maze[0]) - 1):
        maze[ext[1]][ext[0] - 1] = ' '
        if ((ext[0] - 1) % 2 == 0):
            maze[ext[1]][ext[0] - 2] = ' '
    if (ext[1] == len(maze) - 1):
        maze[ext[1] - 1][ext[0]] = ' '
        if ((ext[1] - 1) % 2 == 0):
            maze[ext[1] - 2][ext[0]] = ' '
    return (None)


def print_map(maze: list[list[str]]) -> None:
    """Print the maze character grid to stdout.

    Args:
        maze: 2D list representing the maze.
    """
    i: int

    if (not maze):
        return (None)
    i = 0
    while (i < len(maze)):
        print("".join(maze[i]))
        i += 1
    return (None)
