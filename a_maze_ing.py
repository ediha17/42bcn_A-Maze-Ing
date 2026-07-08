import sys
import random
from typing import IO, Optional, Any
from src import parser, conf
from src.output import (maze_to_hex_grid, write_output_file)
from src.bfs_path_finder import bfs_shortest_path
from mazegen.mazegen import MazeGenerator

COLORS = {
    "blanco": "\033[97m",
    "rojo": "\033[91m",
    "verde": "\033[92m",
    "azul": "\033[94m",
    "amarillo": "\033[93m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "reset": "\033[0m",
    "bg_azul": "\033[44m"
}


def _cell_to_char_pos(cell: list[int],
                      width: int, height: int) -> tuple[int, int]:

    cx, cy = cell[0], cell[1]
    return (cx * 2 + 1, cy * 2 + 1)


def load_maze(filepath: str,
              new_seed: Optional[int] = None) -> Optional[tuple[
                  conf.MazeConfig, list[list[str]], list[str],
                  list[int], list[int], str]]:

    fd: bytes
    f: IO[bytes]
    raw: dict[str, Any]
    data: Optional[conf.MazeConfig]
    maze: list[list[str]]
    hex_grid: list[str]
    ex: int
    ey: int
    ox: int
    oy: int
    raw_path: str
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

        ENTRY = list(data.ENTRY)
        EXIT = list(data.EXIT)

        orig_entry = list(ENTRY)
        orig_exit = list(EXIT)

        seed_to_use = (new_seed if (new_seed is not None)
                       else getattr(data, 'SEED', 0))

        data.SEED = seed_to_use

        generator = MazeGenerator(data.WIDTH, data.HEIGHT,
                                  seed_to_use, data.PERFECT)
        generator.generate()
        maze = generator.get_maze()

        if (data.WIDTH >= 9 and data.HEIGHT >= 7):
            start_cx = (data.WIDTH - 7) // 2
            start_cy = (data.HEIGHT - 5) // 2
            if start_cx % 2 == 0:
                start_cx += 1
            if start_cy % 2 == 0:
                start_cy += 1

            char_entry = [ENTRY[0] * 2 + 1, ENTRY[1] * 2 + 1]
            char_exit = [EXIT[0] * 2 + 1, EXIT[1] * 2 + 1]

            if (MazeGenerator.check_collision(start_cx, start_cy, char_entry)):
                print("WARNING: ENTRY movida por conflicto con patron 42.")
                ENTRY = [0, 0]
            if (MazeGenerator.check_collision(start_cx, start_cy, char_exit)):
                print("WARNING: EXIT movida por conflicto con patron 42.")
                EXIT = [(data.WIDTH - 3) // 2, (data.HEIGHT - 3) // 2]

        # chequeo de seguridad para que
        # no se pase de los maximos de la maze
        max_cx = (data.WIDTH - 1) // 2 - 1
        max_cy = (data.HEIGHT - 1) // 2 - 1
        ENTRY[0] = max(0, min(ENTRY[0], max_cx))
        ENTRY[1] = max(0, min(ENTRY[1], max_cy))
        EXIT[0] = max(0, min(EXIT[0], max_cx))
        EXIT[1] = max(0, min(EXIT[1], max_cy))

        if (orig_entry != ENTRY):
            print(f"Error: La entrada (ENTRY) ha sido movida"
                  f"de {orig_entry} a {ENTRY} "
                  "por límites del mapa o conflicto con el patrón 42.")
        if (orig_exit != EXIT):
            print(f"Error: La salida (EXIT) ha sido movida"
                  f"de {orig_exit} a {EXIT} "
                  f"por límites del mapa o conflicto con el patrón 42.")

        conf.set_entry_exit(maze, ENTRY, EXIT)
        hex_grid = maze_to_hex_grid(maze, data.WIDTH, data.HEIGHT)

        ex, ey = _cell_to_char_pos(ENTRY, data.WIDTH, data.HEIGHT)
        ox, oy = _cell_to_char_pos(EXIT, data.WIDTH, data.HEIGHT)
        raw_path = bfs_shortest_path(maze, ex, ey, ox, oy)
        solution = raw_path[::2]

        return (data, maze, hex_grid, ENTRY, EXIT, solution)

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return (None)
    except Exception as e:
        print(f"Error: {e}")
        return (None)


def print_menu() -> None:
    print("\n1. Regenerar mapa aleatorio")
    print("2. Guardar mapa")
    print("3. Alternar visibilidad de la ruta (On/Off)")
    print("4. Cambiar color del laberinto")
    print("5. Salir")


def get_path_coords(entry_cell: tuple[int, int],
                    solution: str) -> set[tuple[int, int]]:

    coords: set[tuple[int, int]] = set()
    cx_cell, cy_cell = entry_cell

    rx, ry = (cx_cell * 2) + 1, (cy_cell * 2) + 1
    coords.add((rx, ry))

    for move in solution:
        if move == 'N':
            coords.add((rx, ry - 1))  # Añade la pared rota al norte
            cy_cell -= 1
        elif move == 'S':
            coords.add((rx, ry + 1))  # Añade la pared rota al sur
            cy_cell += 1
        elif move == 'E':
            coords.add((rx + 1, ry))  # Añade la pared rota al este
            cx_cell += 1
        elif move == 'W':
            coords.add((rx - 1, ry))  # Añade la pared rota al oeste
            cx_cell -= 1

        rx, ry = (cx_cell * 2) + 1, (cy_cell * 2) + 1
        coords.add((rx, ry))

    return coords


def print_colored_maze(maze: list[list[str]],
                       path_coords: set[tuple[int, int]],
                       show_path: bool, wall_color: str) -> None:

    width = len(maze[0])
    height = len(maze)

    has_42 = (width >= 9 and height >= 7)
    start_cx = 0
    start_cy = 0

    if has_42:
        start_cx = (width - 7) // 2
        start_cy = (height - 5) // 2
        if start_cx % 2 == 0:
            start_cx += 1
        if start_cy % 2 == 0:
            start_cy += 1

    y = 0
    while y < len(maze):
        row_str = ""
        x = 0
        while x < len(maze[y]):
            is_in_42 = (has_42
                        and (start_cx <= x < start_cx + 7)
                        and (start_cy <= y < start_cy + 5))
            if maze[y][x] == 'x':
                row_str += COLORS["verde"] + "🟢" + COLORS["reset"]
            elif maze[y][x] == 'o':
                row_str += COLORS["rojo"] + "🔴" + COLORS["reset"]
            elif show_path and (x, y) in path_coords:
                row_str += COLORS["bg_azul"] + "  " + COLORS["reset"]
            elif maze[y][x] == '|':
                if is_in_42:
                    row_str += COLORS["amarillo"] + "██" + COLORS["reset"]
                else:
                    row_str += COLORS[wall_color] + "██" + COLORS["reset"]
            else:
                row_str += "  "
            x += 1
        print(row_str)
        y += 1


def run_menu(filepath: str) -> int:
    show_path = False
    color_list = ["blanco", "cyan", "magenta", "rojo", "verde"]
    current_color_idx = 0
    path_coords: set[tuple[int, int]] = set()
    current_seed: int

    result = load_maze(filepath)
    if (result is None):
        return (1)

    data, maze, hex_grid, ENTRY, EXIT, solution = result
    current_seed = (data.SEED if data.SEED is not None else
                    random.randint(0, 2**31 - 1))
    entry_cell = (ENTRY[0], ENTRY[1])
    exit_cell = (EXIT[0], EXIT[1])
    if (solution):
        path_coords = get_path_coords(entry_cell, solution)

    while (True):

        print("\n" + "=" * 50)
        print_colored_maze(maze, path_coords, show_path,
                           color_list[current_color_idx])
        print("="*50)

        if (not solution and entry_cell != exit_cell):
            print("Aviso: Sin solucion disponible para este mapa.")

        print_menu()

        try:
            choice = input("Elige una opcion (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            return (0)

        if (choice == '1'):
            current_seed = random.randint(0, 2**31 - 1)
            data.SEED = current_seed
            new_result = load_maze(filepath, current_seed)

            if (new_result is None):
                print("Error al regenerar el mapa.")
            else:
                data, maze, hex_grid, ENTRY, EXIT, solution = new_result
                entry_cell = (ENTRY[0], ENTRY[1])
                exit_cell = (EXIT[0], EXIT[1])

                if (solution):
                    path_coords = get_path_coords(entry_cell, solution)
                else:
                    path_coords = set()

        elif (choice == '2'):
            try:
                write_output_file(data.OUTPUT_FILE, hex_grid, ENTRY, EXIT,
                                  solution, current_seed)
                print(f"Mapa guardado con éxito en: {data.OUTPUT_FILE} "
                      f"(SEED={current_seed})")
            except PermissionError:
                print("\nError: Permiso denegado."
                      f"No se puede guardar en '{data.OUTPUT_FILE}'.")
                print("Comprueba los permisos del archivo o del directorio.")
            except Exception as e:
                print(f"\nError inesperado al guardar el mapa: {e}")

        elif (choice == '3'):
            show_path = not show_path

        elif (choice == '4'):
            current_color_idx = (current_color_idx + 1) % len(color_list)

        elif (choice == '5'):
            print("Saliendo...")
            return (0)

        else:
            print("Opcion no valida. Elige un numero del 1 al 5.")


def main(ac: int, av: list[str]) -> int:
    if (ac != 2):
        print(f"Program use: Python3 {sys.argv[0]} <file>")
        return (1)
    return (run_menu(av[1]))


if (__name__ == "__main__"):
    sys.exit(main(len(sys.argv), sys.argv))
