*This project has been created as part of the 42 curriculum by  <yuhli> <huwang>*

---

# 🌀 A-Maze-ing

> A Python-based random maze generator with interactive ASCII visualization and hexadecimal wall output.

---

## Description

**A-Maze-ing** reads a configuration file, generates a random maze, and outputs it in a hexadecimal wall format. It also provides an interactive ASCII visualization with commands to regenerate the maze, toggle the solution path, and change wall colors.

The maze generator supports both **perfect mazes** (where every pair of cells has exactly one path connecting them) and **imperfect mazes** (with extra loops added for variety). Reproducible results are supported via an optional random seed.

---

## Instructions

### Prerequisites

- Python **3.10** or higher
- *(Optional)* Development tools for linting and testing:

```bash
pip install flake8 mypy pytest build types-setuptools
```

### Setup

```bash
# Clone the repository
git clone
cd a-maze-ing

# (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # Linux / macOS
# venv\Scripts\activate        # Windows
```

### Running

```bash
python3 a_maze_ing.py config.txt
```
### Interactive Commands
Once the maze is displayed, you can use the following keys:

| Key   |Action                                                |
| ----- | ----------------------------------------------------- |
| **r** | Regenerate a new maze using the same configuration    |
| **p** | Toggle display of the shortest solution path          |
| **c** | Cycle through available wall color schemes            |
| **a** | Animate the maze generation process *(Bonus feature)* |
| **q** | Quit the program                                      |

The animation shows the recursive backtracker in action: each step removes a wall, and the current DFS stack is highlighted with . characters. After the animation, the maze is finalized (cycles added if PERFECT=false, and the "42" pattern embedded).

### Makefile Commands

| Command | Description |
|---|---|
| `make install` | Install development dependencies (flake8, mypy, etc.) |
| `make run` | Run the program with the default config |
| `make debug` | Run the program in debug mode with pdb |
| `make lint` | Run `flake8` and `mypy` |
| `make lint-strict` | Run `mypy` in strict mode |
| `make clean` | Remove cache files |

---

## Configuration File Format

Lines starting with `#` are treated as comments and ignored. Each setting follows the `KEY=VALUE` format.

### Required Keys

| Key | Type | Description |
|---|---|---|
| `WIDTH` | Integer | Number of cells horizontally |
| `HEIGHT` | Integer | Number of cells vertically |
| `ENTRY` | `x,y` | Entrance coordinates (0-based) |
| `EXIT` | `x,y` | Exit coordinates (0-based) |
| `OUTPUT_FILE` | String | Filename for the output maze data |
| `PERFECT` | Boolean | `true` = single solution path; `false` = extra loops |

### Optional Keys

| Key | Type | Description |
|---|---|---|
| `SEED` | Integer | Fixed seed for reproducible maze generation |

### Example Configuration

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

---

## Maze Generation Algorithm

The maze is generated using the **Recursive Backtracker** (depth-first search) algorithm.

Starting from a random cell, the algorithm carves a path by visiting unvisited neighbors recursively, backtracking when it reaches a dead end. This continues until every cell has been visited, producing a perfect maze with no isolated areas.

For **non-perfect mazes**, additional cycles are introduced by randomly removing a subset of internal walls after the initial generation.

### Why This Algorithm?

- **Simple to implement** — clean recursive logic with minimal state
- **Efficient** — runs in O(n) time and space relative to the number of cells
- **High-quality output** — produces long, winding corridors that feel natural and challenging
- **Well-understood** — extensively documented with no edge-case surprises

---

## Reusable Module

Building from Source
To build the wheel yourself, run:
```bash
pip install build
python3 -m build
```
The generated files will be in the dist/ directory.
The core generation logic is encapsulated in the `MazeGenerator` class inside `maze_generator.py`. It can be imported and used independently of the CLI.

### Installation
You can install the pre-built wheel package directly:
```bash
pip install mazegen_huwang_yuhli-1.0.0-py3-none-any.whl

### Verification
After installation, verify that the module works:
python3 -c "from maze_generator import MazeGenerator; mg = MazeGenerator(10, 10); mg.generate(); print(mg.get_cell_walls(0, 0))"

This should print an integer between 0 and 15 (e.g., 15).

### Usage Example
```python3
from maze_generator import MazeGenerator

mg = MazeGenerator(20, 15, seed=42)
mg.generate()

walls = mg.get_cell_walls(5, 5)
mg.set_entry_exit((0, 0), (19, 14))
path = mg.solve()
print(f"Path: {path}")
```


---

## Resources

- [Maze generation algorithm — Recursive Backtracker (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [Python `random` module documentation](https://docs.python.org/3/library/random.html)
- [BFS Pathfinding algorithm](https://en.wikipedia.org/wiki/Breadth-first_search)

**AI usage:**
AI was used to assist with designing the BFS pathfinding logic and debugging wall consistency issues across cell boundaries. All AI-generated suggestions were reviewed and validated by team members before integration.

---

## Team & Project Management

### Team Members

| Member | Role |
|---|---|
| **huwang** | Maze generation algorithm, config parsing, output formatting |
| **yuhli** | ASCII visualization, interactive features, packaging & documentation |

### Planning

| Week | Goals | Outcome |
|---|---|---|
| Week 1 | Project setup, config parsing, basic maze generation | ✅ Completed on schedule |
| Week 2 | Output file writing, ASCII rendering | ✅ Completed on schedule |
| Week 3 | Interactive features, packaging, documentation | ✅ Completed with minor delays on packaging |

### Retrospective

**What worked well:**
- The Recursive Backtracker was straightforward to implement and debug.
- Separating the `MazeGenerator` class from the CLI early on made testing and iteration much easier.
- Clear division of responsibilities between team members minimized merge conflicts.

**What could be improved:**
- The "42" pattern embedding is simplistic and can break maze connectivity in certain configurations. A constraint-aware approach would produce better results.
- More unit tests around edge cases (e.g., very small mazes, entry/exit on the same cell) would improve robustness.

### Tools Used

- **VS Code** — primary editor
- **Git** — version control and collaboration
- **Python standard library** — core implementation
- **flake8 / mypy** — linting and static type checking
- **pytest** — unit testing

### Interactive Commands

Once the maze is displayed, you can use the following keys:
