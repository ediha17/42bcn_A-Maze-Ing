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
    SEED: Optional[int] = None

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
        return None

    map["WIDTH"] = (map["WIDTH"] * 2) + 1
    map["HEIGHT"] = (map["HEIGHT"] * 2) + 1

    try:
        map['PERFECT'] = (map['PERFECT'] == "True")
        return (MazeConfig(**map))
    except Exception as e:
        print(f"Error de validación Pydantic: {e}")
        return None


def set_entry_exit(maze: list[list[str]], ent: list[int],
                   ext: list[int]) -> None:
    # Máximo índice de celda posible
    max_cx = (len(maze[0]) - 1) // 2 - 1
    max_cy = (len(maze) - 1) // 2 - 1

    for is_entry, pos in [(True, ent), (False, ext)]:
        cx, cy = pos

        cx = max(0, min(cx, max_cx))
        cy = max(0, min(cy, max_cy))

        # Coordenada del centro del pasillo en la matriz de caracteres
        char_x = cx * 2 + 1
        char_y = cy * 2 + 1

        # Mapeamos a la pared exterior dependiendo de en qué borde esté
        if cx == 0:
            wall_x, wall_y = 0, char_y
            break_x, break_y = 1, char_y
        elif cx >= max_cx:
            wall_x, wall_y = char_x + 1, char_y
            break_x, break_y = char_x, char_y
        elif cy == 0:
            wall_x, wall_y = char_x, 0
            break_x, break_y = char_x, 1
        elif cy >= max_cy:
            wall_x, wall_y = char_x, char_y + 1
            break_x, break_y = char_x, char_y
        else:
            wall_x, wall_y = char_x, char_y
            break_x, break_y = char_x, char_y

        # Colocamos el icono y rompemos la pared hacia adentro
        maze[wall_y][wall_x] = 'x' if is_entry else 'o'
        if wall_x != break_x or wall_y != break_y:
            maze[break_y][break_x] = ' '


def print_map(maze: list[list[str]]) -> None:
    i: int

    if (not maze):
        return (None)
    i = 0
    while (i < len(maze)):
        print("".join(maze[i]))
    i += 1
    return (None)
