# A-Maze-Ing

A maze generator and solver written in Python 3.11. Generates random mazes with a configurable size, entry/exit points, and a "42" pattern seamlessly stamped into the grid if dimensions allow. Features an interactive terminal interface to visualize the maze, toggle the solution path, and regenerate maps on the fly. The solution path is computed with BFS and written to an output file in hexadecimal encoding.

## Usage

```bash
python3 a_maze_ing.py <config_file>
```

Example:

```bash
python3 a_maze_ing.py config_standard.txt
```

## Config file format

`KEY=VALUE` pairs, one per line. Lines starting with `#` are comments.

| Key | Type | Description | Example |
|---|---|---|---|
| WIDTH | int | Number of horizontal cells (passageways) | `WIDTH=20` |
| HEIGHT | int | Number of vertical cells (passageways) | `HEIGHT=15` |
| ENTRY | x,y | Entry point (cell coordinates) | `ENTRY=0,1` |
| EXIT | x,y | Exit point (cell coordinates) | `EXIT=19,13` |
| OUTPUT_FILE | str | Path for the hex output file | `OUTPUT_FILE=maze.txt` |
| PERFECT | bool | True = unique path; False = cycles | `PERFECT=True` |

## Output file format

The output file contains:

1. One row per line, each character a hex digit encoding the cell's walls:
   - bit 0 (LSB) = North wall closed
   - bit 1 = East wall closed
   - bit 2 = South wall closed
   - bit 3 = West wall closed
2. A blank line.
3. Entry coordinates (x,y).
4. Exit coordinates (x,y).
5. Solution path as a sequence of N/E/S/W directions.

Example:

```
157D1395
AFFD6C6B
...

0,1
19,13
SSEESWNE
```

## Algorithm

**Recursive Backtracker (DFS)**

We chose this algorithm because:

- It produces mazes with long, winding corridors and a single clear solution path when `PERFECT=True` — the grid becomes a spanning tree.
- Implementation is straightforward with no external data structures beyond the call stack.
- When `PERFECT=False`, a post-processing pass randomly removes ~15% of remaining interior walls to introduce cycles.
- The solution is found with BFS on the hex-encoded cell graph, which guarantees the shortest path in unweighted grids.

## Reusable module — mazegen

The `mazegen` package can be installed independently:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Then in any Python project:

```python
from mazegen import MazeGenerator

mg = MazeGenerator(width=9, height=9, seed=42, perfect=True)
mg.generate()
maze = mg.get_maze()          # list[list[str]] character grid
```

To rebuild from source:

```bash
make build
pip install mazegen-1.0.0-py3-none-any.whl
```

## Makefile rules

| Rule | Description |
|---|---|
| `make install` | Install Python dependencies |
| `make run` | Run with default config |
| `make debug` | Run under pdb debugger |
| `make clean` | Remove caches and build artefacts |
| `make lint` | Run flake8 + mypy |
| `make build` | Build wheel and sdist |
| `make reinstall` | Force-reinstall the local wheel |

## Team & roles

| Member | Role |
|---|---|
| agarcia2 | Maze generation (DFS), config parser, hex output, BFS solver, packaging |
| ehorvat | Interactive UI, path visualization, error handling, coordinate mapping, '42' pattern integration |

## Planning & evolution

- **Week 1** — Config parser, maze grid representation, DFS generator.
- **Week 2** — BFS path-finder, "42" pattern, entry/exit handling.
- **Week 3** — Hex output format, MazeGenerator class, pip packaging.
- **Week 4** — Interactive terminal UI, visual path-finding, edge-case safety, README.

### Key decisions

- Used Pydantic for config validation — catches type errors and missing keys with clear messages, avoiding manual validation boilerplate.
- Chose a character grid (not a bitmask array) as the internal representation so the ASCII terminal display is trivial.
- Kept a cell-level BFS in `src/output.py` separate from the character-grid BFS — this guarantees the solution in the output file uses correct cell-to-cell directions.
- Decoupled logic cell count (WIDTH/HEIGHT) from character grid constraints to ensure accurate exterior walls and 100% playable maps.

## What worked / what could be improved

### Worked well

- The DFS produces dense, solvable mazes consistently.
- Pydantic validation gives useful error messages with zero boilerplate.
- The hex encoding conversion is clean and testable in isolation.
- Terminal visualization is fully interactive; regenerating maps, swapping colors, and toggling the shortest path makes the demo extremely engaging.
- The '42' pattern acts as a natural wall boundary, allowing the maze corridors to flow through its internal gaps organically.

### Could be improved

- A second generation algorithm (Prim / Kruskal) would give maze variety and cover the bonus points.

## Tools used

- Python 3.11 — main language
- Pydantic v2 — config validation
- pytest — test suite
- flake8 — PEP 8 linting
- mypy — static type checking
- build / setuptools / wheel — packaging
- git — version control (conventional commits)
