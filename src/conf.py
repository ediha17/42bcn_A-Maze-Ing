# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    conf.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 15:42:49 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/17 21:29:35 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from typing import Optional
from src import parser


class MazeConfig:
    def __init__(self, map: dict, ent: list[int], ext: list[int]) -> None:
        self.width = map["WIDTH"]
        self.height = map["HEIGHT"]
        self.entry = ent
        self.exit = ext
        self.output_file = map["OUTPUT_FILE"]
        self.perfect = (map["PERFECT"] == "True")


def init_conf(map: dict) -> Optional[MazeConfig]:
    ent: list[int]
    ex: list[int]

    if (not parser.ft_parser_map(map)):
        return (None)
    ent = parser.ft_parser_coords(map["ENTRY"])
    ex = parser.ft_parser_coords(map["EXIT"])
    if (ent[0] == -1 or ex[0] == -1):
        print("Error: Invalid ENTRY or EXIT")
        return (None)
    parser.check_patern42(map["WIDTH"], map["HEIGHT"])
    return (MazeConfig(map, ent, ex))


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
