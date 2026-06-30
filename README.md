# A-Maze-Ing

A maze generator and solver written in Python 3.11. Generates random mazes
with a configurable size, entry/exit points, and an optional "42" pattern
stamped into the grid. The solution path is computed with BFS and written to
an output file in hexadecimal encoding.

---

## Usage

```bash
python3 a_maze_ing.py <config_file>
```

Example:

```bash
python3 a_maze_ing.py config_standard.txt
```

---

## Config file format

`KEY=VALUE` pairs, one per line. Lines starting with `#` are comments.

| Key | Type | Description | Example |
|---|---|---|---|
| `WIDTH` | int | Character-grid width (≥ 7) | `WIDTH=20` |
| `HEIGHT` | int | Character-grid height (≥ 7) | `HEIGHT=15` |
| `ENTRY` | x,y | Entry point (grid coordinates) | `ENTRY=0,1` |
| `EXIT` | x,y | Exit point (grid coordinates) | `EXIT=19,13` |
| `OUTPUT_FILE` | str | Path for the hex output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | `True` = unique path; `False` = cycles | `PERFECT=True` |

---

## Output file format

The output file contains:

1. One row per line, each character a hex digit encoding the cell's walls:
   - bit 0 (LSB) = North wall closed
   - bit 1 = East wall closed
   - bit 2 = South wall closed
   - bit 3 = West wall closed
2. A blank line.
3. Entry coordinates (`x,y`).
4. Exit coordinates (`x,y`).
5. Solution path as a sequence of `N`/`E`/`S`/`W` directions.

Example:
```
157D1395
AFFD6C6B
...

0,1
19,13
SSEESWNE
```

---

## Algorithm

**Recursive Backtracker (DFS)**

We chose this algorithm because:
- It produces mazes with long, winding corridors and a single clear solution
  path when `PERFECT=True` — the grid becomes a spanning tree.
- Implementation is straightforward with no external data structures beyond
  the call stack.
- When `PERFECT=False`, a post-processing pass randomly removes ~15 % of
  remaining interior walls to introduce cycles.

The solution is found with **BFS on the hex-encoded cell graph**, which
guarantees the shortest path in unweighted grids.

---

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
mg.draw_pattern_42(start_x=2, start_y=2)
maze = mg.get_maze()          # list[list[str]] character grid
```

To rebuild from source:

```bash
make build
pip install mazegen-1.0.0-py3-none-any.whl
```

---

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

---

## Team & roles

| Member | Role |
|---|---|
| **agarcia2** | Maze generation (DFS), config parser, hex output, BFS solver, packaging |
| **< compañero >** | *(fill in)* |

---

## Planning & evolution

1. **Week 1** — Config parser, maze grid representation, DFS generator.
2. **Week 2** — BFS path-finder, "42" pattern, entry/exit handling.
3. **Week 3** — Hex output format, `MazeGenerator` class, pip packaging.
4. **Week 4** — Docstrings, pytest test suite, Makefile, README.

Key decisions:
- Used **Pydantic** for config validation — catches type errors and missing
  keys with clear messages, avoiding manual validation boilerplate.
- Chose a **character grid** (not a bitmask array) as the internal
  representation so the ASCII terminal display is trivial.
- Kept a **cell-level BFS** in `src/output.py` separate from the
  character-grid BFS — this guarantees the solution in the output file uses
  correct cell-to-cell directions.

---

## What worked / what could be improved

**Worked well**
- The DFS produces dense, solvable mazes consistently.
- Pydantic validation gives useful error messages with zero boilerplate.
- The hex encoding conversion is clean and testable in isolation.

**Could be improved**
- A second generation algorithm (Prim / Kruskal) would give maze variety and
  cover the bonus points.
- The character-grid representation ties WIDTH/HEIGHT to grid coordinates
  rather than logical cell counts — a future version should use a bitmask
  array of size WIDTH × HEIGHT for the cell graph directly.
- Terminal visualisation is static; interactive re-generation and
  show/hide-path would improve the demo.

---

## Tools used

- **Python 3.11** — main language
- **Pydantic v2** — config validation
- **pytest** — test suite
- **flake8** — PEP 8 linting
- **mypy** — static type checking
- **build / setuptools / wheel** — packaging
- **git** — version control (conventional commits)
