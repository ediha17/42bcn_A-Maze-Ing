# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    conf.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 15:42:49 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/23 14:03:26 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from typing import Optional, Tuple
from pydantic import BaseModel, Field, field_validator
from src import parser


class MazeConfig(BaseModel):
    WIDTH: int = Field(gt=0)
    HEIGHT: int = Field(gt=0)
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool

    @field_validator('ENTRY', 'EXIT', mode='before')
    @classmethod
    def validate_coords(cls: object, v: str) -> Optional[tuple]:
        if isinstance(v, str):
            res = parser.ft_parser_coords(v)
            if (res[0] == -1):
                raise ValueError("Coordenadas inválidas")
            return tuple(res)
        return (v)



def init_conf(map: dict) -> Optional[MazeConfig]:
    if (not parser.ft_parser_map(map)):
        return (None)
    if (not parser.check_patern42(map["WIDTH"], map["HEIGHT"])):
        return (None)
    try:
        map['PERFECT'] = (map['PERFECT'] == "True")
        return (MazeConfig(**map))
    except Exception as e:
        print(f"Error de validación Pydantic: {e}")
        return (None)


def init_maze(width: int, height: int) -> list[list[str]]:
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
    maze[ent[1]][ent[0]] = 'x'
    maze[ext[1]][ext[0]] = 'o'
    return (None)


def print_map(maze: list[list[str]]) -> None:
    i: int

    if (not maze):
        return (None)
    i = 0
    while (i < len(maze)):
        print("".join(maze[i]))
        i += 1
    return (None)
