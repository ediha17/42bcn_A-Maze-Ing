# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    mazegen.py                                        :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/22 17:46:50 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/24 11:37:47 by agarcia2        ###   ########.fr        #
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

    coords = [(2, 0), (-2, 0), (0, -2), (0, 2)]
    random.shuffle(coords)
    i = 0
    while (i < len(coords)):
        next_x = x + coords[i][0]
        next_y = y + coords[i][1]
        if (next_x > 0 and next_x < width - 1 and
            next_y > 0 and next_y < height - 1 and
                maze[next_y][next_x] == '|'):
            wall_x = x + (coords[i][0] // 2)
            wall_y = y + (coords[i][1] // 2)
            maze[wall_y][wall_x] = ' '
            maze[next_y][next_x] = ' '
            DFS(maze, next_x, next_y, width, height)
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
