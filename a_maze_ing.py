# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 15:34:41 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/17 21:20:14 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import sys
from typing import IO, Optional
from src import parser
from src import conf


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
            print("🛑 El programa se detuvo aquí porque data es None.")
            return (1)
        print("✅ Los datos son válidos. Voy a generar el mapa...")
        maze = conf.init_maze(data.width, data.height)
        print(f"DEBUG: Filas totales esperadas (HEIGHT): {data.height}")
        print(f"DEBUG: Filas reales en la lista (len(maze)): {len(maze)}")
        conf.set_entry_exit(maze, data.entry, data.exit)
        print("✅ Mapa generado en memoria. Voy a imprimirlo...")
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
