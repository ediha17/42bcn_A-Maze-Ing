# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    mazegen.py                                        :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/22 17:46:50 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/23 15:10:23 by agarcia2        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import random


def generate_maze(maze: list[list[str]], width: int, height: int) -> None:
    maze[1][1] = ' '

    DFS(maze, 1, 1, width, height)


def DFS(maze: list[list[str]], x: int, y: int,
        width: int, height: int) -> None:

    coords: list[tuple[int, int]]
    i: int

    coords = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(coords)
    i = 0
    while (i < len(coords)):
        if (x + coords[i][0] > 0 and x + coords[i][0] < width and
            y + coords[i][1] > 0 and y + coords[i][1] < height and
                maze[y + coords[i][1]][x + coords[i][0]] == '|'):
            maze[y + coords[i][1]][x + coords[i][0]] = ' '
            maze[y + coords[i][1] // 2][x + coords[i][0] // 2] = ' '
            DFS(maze, x + coords[i][0], y + coords[i][1], width, height)
        i += 1


def draw_pattern_42(maze: list[list[str]], start_x: int, start_y: int) -> None:
    pattern = ["11111", "10101", "11101", "10101", "11111"]
    y = 0
    while y < len(pattern):
        x = 0
        while x < len(pattern[y]):
            if pattern[y][x] == '1':
                maze[start_y + y][start_x + x] = '|'
            x += 1
        y += 1


def check_collision(start_x: int, start_y: int, pos: list[int]) -> bool:
    return (start_x <= pos[0] < start_x + 5) and (start_y <= pos[1] < start_y + 5)
