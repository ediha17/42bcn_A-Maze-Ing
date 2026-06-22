# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    mazegen.py                                        :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: agarcia2 <agarcia2@student.42barcelona.c  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/06/22 17:46:50 by agarcia2         #+#    #+#              #
#    Updated: 2026/06/22 18:13:15 by agarcia2        ###   ########.fr        #
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
