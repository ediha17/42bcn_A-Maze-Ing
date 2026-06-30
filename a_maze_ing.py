# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 15:34:41 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/30 09:00:00 by agarcia2        ###   ########.fr        #
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
    """Derive a deterministic seed from entry and exit coordinates."""
    seed = (entry[0] * 1000) + (entry[1] * 100000) + \
           (exit_val[0] * 10) + (exit_val[1] * 10000)
    return (seed)


def load_maze(filepath: str) -> Optional[tuple]:
    """Load a config file, generate the maze and compute the solution.

    Args:
        filepath: Path to a KEY=VALUE config file.

    Returns:
        Tuple (data, maze, hex_grid, ENTRY, EXIT, solution) on success,
        or None if the file is missing or the config is invalid.
    """
    fd: bytes
    f: IO[bytes]
    raw: dict
    data: Optional[conf.MazeConfig]
    maze: list[list[str]]
    hex_grid: list[str]
    entry_cell: tuple[int, int]
    exit_cell: tuple[int, int]
    solution: str
    ENTRY: list[int]
    EXIT: list[int]

    try:
        with (open(filepath, 'rb') as f):
            fd = f.read()
            raw = parser.ft_parser(fd)
            data = conf.init_conf(raw)
        if (data is None):
            return (None)
        seed = coords_to_seed(data.ENTRY, data.EXIT)
        random.seed(seed)
        maze = conf.init_maze(data.WIDTH, data.HEIGHT)
        generate_maze(maze, data.WIDTH, data.HEIGHT)
        draw_pattern_42(maze, 2, 2)
        ENTRY = list(data.ENTRY)
        EXIT = list(data.EXIT)
        if (check_collision(2, 2, ENTRY)):
            print("WARNING: ENTRY movida por conflicto con patron 42.")
            ENTRY = [0, 1]
        if (check_collision(2, 2, EXIT)):
            print("WARNING: EXIT movida por conflicto con patron 42.")
            EXIT = [data.WIDTH - 1, data.HEIGHT - 2]
        conf.set_entry_exit(maze, ENTRY, EXIT)
        hex_grid = maze_to_hex_grid(maze, data.WIDTH, data.HEIGHT)
        entry_cell = grid_to_cell_coords(ENTRY, data.WIDTH, data.HEIGHT)
        exit_cell = grid_to_cell_coords(EXIT, data.WIDTH, data.HEIGHT)
        solution = bfs_cell_path(hex_grid, entry_cell, exit_cell)
        return (data, maze, hex_grid, ENTRY, EXIT, solution)
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return (None)
    except Exception as e:
        print(f"Error: {e}")
        return (None)


def print_menu() -> None:
    """Print the interactive menu options."""
    print("\n1. Cargar nuevo mapa")
    print("2. Guardar mapa")
    print("3. Salir")
    return (None)


def run_menu(filepath: str) -> int:
    """Display the maze and run the interactive menu loop.

    Args:
        filepath: Path to the initial config file.

    Returns:
        0 on clean exit, 1 if the initial load fails.
    """
    data: Optional[conf.MazeConfig]
    maze: list[list[str]]
    hex_grid: list[str]
    ENTRY: list[int]
    EXIT: list[int]
    solution: str
    result: Optional[tuple]
    choice: str
    new_path: str

    result = load_maze(filepath)
    if (result is None):
        return (1)
    data, maze, hex_grid, ENTRY, EXIT, solution = result

    while (True):
        conf.print_map(maze)
        if (solution):
            print(f"Solucion: {solution}")
        else:
            print("Sin solucion disponible.")
        print_menu()
        try:
            choice = input("Elige una opcion: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            return (0)
        if (choice == '1'):
            try:
                new_path = input("Ruta del nuevo config: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nSaliendo...")
                return (0)
            result = load_maze(new_path)
            if (result is None):
                print("Error al cargar. Se mantiene el mapa actual.")
                continue
            data, maze, hex_grid, ENTRY, EXIT, solution = result
        elif (choice == '2'):
            write_output_file(data.OUTPUT_FILE, hex_grid, ENTRY, EXIT, solution)
            print(f"Mapa guardado en: {data.OUTPUT_FILE}")
        elif (choice == '3'):
            print("Saliendo...")
            return (0)
        else:
            print("Opcion no valida. Elige 1, 2 o 3.")
    return (0)


def main(ac: int, av: list[str]) -> int:
    """Entry point. Expects exactly one argument: the config file path."""
    if (ac != 2):
        print(f"Program use: Python3 {sys.argv[0]} <file>")
        return (1)
    return (run_menu(av[1]))


if (__name__ == "__main__"):
    sys.exit(main(len(sys.argv), sys.argv))
