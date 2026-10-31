#!/usr/bin/env python3
"""A-Maze-ing - Main program with animation bonus.

Reads a configuration file, generates a maze, writes output file,
and provides interactive ASCII visualization with animation.
"""

import sys
import random
import time
from typing import Dict, Tuple, Optional, NamedTuple

from maze_generator import MazeGenerator


class Config(NamedTuple):
    """Configuration parameters for maze generation.

    Attributes:
        width: Number of cells horizontally.
        height: Number of cells vertically.
        entry: (x, y) coordinates of the entrance.
        exit: (x, y) coordinates of the exit.
        output_file: Path to the output file.
        perfect: True if the maze must be perfect (single path).
        seed: Optional random seed for reproducibility.
    """
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int]


def parse_config(filename: str) -> Config:
    """Parse the configuration file and return a typed Config object.

    The file must contain KEY=VALUE lines. Lines starting with '#' are ignored.
    Inline comments (after '#') are also stripped.

    Args:
        filename: Path to the configuration file.

    Returns:
        A Config object with all fields properly typed.

    Raises:
        SystemExit: If the file cannot be read, required keys are missing,
            values are malformed, or coordinates are out of bounds.
    """
    raw_config: Dict[str, str] = {}
    required_keys = {
        'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'
    }

    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Remove inline comments
                if '#' in line:
                    line = line[:line.index('#')].strip()
                    if not line:
                        continue
                if '=' not in line:
                    raise ValueError(f"Line {line_num}: missing '='")
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                raw_config[key] = value
    except FileNotFoundError:
        print(f"Error: Config file '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing config: {e}")
        sys.exit(1)

    # Check required keys
    missing = required_keys - set(raw_config.keys())
    if missing:
        print(f"Error: Missing required keys: {', '.join(missing)}")
        sys.exit(1)

    # Convert types
    try:
        width = int(raw_config['WIDTH'])
        height = int(raw_config['HEIGHT'])

        ex, ey = raw_config['ENTRY'].split(',')
        entry = (int(ex), int(ey))
        xx, xy = raw_config['EXIT'].split(',')
        exit_ = (int(xx), int(xy))

        perfect = raw_config['PERFECT'].lower() in ('true', '1', 'yes')

        seed: Optional[int] = None
        if 'SEED' in raw_config:
            seed = int(raw_config['SEED'])
    except (ValueError, IndexError) as e:
        print(f"Error: Invalid value format: {e}")
        sys.exit(1)

    # Bounds checking
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        print("Error: ENTRY out of bounds")
        sys.exit(1)
    if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
        print("Error: EXIT out of bounds")
        sys.exit(1)
    if entry == exit_:
        print("Error: Entry and exit must be different")
        sys.exit(1)

    return Config(
        width, height, entry, exit_,
        raw_config['OUTPUT_FILE'], perfect, seed
    )


def write_maze_file(filename: str, grid: list[list[int]],
                    entry: Tuple[int, int], exit_: Tuple[int, int],
                    path: Optional[str]) -> None:
    """Write the maze data to a file in the required format.

    Format:
        - One line per row of hexadecimal wall codes.
        - Empty line.
        - Entry coordinates as "x,y".
        - Exit coordinates as "x,y".
        - Path string (or empty line if no path).

    Args:
        filename: Output file path.
        grid: 2D list of wall codes (0-15).
        entry: (x, y) entrance coordinates.
        exit_: (x, y) exit coordinates.
        path: Direction string (e.g., "SENW") or None.
    """
    with open(filename, 'w') as f:
        for row in grid:
            line = ''.join(hex(cell)[2:].upper() for cell in row)
            f.write(line + '\n')
        f.write('\n')  # empty line
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        if path is not None:
            f.write(path + '\n')
        else:
            f.write('\n')


