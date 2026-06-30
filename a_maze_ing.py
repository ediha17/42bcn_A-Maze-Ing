import sys
from typing import IO, Optional
from src import parser, conf
from src.output import (maze_to_hex_grid, grid_to_cell_coords,
                        bfs_cell_path, write_output_file)
from mazegen.mazegen import MazeGenerator

# Colores para el laberinto
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


def coords_to_seed(entry: tuple[int, int], exit_val: tuple[int, int]) -> int:
    """Derive a deterministic seed from entry and exit coordinates."""
    seed = (entry[0] * 1000) + (entry[1] * 100000) + \
           (exit_val[0] * 10) + (exit_val[1] * 10000)
    return (seed)


def load_maze(filepath: str) -> Optional[tuple]:
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

        generator = MazeGenerator(data.WIDTH, data.HEIGHT, seed, data.PERFECT)
        generator.generate()
        maze = generator.get_maze()

        ENTRY = list(data.ENTRY)
        EXIT = list(data.EXIT)

        num_cells_x = data.WIDTH // 2
        num_cells_y = data.HEIGHT // 2
        start_cx = (num_cells_x - 7) // 2
        start_cy = (num_cells_y - 5) // 2

        if (data.WIDTH >= 7 and data.HEIGHT >= 5):
            if (MazeGenerator.check_collision(start_cx, start_cy, ENTRY)):
                print("WARNING: ENTRY movida por conflicto con patron 42.")
                ENTRY = [0, 1]
            if (MazeGenerator.check_collision(start_cx, start_cy, EXIT)):
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
    print("3. Alternar visibilidad de la ruta (On/Off)")
    print("4. Cambiar color del laberinto")
    print("5. Salir")


def get_path_coords(entry: list[int], exit_val: list[int],
                    entry_cell: tuple[int, int],
                    solution: str) -> set[tuple[int, int]]:

    coords: set[tuple[int, int]] = {(entry[0], entry[1]),
                                    (exit_val[0], exit_val[1])}
    cx_cell, cy_cell = entry_cell

    # Coordenada base del primer pasillo en la matriz cruda
    rx, ry = (cx_cell * 2) + 1, (cy_cell * 2) + 1
    coords.add((rx, ry))

    for move in solution:
        if move == 'N':
            coords.add((rx, ry - 1))  # Añade la pared rota
            cy_cell -= 1
        elif move == 'S':
            coords.add((rx, ry + 1))
            cy_cell += 1
        elif move == 'E':
            coords.add((rx + 1, ry))
            cx_cell += 1
        elif move == 'W':
            coords.add((rx - 1, ry))
            cx_cell -= 1

        rx, ry = (cx_cell * 2) + 1, (cy_cell * 2) + 1
        coords.add((rx, ry))

    return coords


def print_colored_maze(maze: list[list[str]],
                       path_coords: set[tuple[int, int]],
                       show_path: bool, wall_color: str) -> None:

    width = len(maze[0])
    height = len(maze)

    # Comprobamos si el laberinto es apto para tener el 42
    has_42 = (width >= 7 and height >= 5)

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
            # Solo marcamos is_in_42 como True si has_42 es True
            is_in_42 = has_42 and (start_cx <= x < start_cx + 7) and (start_cy <= y < start_cy + 5)

            # 1. Pintar Entrada y Salida
            if maze[y][x] == 'x':
                row_str += COLORS["verde"] + "🟢" + COLORS["reset"]
            elif maze[y][x] == 'o':
                row_str += COLORS["rojo"] + "🔴" + COLORS["reset"]
            # 2. Pintar el camino
            elif show_path and (x, y) in path_coords:
                row_str += COLORS["bg_azul"] + "  " + COLORS["reset"]
            # 3. Pintar Paredes
            elif maze[y][x] == '|':
                if is_in_42:
                    row_str += COLORS["amarillo"] + "██" + COLORS["reset"]
                else:
                    row_str += COLORS[wall_color] + "██" + COLORS["reset"]
            # 4. Pasillos vacíos
            else:
                row_str += "  "
            x += 1
        print(row_str)
        y += 1


def run_menu(filepath: str) -> int:
    # 1. Variables de estado de la interfaz visual
    show_path = False
    color_list = ["blanco", "cyan", "magenta", "rojo", "verde"]
    current_color_idx = 0
    path_coords: set[tuple[int, int]] = set()

    # 2. Carga inicial del mapa
    result = load_maze(filepath)
    if (result is None):
        return (1)

    data, maze, hex_grid, ENTRY, EXIT, solution = result

    # Pre-calculamos las coordenadas visuales del camino si existe solución
    entry_cell = grid_to_cell_coords(ENTRY, data.WIDTH, data.HEIGHT)
    if (solution):
        path_coords = get_path_coords(ENTRY, EXIT, entry_cell, solution)

    # 3. Bucle infinito del menú interactivo
    while (True):
        # Imprimimos el laberinto con las opciones visuales actuales
        print("\n" + "="*50)
        print_colored_maze(maze, path_coords, show_path,
                           color_list[current_color_idx])
        print("="*50)

        if (not solution):
            print("Aviso: Sin solucion disponible para este mapa.")

        print_menu()

        # Captura de input con protección (Ctrl+C / Ctrl+D)
        try:
            choice = input("Elige una opcion (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            return (0)

        # 4. Gestión de las opciones
        if (choice == '1'):
            try:
                new_path = input("Ruta del nuevo config: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nSaliendo...")
                return (0)

            new_result = load_maze(new_path)
            if (new_result is None):
                print("Error al cargar. Se mantiene el mapa actual.")
            else:
                # Si carga bien, actualizamos TODAS las variables
                data, maze, hex_grid, ENTRY, EXIT, solution = new_result
                entry_cell = grid_to_cell_coords(ENTRY, data.WIDTH,
                                                 data.HEIGHT)
                if (solution):
                    path_coords = get_path_coords(ENTRY, EXIT, entry_cell,
                                                  solution)
                else:
                    path_coords = set()

        elif (choice == '2'):
            write_output_file(data.OUTPUT_FILE, hex_grid, ENTRY, EXIT,
                              solution)
            print(f"Mapa guardado en: {data.OUTPUT_FILE}")

        elif (choice == '3'):
            # Alterna entre True y False
            show_path = not show_path

        elif (choice == '4'):
            # Avanza al siguiente color en la lista de forma cíclica
            current_color_idx = (current_color_idx + 1) % len(color_list)

        elif (choice == '5'):
            print("Saliendo...")
            return (0)

        else:
            print("Opcion no valida. Elige un numero del 1 al 5.")


def main(ac: int, av: list[str]) -> int:
    """Entry point. Expects exactly one argument: the config file path."""
    if (ac != 2):
        print(f"Program use: Python3 {sys.argv[0]} <file>")
        return (1)
    return (run_menu(av[1]))


if (__name__ == "__main__"):
    sys.exit(main(len(sys.argv), sys.argv))
