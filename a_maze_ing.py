# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 15:34:41 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/23 21:43:22 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import sys
import random
from typing import IO, Optional
from src import parser, conf
from src.output import (maze_to_hex_grid, grid_to_cell_coords,
                        bfs_cell_path, write_output_file)
from mazegen.mazegen import check_collision, draw_pattern_42, generate_maze


def coords_to_seed(entry: tuple[int, int], exit_val: tuple[int, int]) -> int:
    seed = (entry[0] * 1000) + (entry[1] * 100000) + (exit_val[0] * 10) + (exit_val[1] * 10000)
    return (seed)


def main(ac: int, av: list[str]) -> int:
    fd: bytes
    f: IO[bytes]
    map: dict
    data: Optional[conf.MazeConfig]
    maze: list[list[str]]
    hex_grid: list[str]
    entry_cell: tuple[int, int]
    exit_cell: tuple[int, int]
    solution: str

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
        seed = coords_to_seed(data.ENTRY, data.EXIT)
        random.seed(seed)
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
        conf.set_entry_exit(maze, ENTRY, EXIT)
        conf.print_map(maze)
        hex_grid = maze_to_hex_grid(maze, data.WIDTH, data.HEIGHT)
        entry_cell = grid_to_cell_coords(ENTRY, data.WIDTH, data.HEIGHT)
        exit_cell = grid_to_cell_coords(EXIT, data.WIDTH, data.HEIGHT)
        solution = bfs_cell_path(hex_grid, entry_cell, exit_cell)
        if (solution):
            print(f"Camino más corto encontrado: {solution}")
        else:
            print("No se ha encontrado ninguna ruta válida"
                  " (quizás el patrón 42 o una pared bloquean el paso).")
        write_output_file(data.OUTPUT_FILE, hex_grid, ENTRY, EXIT, solution)
        print(f"Maze guardado en: {data.OUTPUT_FILE}")
    except FileNotFoundError:
        print(f"Error: The file '{av[1]}' was not found.")
        return (1)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return (1)
    return (0)


if (__name__ == "__main__"):
    sys.exit(main(len(sys.argv), sys.argv))