def render_maze(maze: MazeGenerator, show_path: bool = False,
                path: Optional[str] = None,
                color_code: str = '', reset_code: str = '',
                frontier: Optional[set[tuple[int, int]]] = None) -> str:
    """Render the maze as an ASCII string using '+', '-', '|', and spaces.

    The rendering uses a classic grid style where each cell is represented
    by a 3x3 block of characters. Walls are drawn with '-', '|', and '+',
    while cell interiors are spaces, 'E', 'X', '*', or '#' (for fully closed
    cells).

    Args:
        maze: The MazeGenerator instance.
        show_path: If True, mark the path with '*'.
        path: The direction string of the path (required if show_path=True).
        color_code: ANSI color code for walls.
        reset_code: ANSI reset code.
        frontier: Optional set of (x,y) cells on the DFS stack,
            displayed as '.' to visualise the animation frontier.

    Returns:
        A multi-line string representing the maze.
    """
    grid = maze.grid
    rows = maze.height
    cols = maze.width
    entry = maze.entry
    exit_ = maze.exit

    # These must be set before rendering
    assert entry is not None
    assert exit_ is not None

    # Prepare path cells and edges if needed
    path_cells = set()
    path_edges = []
    if show_path and path is not None:
        cur = entry
        path_cells.add(cur)
        for d in path:
            if d == 'N':
                nxt = (cur[0], cur[1] - 1)
            elif d == 'S':
                nxt = (cur[0], cur[1] + 1)
            elif d == 'E':
                nxt = (cur[0] + 1, cur[1])
            elif d == 'W':
                nxt = (cur[0] - 1, cur[1])
            else:
                continue
            path_edges.append((cur, nxt))
            path_cells.add(nxt)
            cur = nxt

    # Canvas size: (2*rows+1) x (2*cols+1)
    H = 2 * rows + 1
    W = 2 * cols + 1
    canvas = [[' ' for _ in range(W)] for _ in range(H)]

    # Draw all junctions as '+'
    for r in range(0, H, 2):
        for c in range(0, W, 2):
            canvas[r][c] = '+'

    # Draw walls based on grid
    for y in range(rows):
        for x in range(cols):
            cell = grid[y][x]
            # North wall
            if (cell >> MazeGenerator.N) & 1:
                canvas[2 * y][2 * x + 1] = '-'
            # South wall
            if (cell >> MazeGenerator.S) & 1:
                canvas[2 * y + 2][2 * x + 1] = '-'
            # West wall
            if (cell >> MazeGenerator.W) & 1:
                canvas[2 * y + 1][2 * x] = '|'
            # East wall
            if (cell >> MazeGenerator.E) & 1:
                canvas[2 * y + 1][2 * x + 2] = '|'

    # Draw cell interiors and markers
    for y in range(rows):
        for x in range(cols):
            cx, cy = 2 * x + 1, 2 * y + 1  # canvas coordinates (col, row)
            cell = grid[y][x]
            if (x, y) == entry:
                canvas[cy][cx] = 'E'
            elif (x, y) == exit_:
                canvas[cy][cx] = 'X'
            elif show_path and (x, y) in path_cells:
                canvas[cy][cx] = '*'
            elif frontier and (x, y) in frontier:
                canvas[cy][cx] = '.'
            elif (x, y) in maze.pattern_42_cells:  # part of 42 pattern
                canvas[cy][cx] = '#'
            else:
                canvas[cy][cx] = ' '

    # Draw path edges (between cells)
    if show_path and path_edges:
        for (a, b) in path_edges:
            if a[0] == b[0]:  # same column, vertical move
                if b[1] > a[1]:  # south
                    canvas[2 * a[1] + 2][2 * a[0] + 1] = '*'
                else:  # north
                    canvas[2 * a[1]][2 * a[0] + 1] = '*'
            else:  # same row, horizontal move
                if b[0] > a[0]:  # east
                    canvas[2 * a[1] + 1][2 * a[0] + 2] = '*'
                else:  # west
                    canvas[2 * a[1] + 1][2 * a[0]] = '*'

    # Convert canvas to list of strings
    result_lines = [''.join(row) for row in canvas]

    # Apply color only to wall characters if requested
    if color_code:
        wall_chars = {'+', '-', '|'}
        colored_lines = []
        for line in result_lines:
            new_line = ''
            for ch in line:
                if ch in wall_chars:
                    new_line += color_code + ch + reset_code
                else:
                    new_line += ch
            colored_lines.append(new_line)
        result_lines = colored_lines

    return '\n'.join(result_lines)


