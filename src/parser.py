# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    parser.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 18:57:59 by agarcia2         #+#    #+#              #
#    Updated: 2026/07/01 00:33:53 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


def ft_parser(fd: bytes) -> dict:
    """Parse a KEY=VALUE config file from raw bytes.

    Lines starting with '#' and empty lines are ignored. Values that
    can be cast to int are stored as int; otherwise as str.

    Args:
        fd: Raw file contents as bytes.

    Returns:
        Dict mapping each key (str) to its parsed value (int or str).
    """
    map: dict
    lines: list[str]
    parts: list[str]
    i: int

    i = 0
    map = {}
    try:
        lines = fd.decode('utf-8').split('\n')
    except UnicodeDecodeError:
        print("Error: the configuration file is not valid UTF-8")
        return ({})
    while (i < len(lines)):
        if (len(lines[i]) == 0 or lines[i][0] == '#'):
            i += 1
            continue
        parts = lines[i].split('=')
        if (len(parts) == 2):
            if (parts[1].strip()):
                try:
                    map[parts[0].strip()] = int(parts[1].strip())
                except ValueError:
                    map[parts[0].strip()] = parts[1].strip()
        i += 1
    return (map)


def ft_parser_map(map: dict) -> bool:
    """Validate that all required config keys are present.

    Args:
        map: Parsed config dict.

    Returns:
        True if all required keys exist, False otherwise.
    """
    req: list[str]
    i: int

    req = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    i = 0
    while (i < len(req)):
        if (req[i] not in map):
            print(f"Error: Missing key {req[i]}")
            return (False)
        i += 1
    if (map["PERFECT"] not in ("True", "False")):
        print("Error: PERFECT must be 'True' or 'False'")
        return (False)
    return (True)


def ft_parser_coords(raw: str) -> list[int]:
    """Parse a 'x,y' coordinate string into a two-element int list.

    Args:
        raw: Coordinate string in the form 'x,y' (whitespace is stripped).

    Returns:
        [x, y] on success, or [-1, -1] if the format is invalid.
    """
    new: list[str]
    coords: list[int]
    i: int

    new = raw.split(',')
    coords = []
    if (len(new) != 2):
        return ([-1, -1])
    i = 0
    while (i < len(new)):
        if (new[i].strip()):
            coords.append(int(new[i].strip()))
        else:
            return ([-1, -1])
        i += 1

    return (coords)


def check_patern42(width: int, heigth: int) -> bool:
    """Return True if the maze is large enough to display the '42' pattern.

    Args:
        width: Maze grid width.
        heigth: Maze grid height.

    Returns:
        False and prints an error if either dimension is below 7.
    """
    if (width < 7 or heigth < 7):
        print("Error: The maze size does not allow the '42' pattern.")
        return (False)
    return (True)
