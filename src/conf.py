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
    max_cx = (len(maze[0]) - 1) // 2 - 1
    max_cy = (len(maze) - 1) // 2 - 1

    for is_entry, pos in [(True, ent), (False, ext)]:
        cx, cy = pos

        # SISTEMA DE SEGURIDAD: Mantenemos la coordenada dentro del mapa
        cx = max(0, min(cx, max_cx))
        cy = max(0, min(cy, max_cy))

        # Calculamos el centro del pasillo
        char_x = cx * 2 + 1
        char_y = cy * 2 + 1

        # Colocamos el icono directamente en el pasillo, sin tocar los muros
        maze[char_y][char_x] = 'x' if is_entry else 'o'


def print_map(maze: list[list[str]]) -> None:
    i: int

    if (not maze):
        return (None)
    i = 0
    while (i < len(maze)):
        print("".join(maze[i]))
    i += 1
    return (None)