def interactive_loop(maze: MazeGenerator, cfg: Config) -> None:
    """Run the interactive command loop for the maze with animation bonus.

    Displays the maze and responds to user commands:
        r : regenerate the maze with the same configuration
        p : toggle path display
        c : cycle through wall colors
        a : animate the maze generation process
        q : quit

    Args:
        maze: The MazeGenerator instance.
        cfg: The configuration object.
    """
    show_path = False
    path = maze.solve()  # compute initial path

    # Color settings
    color_index = 0
    colors = [
        '',                           # 0: default (no color)
        '\033[31m',                   # 1: red
        '\033[32m',                   # 2: green
        '\033[34m',                   # 3: blue
        '\033[33m',                   # 4: yellow
    ]
    reset = '\033[0m'

    while True:
        # Clear screen using ANSI — no subprocess, no blank frame
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()

        # Render maze as string
        maze_str = render_maze(
            maze, show_path,
            path if show_path else None,
            color_code=colors[color_index],
            reset_code=reset
        )
        print(maze_str)

        print(
            "\nCommands: [r]egenerate, [p] toggle path, "
            "[c] change color, [a] animate, [q]uit"
        )
        cmd = input("> ").strip().lower()

        if cmd == 'q':
            break
        elif cmd == 'r':
            if cfg.seed is not None:
                random.seed(cfg.seed)
            maze.generate()
            maze.set_entry_exit(cfg.entry, cfg.exit)
            if not cfg.perfect:
                maze.add_cycles(probability=0.1)
            maze.embed_42()
            path = maze.solve()
            if path is None:
                print("Warning: No path found after regeneration.")
            else:
                write_maze_file(cfg.output_file, maze.grid,
                                cfg.entry, cfg.exit, path)
            show_path = False
        elif cmd == 'p':
            show_path = not show_path
        elif cmd == 'c':
            color_index = (color_index + 1) % len(colors)
        elif cmd == 'a':
            # Animate generation — hide cursor to reduce visual noise
            sys.stdout.write('\033[?25l')
            sys.stdout.flush()
            try:
                if cfg.seed is not None:
                    random.seed(cfg.seed)
                maze.set_entry_exit(cfg.entry, cfg.exit)
                first_frame = True
                for _ in maze.generate_animated(perfect=cfg.perfect):
                    frontier = getattr(maze, 'anim_frontier', None)
                    if first_frame:
                        # Full clear once so old content is gone
                        sys.stdout.write('\033[2J\033[H')
                        sys.stdout.flush()
                        first_frame = False
                    else:
                        # Move cursor home and overwrite — no blank frame
                        sys.stdout.write('\033[H')
                        sys.stdout.flush()
                    maze_str = render_maze(
                        maze, False, None,
                        color_code=colors[color_index],
                        reset_code=reset,
                        frontier=frontier
                    )
                    sys.stdout.write(maze_str + '\n')
                    sys.stdout.write('\033[K')
                    sys.stdout.flush()
                    time.sleep(0.03)
            finally:
                sys.stdout.write('\033[?25h')
                sys.stdout.flush()
            # After animation, apply cycles if non-perfect and embed 42
            if not cfg.perfect:
                maze.add_cycles(probability=0.1)
            maze.embed_42()
            path = maze.solve()
            if path is None:
                print("Warning: No path found after animation.")
            else:
                write_maze_file(cfg.output_file, maze.grid,
                                cfg.entry, cfg.exit, path)
            show_path = False
        else:
            print("Unknown command.")


def main() -> None:
    """Main entry point.

    Parses command line arguments, reads configuration,
    generates the maze, writes the output file, and starts
    the interactive loop.
    """
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]
    cfg = parse_config(config_file)

    maze = MazeGenerator(cfg.width, cfg.height, cfg.seed)
    maze.generate()
    maze.set_entry_exit(cfg.entry, cfg.exit)
    if not cfg.perfect:
        maze.add_cycles(probability=0.1)
    maze.embed_42()

    path = maze.solve()
    if path is None:
        print("Error: No path from entry to exit found.")
        sys.exit(1)

    write_maze_file(cfg.output_file, maze.grid, cfg.entry, cfg.exit, path)
    print(f"Maze written to {cfg.output_file}")

    interactive_loop(maze, cfg)


if __name__ == "__main__":
    main()
