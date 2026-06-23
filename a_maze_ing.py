# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 15:34:41 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/23 14:55:25 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import sys
from typing import IO, Optional
from src import parser
from src import conf
from mazegen.mazegen import check_collision, draw_pattern_42, generate_maze


def main(ac: int, av: list[str]) -> int:
    fd: bytes
    f: IO[bytes]
    map: dict
    data: Optional[conf.MazeConfig]
    maze: list[list[str]]

    if (ac != 2):
        print(f"Porgram use: Python3 {sys.argv[0]} <file>")
        return (1)
    try:
        with (open(av[1], 'rb') as f):
            fd = f.read()
            map = parser.ft_parser(fd)
            data = conf.init_conf(map)
        if (data is None):
            return (1)
        maze = conf.init_maze(data.WIDTH, data.HEIGHT)
        generate_maze(maze, data.WIDTH, data.HEIGHT)
        draw_pattern_42(maze, 2, 2)
        ENTRY = list(data.ENTRY)
        EXIT = list(data.EXIT)
        if (check_collision(2, 2, ENTRY)):
            print("⚠️ WARNING: ENTRY movida por conflicto con patrón 42.")
            ENTRY = [0, 1]
        if (check_collision(2, 2, EXIT)):
            print("⚠️ WARNING: EXIT movida por conflicto con patrón 42.")
            EXIT = [data.WIDTH - 1, data.HEIGHT - 2]
        conf.set_entry_exit(maze, list(data.ENTRY), list(data.EXIT))
        conf.print_map(maze)
    except FileNotFoundError:
        print(f"Error: The file '{av[1]}' was not found.")
        return (1)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return (1)
    return (0)


if (__name__ == "__main__"):
    sys.exit(main(len(sys.argv), sys.argv))
