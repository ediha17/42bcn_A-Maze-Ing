def maze_to_hex_grid(
        maze: list[list[str]], width: int, height: int) -> list[str]:
    rows: list[str]
    row_str: str
    cell_val: int
    gx: int
    gy: int

    rows = []
    gy = 1
    while (gy < height - 1):
        row_str = ''
        gx = 1
        while (gx < width - 1):
            cell_val = 0
            if (maze[gy - 1][gx] == '|'):
                cell_val |= 1
            if (maze[gy][gx + 1] == '|'):
                cell_val |= 2
            if (maze[gy + 1][gx] == '|'):
                cell_val |= 4
            if (maze[gy][gx - 1] == '|'):
                cell_val |= 8
            row_str += format(cell_val, 'X')
            gx += 2
        rows.append(row_str)
        gy += 2
    return (rows)


def write_output_file(path: str, hex_rows: list[str],
                      entry: list[int], exit_: list[int],
                      solution: str, seed: int) -> None:
    i: int

    with open(path, 'w') as f:
        i = 0
        while (i < len(hex_rows)):
            f.write(hex_rows[i] + '\n')
            i += 1
        f.write('\n')
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        f.write(solution + '\n')
    return (None)
