# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    parser.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/17 18:57:59 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/17 20:33:30 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

def ft_parser(fd: bytes) -> dict:
    map: dict
    lines: list[str]
    parts: list[str]
    i: int

    i = 0
    map = {}
    lines = fd.decode('utf-8').split('\n')
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
    req: list[str]
    i: int

    req = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    i = 0
    while (i < len(req)):
        if (req[i] not in map):
            print(f"Error: Missing key {req[i]}")
            return (False)
        i += 1
    return (True)


def ft_parser_coords(raw: str) -> list[int]:
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
    if (width < 7 or heigth < 7):
        print("Error: The maze size does not allow the '42' pattern.")
        return (False)
    return (True)
